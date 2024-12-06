#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging

from toscaparser.common import exception
from toscaparser.dataentity import DataEntity
from toscaparser import functions
from toscaparser.groups import Group
from toscaparser.nodetemplate import NodeTemplate
from toscaparser.parameters import Input
from toscaparser.parameters import Output
from toscaparser.policy import Policy
from toscaparser.workflow import Workflow
from toscaparser.relationship_template import RelationshipTemplate
from toscaparser.substitution_mappings import SubstitutionMappings
from toscaparser.utils.gettextutils import _
from toscaparser.common.exception import ExceptionCollector
from toscaparser.common.exception import ValidationError
from toscaparser.elements.statefulentitytype import StatefulEntityType
from toscaparser.elements.artifacttype import ArtifactTypeDef
from toscaparser.elements.relationshiptype import RelationshipType
from toscaparser.elements.nodetype import NodeType
from toscaparser.elements.entity_type import EntityType, Namespace


# Topology template key names
SECTIONS = (DESCRIPTION, INPUTS, NODE_TEMPLATES,
            RELATIONSHIP_TEMPLATES, OUTPUTS, GROUPS,
            SUBSTITUION_MAPPINGS, POLICIES, WORKFLOWS, ROOT) = \
           ('description', 'inputs', 'node_templates',
            'relationship_templates', 'outputs', 'groups',
            'substitution_mappings', 'policies', 'workflows', 'root')

log = logging.getLogger("tosca.model")


class TopologyTemplate(object):
    processIntrinsicFunctions = False

    '''Load the template data.'''
    def __init__(self, template, custom_defs,
                 parsed_params=None,
                 tosca_template=None):
        self.tpl = template or {}
        self.tosca_template = tosca_template
        self.custom_defs = custom_defs
        self.parsed_params = parsed_params
        self._validate_field()
        self.description = self._tpl_description()
        self.inputs = self._inputs()
        self.relationship_templates = self._relationship_templates()
        self.node_templates = self._nodetemplates()
        self.outputs = self._outputs()
        self.groups = self._groups()
        self.policies = self._policies()
        self.workflows = self._workflows()
        if not exception.ExceptionCollector.exceptionsCaught():
            if self.processIntrinsicFunctions:
                self._process_intrinsic_functions()
            else:
                self._validate_intrinsic_functions()

        self.substitution_mappings = None
        tpl_substitution_mapping = self._tpl_substitution_mappings()
        if tpl_substitution_mapping:
            self.substitution_mappings = SubstitutionMappings(tpl_substitution_mapping, self)

    def copy(self):
        return TopologyTemplate(self.tpl, self.custom_defs, self.parsed_params, self.tosca_template)

    def _inputs(self):
        inputs = []
        parsed_params = self.parsed_params
        for name, attrs in self._tpl_inputs().items():
            input = Input(name, attrs, self.custom_defs)
            if parsed_params is not None and name in parsed_params:
                input.validate(parsed_params[name])
            else:
                default = input.default
                if default:
                    input.validate(default)
            if parsed_params is not None:
                if (input.name not in parsed_params and input.required
                                            and input.default is None):
                      exception.ExceptionCollector.appendException(
                        exception.MissingRequiredInputError(
                            what=_('Topology template'),
                            input_name=input.name))

            inputs.append(input)
        return inputs

    @property
    def nodetemplates(self):
        return self.node_templates.values()

    def _nodetemplates(self):
        nodetemplates = {}
        tpls = self._tpl_nodetemplates()
        if tpls:
            for name in tpls:
                tpl = NodeTemplate(
                    name,
                    self,
                    self.custom_defs,
                    self.relationship_templates
                )
                # why these tests? defeats validation
                # if (tpl.type_definition and
                #     (tpl.type in tpl.type_definition.TOSCA_DEF or
                #      (tpl.type not in tpl.type_definition.TOSCA_DEF and
                #       bool(tpl.custom_def)))):
                tpl.validate(self)
                nodetemplates[name] = tpl
        return nodetemplates

    def add_template(self, name, tpl, get_relationships=True):
        # if name in self.node_templates:
        #     exception.ExceptionCollector.appendException(
        #           exception.ValidationError(message=
        #               'Node template already defined "%s"' % name))
        #     return None

        self.tpl.setdefault(NODE_TEMPLATES, {})[name] = tpl
        node = NodeTemplate(
            name,
            self,
            self.custom_defs,
            self.relationship_templates)
        node.validate(self)
        if get_relationships:
            # this will update the relationship_tpl of the target node
            # call after topology is complete
            node.relationships
        self.node_templates[name] = node
        return node

    def _relationship_templates(self):
        rel_templates = {}
        tpls = self._tpl_relationship_templates()
        for name in tpls:
            rel_templates[name] = RelationshipTemplate(tpls[name], name, self.custom_defs)
        return rel_templates

    def _outputs(self):
        outputs = []
        for name, attrs in self._tpl_outputs().items():
            output = Output(name, attrs, self.custom_defs)
            output.validate()
            outputs.append(output)
        return outputs

    def _substitution_mappings(self):
        tpl_substitution_mapping = self._tpl_substitution_mappings()
        if tpl_substitution_mapping:
            return SubstitutionMappings(tpl_substitution_mapping, self)

    def _do_substitutions(self, nested_topologies):
        # if a node template should be substituted, set its substitution
        remaining_topologies = [t for t in nested_topologies if t is not self]
        for nodetemplate in self.nodetemplates:
            if "substitute" not in nodetemplate.directives:
                continue
            for topology in remaining_topologies:
                mappings = topology.substitution_mappings
                if mappings.match(nodetemplate):
                    # the node template's properties treated as inputs
                    # create a new substitution mapping object for the mapped node
                    nodetemplate.substitution = mappings.substitute(nodetemplate, remaining_topologies)
                    break
            else:
                exception.ExceptionCollector.appendException(
                      exception.ValidationError(message=
                          'No substitute topology found for "%s"' % nodetemplate.name))

    def _policies(self):
        policies = []
        for policy in self._tpl_policies():
            for policy_name, policy_tpl in policy.items():
                target_list = policy_tpl.get('targets')
                target_objects = []
                targets_type = "groups"
                if target_list and len(target_list) >= 1:
                    target_objects = self._get_policy_groups(target_list)
                    if not target_objects:
                        targets_type = "node_templates"
                        target_objects = self._get_group_members(target_list)
                policyObj = Policy(policy_name, policy_tpl,
                                   target_objects, targets_type,
                                   self.custom_defs)
                # If the policyObj.type is defined in TOSCA_definition_1_0.yaml
                # or is defined as a custom definition, validate the properties
                # before adding it to the policies list.
                if (policyObj.type_definition and
                    (policyObj.type in policyObj.type_definition.TOSCA_DEF or
                     (policyObj.type not in policyObj.type_definition.TOSCA_DEF
                      and bool(policyObj.custom_def)))):
                    policyObj.validate()
                    policies.append(policyObj)
        return policies

    def _groups(self):
        groups = []
        member_nodes = None
        for group_name, group_tpl in self._tpl_groups().items():
            member_names = group_tpl.get('members')
            if member_names is not None:
                DataEntity.validate_datatype('list', member_names)
                if len(member_names) < 1 or \
                        len(member_names) != len(set(member_names)):
                    exception.ExceptionCollector.appendException(
                        exception.InvalidGroupTargetException(
                            message=_('Member nodes "%s" should be >= 1 '
                                      'and not repeated') % member_names))
                else:
                    member_nodes = self._get_group_members(member_names)
            group = Group(group_name, group_tpl,
                          member_nodes,
                          self.custom_defs)
            groups.append(group)
        return groups

    def _get_group_members(self, member_names):
        member_nodes = []
        self._validate_group_members(member_names)
        for member in member_names:
            for node in self.nodetemplates:
                if node.name == member:
                    member_nodes.append(node)
        return member_nodes

    def _get_policy_groups(self, member_names):
        member_groups = []
        for member in member_names:
            for group in self.groups:
                if group.name == member:
                    member_groups.append(group)
        return member_groups

    def _validate_group_members(self, members):
        for member in members:
            if member not in self._tpl_nodetemplates() and member not in self._tpl_groups():
                exception.ExceptionCollector.appendException(
                    exception.InvalidGroupTargetException(
                        message=_('Target member "%s" is not found in '
                                  'node_templates or groups') % member))

    def _workflows(self):
        workflows = {}
        for workflow_name, workflow_tpl in self._tpl_workflows().items():
            workflowObj = Workflow(workflow_name, workflow_tpl,
                               self.custom_defs)
            workflows[workflow_name] = workflowObj
        return workflows

    # topology template can act like node template
    # it is exposed by substitution_mappings.
    def nodetype(self):
        return self.substitution_mappings.node_type \
            if self.substitution_mappings else None

    def capabilities(self):
        return self.substitution_mappings.capabilities \
            if self.substitution_mappings else None

    def requirements(self):
        return self.substitution_mappings.requirements \
            if self.substitution_mappings else None

    def _tpl_description(self):
        description = self.tpl.get(DESCRIPTION)
        if description:
            return description.rstrip()

    def _tpl_inputs(self):
        inputs = self.tpl.get(INPUTS) or {}
        if not isinstance(inputs, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=INPUTS, type="dict"))
            return {}
        return inputs

    def _tpl_nodetemplates(self):
        nodetemplates = self.tpl.get(NODE_TEMPLATES)
        if nodetemplates and not isinstance(nodetemplates, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=NODE_TEMPLATES, type="dict"))
        return nodetemplates

    def _tpl_relationship_templates(self):
        relationship_templates = self.tpl.get(RELATIONSHIP_TEMPLATES) or {}
        if not isinstance(relationship_templates, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=RELATIONSHIP_TEMPLATES,
                                            type="dict"))
        return relationship_templates

    def _tpl_outputs(self):
        outputs = self.tpl.get(OUTPUTS) or {}
        if not isinstance(outputs, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=OUTPUTS, type="dict"))
        return outputs

    def _tpl_substitution_mappings(self):
        substitution_mappings = self.tpl.get(SUBSTITUION_MAPPINGS) or self.tpl.get(ROOT) or {}
        if not isinstance(substitution_mappings, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=SUBSTITUION_MAPPINGS,
                                            type="dict"))
        return substitution_mappings

    def _tpl_groups(self):
        groups = self.tpl.get(GROUPS) or {}
        if not isinstance(groups, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=GROUPS, type="dict"))
            return {}
        return groups

    def _tpl_policies(self):
        policies = self.tpl.get(POLICIES) or []
        if not isinstance(policies, list):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=POLICIES, type="list"))
        return policies

    def _tpl_workflows(self):
        workflows = self.tpl.get(WORKFLOWS) or {}
        if not isinstance(workflows, dict):
            exception.ExceptionCollector.appendException(
                exception.TypeMismatchError(what=WORKFLOWS, type="dict"))
        return workflows

    def _validate_field(self):
        for name in self.tpl:
            if name not in SECTIONS:
                exception.ExceptionCollector.appendException(
                    exception.UnknownFieldError(what='Template', field=name))

    def _process_intrinsic_functions(self):
        """Process intrinsic functions

        Current implementation processes functions within node template
        properties, requirements, interfaces inputs and template outputs.
        """
        if hasattr(self, 'nodetemplates'):
            for node_template in self.nodetemplates:
                for prop in node_template.get_properties_objects():
                    prop.value = functions.get_function(self,
                                                        node_template,
                                                        prop.value)

                for interface in node_template.interfaces:
                    if interface.inputs:
                        for name, value in interface.inputs.items():
                            interfacevalue =  functions.get_function(
                                self,
                                node_template,
                                value)
                            if isinstance(interfacevalue, functions.GetInput):
                               interface.inputs[name] = interfacevalue.result()

                if node_template.get_capabilities_objects():
                    for cap in node_template.get_capabilities_objects():
                        if cap.get_properties_objects():
                            for prop in cap.get_properties_objects():
                                propvalue = functions.get_function(
                                    self,
                                    node_template,
                                    prop.value)
                                # note: (throw exception if validation had failed)
                                if isinstance(propvalue, functions.GetInput):
                                    propvalue = propvalue.result()
                                    for p, v in cap._properties.items():
                                        if p == prop.name:
                                            cap._properties[p] = propvalue

                for rel_tpl, req, reqDef in node_template.relationships:
                    # XXX should use something like findProps to recursively validate properties
                    for prop in rel_tpl.get_properties_objects():
                        prop.value = functions.get_function(self, req, prop.value)
                    for interface in rel_tpl.interfaces:
                        if interface.inputs:
                            for name, value in interface.inputs.items():
                                interface.inputs[name] = functions.get_function(self,
                                                           rel_tpl,
                                                           value)

        for output in self.outputs:
            func = functions.get_function(self, self.outputs, output.value)
            if isinstance(func, functions.GetAttribute):
                output.attrs[output.VALUE] = func

    def _validate_intrinsic_functions(self):
        """Process intrinsic functions

        Current implementation processes functions within node template
        properties, requirements, interfaces inputs and template outputs.
        """
        if hasattr(self, 'nodetemplates'):
            for node_template in self.nodetemplates:
                ExceptionCollector.near = f' in node template "{node_template.name}"'
                # XXX should use something like findProps to recursively validate properties
                for prop in node_template.get_properties_objects():
                    functions.get_function(self,
                                                node_template,
                                                prop.value)
                for interface in node_template.interfaces:
                    if interface.inputs:
                        for name, value in interface.inputs.items():
                            functions.get_function(
                                self,
                                node_template,
                                value)
                if node_template.get_capabilities_objects():
                    for cap in node_template.get_capabilities_objects():
                        if cap.get_properties_objects():
                            for prop in cap.get_properties_objects():
                                functions.get_function(
                                    self,
                                    node_template,
                                    prop.value)

        for output in self.outputs:
            ExceptionCollector.near = f' in output "{output.name}"'
            functions.get_function(self, self.outputs, output.value)
        ExceptionCollector.near = ""

    def validate_relationships(self, strict):
        if not hasattr(self, 'nodetemplates'):
            return
        solve_topology = self.tosca_template and self.tosca_template.import_resolver and self.tosca_template.import_resolver.solve_topology
        if solve_topology:
            solve_topology(self)
        for node_template in self.nodetemplates:
            ExceptionCollector.near = f' in node template "{node_template.name}"'
            for rel_tpl, req, reqDef in node_template.relationships:
                # XXX should use something like findProps to recursively validate properties
                for prop in rel_tpl.get_properties_objects():
                    functions.get_function(self, req, prop.value)
                for interface in rel_tpl.interfaces:
                    if interface.inputs:
                        for name, value in interface.inputs.items():
                            functions.get_function(self,
                                                   rel_tpl,
                                                   value)

            if node_template.substitution:
                node_template.substitution.topology.validate_relationships(strict)
            elif strict:
                for name in node_template.missing_requirements:
                    msg = f'Required requirement "{name}" not defined'
                    ExceptionCollector.appendException(
                        ValidationError(message = msg))

    def find_node_related_template(self, name, namespace_id=None):
        node = self.node_templates.get(name)
        if not self.tosca_template:
            return node
        is_imported = self is not self.tosca_template.topology_template
        # if we check an imported topology and the node is marked as default or wasn't found
        if is_imported:
            if not node or (node and "default" in node.directives):
                # check the outermost topology
                match = self.tosca_template.topology_template.node_templates.get(name)
                if match:
                    return match
        if not node:
            if namespace_id:
                nested = self.tosca_template.find_topology_by_namespace_id(namespace_id)
                if nested:
                    # the type's namespace also has might have templates that it references
                    node = nested.node_templates.get(name)
                    if node:
                        return node
            # outermost templates can reference imported "default" templates
            for nested in self.tosca_template.nested_topologies.values():
                match = nested.node_templates.get(name)
                if match and "default" in match.directives:
                    return match
        return node

    def find_type(self, name: str, namespace_id=None):
        return find_type(name, self.custom_defs, namespace_id)

def find_type(typename: str, custom_defs, namespace_id=None):
    if isinstance(custom_defs, Namespace):
        if namespace_id:
            custom_defs = custom_defs.find_namespace(namespace_id)
        typedef = EntityType.find_type(typename, custom_defs)
    else:
        typedef = EntityType.find_type(typename)
    if typedef:
        return typedef

    ExceptionCollector.pause()
    try:
        # prefix is only used to expand "tosca:Type"
        test_typedef = StatefulEntityType(
            typename, StatefulEntityType.NODE_PREFIX, custom_defs
        )
    except Exception:
        return None
    finally:
        ExceptionCollector.resume()
    if not test_typedef.defs:
        return None

    if "derived_from" not in test_typedef.defs:
        _source = test_typedef.defs.get("_source")
        section = isinstance(_source, dict) and _source.get("section")
        if _source and not section:
            logging.warning(
                'Unable to determine type of %s: missing "derived_from" key',
                typename,
            )
        elif section == "node_types":
            custom_defs[typename]["derived_from"] = "tosca.nodes.Root"
        elif section == "relationship_types":
            custom_defs[typename]["derived_from"] = "tosca.relationships.Root"
    if test_typedef.is_derived_from("tosca.nodes.Root"):
        typedef = NodeType(typename, custom_defs)
    elif test_typedef.is_derived_from("tosca.relationships.Root"):
        typedef = RelationshipType(typename, custom_defs)
    elif test_typedef.is_derived_from("tosca.artifacts.Root"):
        typedef = ArtifactTypeDef(typename, custom_defs)
    else:
        typedef = test_typedef
    EntityType.add_type(typename, typedef)
    return typedef
