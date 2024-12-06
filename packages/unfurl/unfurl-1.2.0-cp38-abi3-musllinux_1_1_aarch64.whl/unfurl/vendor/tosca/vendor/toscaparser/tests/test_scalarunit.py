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

from types import SimpleNamespace

import pytest
from toscaparser.common import exception
from toscaparser.elements.scalarunit import ScalarUnit_Frequency
from toscaparser.elements.scalarunit import ScalarUnit_Size
from toscaparser.elements.scalarunit import ScalarUnit_Time
from toscaparser.nodetemplate import NodeTemplate
from toscaparser.topology_template import TopologyTemplate
from toscaparser.tests.base import TestCase
from toscaparser.utils.gettextutils import _
from toscaparser.utils import yamlparser


@pytest.mark.parametrize(
    ["title", "self"],
 [
        (
            # tpl_snippet with mem_size given as number+space+MB
            'mem_size_is_number_Space_MB',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         mem_size: 1024 MB
                 ''',
                 property='mem_size',
                 expected='1024 MB')
        ),
        (
            # tpl_snippet with mem_size given as number+spaces+GB
            'mem_size_is_number_Space_GB',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         mem_size: 1     GB
                 ''',
                 property='mem_size',
                 expected='1 GB')
        ),
        (
            # tpl_snippet with mem_size given as number+tiB
            'mem_size_is_number_NoSpace_GB',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         mem_size: 1tiB
                 ''',
                 property='mem_size',
                 expected='1 TiB')
        ),
        (
            # tpl_snippet with mem_size given as number+Spaces+GIB
            'mem_size_is_number_Spaces_GB',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         mem_size: 1     GIB
                 ''',
                 property='mem_size',
                 expected='1 GiB')
        ),
        (
            # tpl_snippet with mem_size given as number+Space+tib
            'mem_size_is_number_Spaces_GB',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         mem_size: 1 tib
                 ''',
                 property='mem_size',
                 expected='1 TiB')
        ),
        (
            'cpu_frequency_is_float_Space_GHz',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         cpu_frequency: 2.5 GHz
                 ''',
                 property='cpu_frequency',
                 expected='2.5 GHz')
        ),
        (
            'cpu_frequency_is_float_Space_MHz',
            SimpleNamespace(tpl_snippet='''
                 server:
                   type: tosca.nodes.Compute
                   capabilities:
                     host:
                       properties:
                         cpu_frequency: 800 MHz
                 ''',
                 property='cpu_frequency',
                 expected='800 MHz')
        ),
    ])
def test_scenario_scalar_unit_positive(title, self):
    tpl = self.tpl_snippet
    nodetemplates = yamlparser.simple_parse(tpl)
    topology = TopologyTemplate({'node_templates':nodetemplates}, [])
    nodetemplate = NodeTemplate('server', topology)
    props = nodetemplate.get_capability('host').get_properties()
    prop_name = self.property
    if props and prop_name in props.keys():
        prop = props[prop_name]
        assert prop.validate() is None
        resolved = prop.value
    assert resolved == self.expected


@pytest.mark.parametrize(
    ["title", "self"],
 [
        (   # Note that (1 TB) / (1 GB) = 1000
            'Input is TB, user input is GB',
            SimpleNamespace(InputMemSize='1   TB',
                 UserInputUnit='gB',
                 expected=1000)
        ),
        (   # Note that (1 Tib)/ (1 GB) = 1099
            'Input is TiB, user input is GB',
            SimpleNamespace(InputMemSize='1   TiB',
                 UserInputUnit='gB',
                 expected=1099.511627776)
        ),
    ]   
)
def test_scenario_get_num_from_scalar_unit_size(title, self):
    resolved = (ScalarUnit_Size(self.InputMemSize).
                get_num_from_scalar_unit(self.UserInputUnit))
    assert resolved == self.expected


@pytest.mark.parametrize(
    ["title", "self"],
 [
        (   # Note that (1 GHz) / (1 Hz) = 1000000000
            'Input is GHz, user input is Hz',
            SimpleNamespace(InputMemSize='1   GHz',
                 UserInputUnit='Hz',
                 expected=1000000000)
        ),
        (
            'Input is GHz, user input is Hz',
            SimpleNamespace(InputMemSize='2.4   GHz',
                 UserInputUnit='Hz',
                 expected=2400000000)
        ),
        (   # Note that (1 GHz)/ (1 MHz) = 1000
            'Input is MHz, user input is GHz',
            SimpleNamespace(InputMemSize='800   MHz',
                 UserInputUnit='GHz',
                 expected=0.8)
        ),
        (
            'Input is GHz, user input is Hz',
            SimpleNamespace(InputMemSize='0.9  GHz',
                 UserInputUnit='MHz',
                 expected=900)
        ),
        (
            'Input is GHz, user input is Hz',
            SimpleNamespace(InputMemSize='2.7GHz',
                 UserInputUnit='MHz',
                 expected=2700)
        ),
    ]
)
def test_scenario_get_num_from_scalar_unit_frequency(title, self):
    resolved = (ScalarUnit_Frequency(self.InputMemSize).
                get_num_from_scalar_unit(self.UserInputUnit))
    assert resolved == self.expected


@pytest.mark.parametrize(
    ["title", "self"],
 [
        (   # Note that (1 s) / (1 ms) = 1000
            'Input is 500ms, user input is s',
            SimpleNamespace(InputMemSize='500   ms',
                 UserInputUnit='s',
                 expected=0.5)
        ),
        (   # Note that (1 h)/ (1 s) = 3600
            'Input is h, user input is s',
            SimpleNamespace(InputMemSize='1   h',
                 UserInputUnit='s',
                 expected=3600)
        ),
        (   # Note that (1 m)/ (1 s) = 60
            'Input is m, user input is s',
            SimpleNamespace(InputMemSize='0.5   m',
                 UserInputUnit='s',
                 expected=30)
        ),
        (   # Note that (1 d)/ (1 h) = 24
            'Input is d, user input is h',
            SimpleNamespace(InputMemSize='1   d',
                 UserInputUnit='h',
                 expected=24)
        ),
    ])
def test_scenario_get_num_from_scalar_unit_time(title, self):
    resolved = (ScalarUnit_Time(self.InputMemSize).
                get_num_from_scalar_unit(self.UserInputUnit))
    assert resolved == self.expected


class GetNumFromScalarUnitSizeNegative(TestCase):

    InputMemSize = '1 GB'
    UserInputUnit = 'qB'

    def test_get_num_from_scalar_unit_size_negative(self):
        try:
            (ScalarUnit_Size(self.InputMemSize).
             get_num_from_scalar_unit(self.UserInputUnit))
        except Exception as error:
            self.assertIsInstance(error, ValueError)
            self.assertEqual(_('The unit "qB" is not valid. Valid units are '
                               '"[\'B\', \'GB\', \'GiB\', \'KiB\', \'MB\', '
                               '\'MiB\', \'TB\', \'TiB\', \'kB\']".'),
                             error.__str__())


class GetNumFromScalarUnitFrequencyNegative(TestCase):

    InputFrequency = '2.7 GHz'
    UserInputUnit = 'Jz'

    def test_get_num_from_scalar_unit_frequency_negative(self):
        try:
            (ScalarUnit_Frequency(self.InputFrequency).
             get_num_from_scalar_unit(self.UserInputUnit))
        except Exception as error:
            self.assertIsInstance(error, ValueError)
            self.assertEqual(_('The unit "Jz" is not valid. Valid units are '
                               '"[\'GHz\', \'Hz\', \'MHz\', \'kHz\']".'),
                             error.__str__())


class GetNumFromScalarUnitTimeNegative(TestCase):

    InputTime = '5 ms'
    UserInputUnit = 'D'

    def test_get_num_from_scalar_unit_frequency_negative(self):
        try:
            (ScalarUnit_Time(self.InputTime).
             get_num_from_scalar_unit(self.UserInputUnit))
        except Exception as error:
            self.assertIsInstance(error, ValueError)
            self.assertEqual(_('"Jz" is not a valid scalar-unit.'),
                             error.__str__())


class ScalarUnitNegativeTest(TestCase):

    custom_def_snippet = '''
    tosca.my.nodes.Compute:
      derived_from: tosca.nodes.Root
      properties:
        cpu_frequency:
          required: false
          type: scalar-unit.frequency
          constraints:
            - greater_or_equal: 0.1 GHz
        disk_size:
          required: false
          type: scalar-unit.size
          constraints:
            - greater_or_equal: 1 GB
        mem_size:
          required: false
          type: scalar-unit.size
          constraints:
            - in_range: [1 MiB, 1 GiB]
    '''
    custom_def = yamlparser.simple_parse(custom_def_snippet)

    # disk_size doesn't provide a value, mem_size uses an invalid unit.
    def test_invalid_scalar_unit(self):
        tpl_snippet = '''
        server:
          type: tosca.my.nodes.Compute
          properties:
            cpu_frequency: 50.3.6 GHZ
            disk_size: MB
            mem_size: 1 QB
        '''
        nodetemplates = yamlparser.simple_parse(tpl_snippet)
        self.assertRaises(ValueError, lambda: TopologyTemplate({'node_templates':nodetemplates}, self.custom_def))

    # disk_size is less than 1 GB, mem_size is not in the required range.
    # Note: in the spec, the minimum value of mem_size is 1 MiB (> 1 MB)
    def test_constraint_for_scalar_unit(self):
        tpl_snippet = '''
        server:
          type: tosca.my.nodes.Compute
          properties:
            cpu_frequency: 0.05 GHz
            disk_size: 500 MB
            mem_size: 1 MB
        '''
        nodetemplates = yamlparser.simple_parse(tpl_snippet)
        self.assertRaises(exception.ValidationError, lambda: TopologyTemplate({'node_templates':nodetemplates}, self.custom_def))
        # XXX fix constraints
        # topology = TopologyTemplate({'node_templates':nodetemplates}, self.custom_def)
        # nodetemplate = NodeTemplate('server', topology, self.custom_def)
        # props = nodetemplate.get_properties()
        # if 'cpu_frequency' in props.keys():
        #     error = self.assertRaises(exception.ValidationError,
        #                               props['cpu_frequency'].validate)
        #     self.assertEqual(_('The value "0.05 GHz" of property '
        #                        '"cpu_frequency" must be greater than or equal '
        #                        'to "0.1 GHz".'), error.__str__())
        # if 'disk_size' in props.keys():
        #     error = self.assertRaises(exception.ValidationError,
        #                               props['disk_size'].validate)
        #     self.assertEqual(_('The value "500 MB" of property "disk_size" '
        #                        'must be greater than or equal to "1 GB".'),
        #                      error.__str__())
        #
        # if 'mem_size' in props.keys():
        #     error = self.assertRaises(exception.ValidationError,
        #                               props['mem_size'].validate)
        #     self.assertEqual(_('The value "1 MB" of property "mem_size" is '
        #                        'out of range "(min:1 MiB, max:1 GiB)".'),
        #                      error.__str__())

class ScalarDefaultUnitTest(TestCase):

    custom_def_snippet = '''
    tosca.my.nodes.Compute:
      derived_from: tosca.nodes.Root
      properties:
        disk_size:
          required: false
          type: scalar-unit.size
          metadata:
            default_unit: GB
    '''
    custom_def = yamlparser.simple_parse(custom_def_snippet)

    def test_invalid_scalar_unit(self):
        tpl_snippet = '''
        server:
          type: tosca.my.nodes.Compute
          properties:
            disk_size: 3
        '''
        nodetemplates = yamlparser.simple_parse(tpl_snippet)
        topology = TopologyTemplate({'node_templates':nodetemplates}, self.custom_def)
        nodetemplate = topology.node_templates["server"]
        assert nodetemplate
        self.assertEqual(nodetemplate.get_property_value('disk_size'), "3 GB")
