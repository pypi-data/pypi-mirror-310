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

from toscaparser.common.exception import ExceptionCollector
from toscaparser.common.exception import UnknownFieldError
from toscaparser.elements.statefulentitytype import StatefulEntityType


class RelationshipType(StatefulEntityType):
    '''TOSCA built-in relationship type.'''
    SECTIONS = (DERIVED_FROM, VALID_TARGET_TYPES, INTERFACES,
                ATTRIBUTES, PROPERTIES, DESCRIPTION, VERSION,
                CREDENTIAL, _SOURCE) = ('derived_from', 'valid_target_types',
                               'interfaces', 'attributes', 'properties',
                               'description', 'version', 'credential', '_source')

    SPECIAL_SECTIONS = (METADATA, NAME, TITLE, DESCRIPTION) = ('metadata', 'name', 'title', 'description')

    def __init__(self, type, custom_def=None):
        super(RelationshipType, self).__init__(type, self.RELATIONSHIP_PREFIX,
                                               custom_def)
        self.custom_def = custom_def
        if self.defs:
            self._validate_keys()

    @property
    def parent_type(self):
        '''Return that parent is RelationshipType that this is derived from.'''
        prel = self.derived_from(self.defs)
        if prel:
            return RelationshipType(prel, custom_def=self.custom_def)

    @property
    def valid_target_types(self):
        return self.get_value('valid_target_types', None, True) or []

    def _validate_keys(self):
        for key in self.defs.keys():
            if key not in self.SECTIONS and key not in self.SPECIAL_SECTIONS:
                ExceptionCollector.appendException(
                    UnknownFieldError(what='Relationshiptype "%s"' % self.type,
                                      field=key))
