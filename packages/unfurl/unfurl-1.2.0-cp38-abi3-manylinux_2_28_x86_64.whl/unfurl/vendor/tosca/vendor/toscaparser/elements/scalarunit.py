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
import re

from toscaparser.common.exception import ExceptionCollector
from toscaparser.utils.gettextutils import _
from toscaparser.utils import validateutils

log = logging.getLogger('tosca')

scalar_pattern = re.compile(r'([0-9.]+)\s*(\w+)?')

class ScalarUnit(object):
    '''Parent class for scalar-unit type.'''

    SCALAR_UNIT_TYPES = (
        SCALAR_UNIT_SIZE, SCALAR_UNIT_FREQUENCY, SCALAR_UNIT_TIME, SCALAR_UNIT_BITRATE
    ) = (
        'scalar-unit.size', 'scalar-unit.frequency', 'scalar-unit.time', 'scalar-unit.bitrate'
    )

    def __init__(self, value):
        self.value = value

    @classmethod
    def _check_unit_in_scalar_standard_units(self, input_unit):
        """Check whether the input unit is following specified standard

        If unit is not following specified standard, convert it to standard
        unit after displaying a warning message.
        """
        if input_unit in self.SCALAR_UNIT_DICT.keys():
            return input_unit
        else:
            for key in self.SCALAR_UNIT_DICT.keys():
                if key.upper() == input_unit.upper():
                    # log.warning('The unit "%(unit)s" does not follow '
                    #             'scalar unit standards; using "%(key)s" '
                    #             'instead.' % {'unit': input_unit,
                    #                           'key': key})
                    return key
            msg = (_('The unit "%(unit)s" is not valid. Valid units are '
                     '"%(valid_units)s".') %
                   {'unit': input_unit,
                    'valid_units': sorted(self.SCALAR_UNIT_DICT.keys())})
            ExceptionCollector.appendException(ValueError(msg))

    def validate_scalar_unit(self):
        regex = scalar_pattern
        try:
            result = regex.match(str(self.value)).groups()
            validateutils.str_to_num(result[0])
            scalar_unit = self._check_unit_in_scalar_standard_units(result[1])
            self.value = ' '.join([result[0], scalar_unit])
            return self.value

        except Exception:
            ExceptionCollector.appendException(
                ValueError(_('"%s" is not a valid scalar-unit.')
                           % self.value))

    def get_num_from_scalar_unit(self, unit=None):
        if unit:
            unit = self._check_unit_in_scalar_standard_units(unit)
        else:
            unit = self.SCALAR_UNIT_DEFAULT
        self.validate_scalar_unit()

        match = scalar_pattern.match(str(self.value))
        if match:
            result = match.groups()
        else:
            return None

        if not result[1]:
            multiplier = self.SCALAR_UNIT_DICT[unit]
        else:
            multiplier = self.SCALAR_UNIT_DICT[result[1]]

        converted = (float(validateutils.str_to_num(result[0]))
                     * multiplier
                     / self.SCALAR_UNIT_DICT[unit])
        if converted - int(converted) < 0.0000000000001:
            converted = int(converted)
        return converted

    @classmethod
    def to_scalar(cls, value):
        "Find the closest unit"
        val = float(value)
        smallest_unit = cls.SCALAR_UNIT_UNITARY
        smallest_val = val / smallest_unit
        for unit, scale in cls.SCALAR_UNIT_DICT.items():
            if scale > val:
                continue
            scaled = val / scale
            if scaled < smallest_val:
                smallest_val = scaled
                smallest_unit = unit
        if smallest_val - int(smallest_val) < 0.0000000000001:
            smallest_val = int(smallest_val)
        if round(smallest_val, 4) > 0:
            smallest_val = round(smallest_val, 5)
        return str(smallest_val) + " " + smallest_unit


class ScalarUnit_Size(ScalarUnit):

    SCALAR_UNIT_DEFAULT = 'B'
    SCALAR_UNIT_UNITARY = 'B'
    SCALAR_UNIT_DICT = {'B': 1, 'kB': 1000, 'KiB': 1024, 'MB': 1000000,
                        'MiB': 1048576, 'GB': 1000000000,
                        'GiB': 1073741824, 'TB': 1000000000000,
                        'TiB': 1099511627776}


class ScalarUnit_Time(ScalarUnit):

    SCALAR_UNIT_DEFAULT = 's'
    SCALAR_UNIT_UNITARY = 's'
    SCALAR_UNIT_DICT = {'d': 86400, 'h': 3600, 'm': 60, 's': 1,
                        'ms': 0.001, 'us': 0.000001, 'ns': 0.000000001}


class ScalarUnit_Frequency(ScalarUnit):

    SCALAR_UNIT_DEFAULT = 'GHz'
    SCALAR_UNIT_UNITARY = 'Hz'
    SCALAR_UNIT_DICT = {'Hz': 1, 'kHz': 1000,
                        'MHz': 1000000, 'GHz': 1000000000}


class ScalarUnit_Bitrate(ScalarUnit):

    SCALAR_UNIT_DEFAULT = 'bps'
    SCALAR_UNIT_UNITARY = 'bps'
    SCALAR_UNIT_DICT = {'bps': 1, 'Kbps': 1000, 'Kibps': 1024, 'Mbps': 1000000,
                        'Mibps': 1048576, 'Gbps': 1000000000,
                        'Gibps': 1073741824, 'Tbps': 1000000000000,
                        'Tibps': 1099511627776}


scalarunit_mapping = {
    ScalarUnit.SCALAR_UNIT_FREQUENCY: ScalarUnit_Frequency,
    ScalarUnit.SCALAR_UNIT_SIZE: ScalarUnit_Size,
    ScalarUnit.SCALAR_UNIT_TIME: ScalarUnit_Time,
    ScalarUnit.SCALAR_UNIT_BITRATE: ScalarUnit_Bitrate,
}


def get_scalarunit_class(type):
    return scalarunit_mapping.get(type)


def get_scalarunit_value(type, value, unit=None):
    if type in ScalarUnit.SCALAR_UNIT_TYPES:
        ScalarUnit_Class = get_scalarunit_class(type)
        return ScalarUnit_Class(value).get_num_from_scalar_unit(unit)
    else:
        ExceptionCollector.appendException(
            TypeError(_('"%s" is not a valid scalar-unit type.') % type))


def scalar_type_from_unit(unit):
    for scalar_cls in [ScalarUnit_Size, ScalarUnit_Time, ScalarUnit_Frequency, ScalarUnit_Bitrate]:
        for name in scalar_cls.SCALAR_UNIT_DICT:
            if name.lower() == unit.lower():
                return 'scalar-unit.' + scalar_cls.__name__[len("ScalarUnit_"):].lower()
    return ""
