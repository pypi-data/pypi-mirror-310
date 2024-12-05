#
# Copyright 2024 by Delphix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This class has been automatically generated from:
#     /delphix-analytics-statistic-enum-axis.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.StatisticAxis import StatisticAxis
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StatisticEnumAxis(StatisticAxis):
    """
    *(extends* :py:class:`v1_11_27.web.vo.StatisticAxis` *)* The attributes of
    a statistic axis which is an enum type.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StatisticEnumAxis", True)
        self._enum_values = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enum_values = []
        for item in data.get("enumValues") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._enum_values.append(item)
        obj._enum_values = (obj._enum_values, dirty)
        return obj

    def to_dict(self, dirty=False, belongs_to_parent=False):
        dct = super().to_dict(dirty, belongs_to_parent)

        def dictify(obj, prop_is_list_or_vo=False):
            if isinstance(obj, list):
                return [dictify(o, prop_is_list_or_vo) for o in obj]
            elif hasattr(obj, "to_dict"):
                return obj.to_dict(dirty=dirty, belongs_to_parent=prop_is_list_or_vo)
            else:
                return obj
        if "enum_values" == "type" or (self.enum_values is not self.__undef__ and (not (dirty and not self._enum_values[1]))):
            dct["enumValues"] = dictify(self.enum_values)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enum_values = (self._enum_values[0], True)

    def is_dirty(self):
        return any([self._enum_values[1]])

    def is_dirty_list(self, prop_name, private_var):
        if isinstance(prop_name, list) and prop_name and hasattr(prop_name[0], 'type'):
            for item in prop_name:
                if isinstance(item, list):
                    if self.is_dirty_list(item) or item.is_dirty():
                        return True
                elif item.is_dirty():
                    return True
        else:
            return private_var[1]
        return False

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, StatisticEnumAxis):
            return False
        return super().__eq__(other) and \
               self.enum_values == other.enum_values

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enum_values(self):
        """
        The set of values that are allowed for this axis.

        :rtype: ``list`` of ``str``
        """
        return self._enum_values[0]

    @enum_values.setter
    def enum_values(self, value):
        self._enum_values = (value, True)

