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
#     /delphix-analytics-statistic-axis.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_13.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_13 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StatisticAxis(TypedObject):
    """
    *(extends* :py:class:`v1_11_13.web.vo.TypedObject` *)* The attributes of a
    statistic axis.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StatisticAxis", True)
        self._axis_name = (self.__undef__, True)
        self._explanation = (self.__undef__, True)
        self._constraint_type = (self.__undef__, True)
        self._value_type = (self.__undef__, True)
        self._stream_attribute = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._axis_name = (data.get("axisName", obj.__undef__), dirty)
        if obj._axis_name[0] is not None and obj._axis_name[0] is not obj.__undef__:
            assert isinstance(obj._axis_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._axis_name[0], type(obj._axis_name[0])))
            common.validate_format(obj._axis_name[0], "None", None, None)
        obj._explanation = (data.get("explanation", obj.__undef__), dirty)
        if obj._explanation[0] is not None and obj._explanation[0] is not obj.__undef__:
            assert isinstance(obj._explanation[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._explanation[0], type(obj._explanation[0])))
            common.validate_format(obj._explanation[0], "None", None, None)
        obj._constraint_type = (data.get("constraintType", obj.__undef__), dirty)
        if obj._constraint_type[0] is not None and obj._constraint_type[0] is not obj.__undef__:
            assert isinstance(obj._constraint_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._constraint_type[0], type(obj._constraint_type[0])))
            common.validate_format(obj._constraint_type[0], "None", None, None)
        obj._value_type = (data.get("valueType", obj.__undef__), dirty)
        if obj._value_type[0] is not None and obj._value_type[0] is not obj.__undef__:
            assert isinstance(obj._value_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._value_type[0], type(obj._value_type[0])))
            assert obj._value_type[0] in ['INTEGER', 'BOOLEAN', 'STRING', 'HISTOGRAM', 'AVERAGE'], "Expected enum ['INTEGER', 'BOOLEAN', 'STRING', 'HISTOGRAM', 'AVERAGE'] but got %s" % obj._value_type[0]
            common.validate_format(obj._value_type[0], "None", None, None)
        obj._stream_attribute = (data.get("streamAttribute", obj.__undef__), dirty)
        if obj._stream_attribute[0] is not None and obj._stream_attribute[0] is not obj.__undef__:
            assert isinstance(obj._stream_attribute[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._stream_attribute[0], type(obj._stream_attribute[0])))
            common.validate_format(obj._stream_attribute[0], "None", None, None)
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
        if "axis_name" == "type" or (self.axis_name is not self.__undef__ and (not (dirty and not self._axis_name[1]))):
            dct["axisName"] = dictify(self.axis_name)
        if "explanation" == "type" or (self.explanation is not self.__undef__ and (not (dirty and not self._explanation[1]))):
            dct["explanation"] = dictify(self.explanation)
        if "constraint_type" == "type" or (self.constraint_type is not self.__undef__ and (not (dirty and not self._constraint_type[1]))):
            dct["constraintType"] = dictify(self.constraint_type)
        if "value_type" == "type" or (self.value_type is not self.__undef__ and (not (dirty and not self._value_type[1]))):
            dct["valueType"] = dictify(self.value_type)
        if "stream_attribute" == "type" or (self.stream_attribute is not self.__undef__ and (not (dirty and not self._stream_attribute[1]))):
            dct["streamAttribute"] = dictify(self.stream_attribute)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._axis_name = (self._axis_name[0], True)
        self._explanation = (self._explanation[0], True)
        self._constraint_type = (self._constraint_type[0], True)
        self._value_type = (self._value_type[0], True)
        self._stream_attribute = (self._stream_attribute[0], True)

    def is_dirty(self):
        return any([self._axis_name[1], self._explanation[1], self._constraint_type[1], self._value_type[1], self._stream_attribute[1]])

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
        if not isinstance(other, StatisticAxis):
            return False
        return super().__eq__(other) and \
               self.axis_name == other.axis_name and \
               self.explanation == other.explanation and \
               self.constraint_type == other.constraint_type and \
               self.value_type == other.value_type and \
               self.stream_attribute == other.stream_attribute

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def axis_name(self):
        """
        The name for this axis.

        :rtype: ``str``
        """
        return self._axis_name[0]

    @axis_name.setter
    def axis_name(self, value):
        self._axis_name = (value, True)

    @property
    def explanation(self):
        """
        A deeper explanation of the data this corresponds to.

        :rtype: ``str``
        """
        return self._explanation[0]

    @explanation.setter
    def explanation(self, value):
        self._explanation = (value, True)

    @property
    def constraint_type(self):
        """
        The type of constraint that can be applied to this axis.

        :rtype: ``str``
        """
        return self._constraint_type[0]

    @constraint_type.setter
    def constraint_type(self, value):
        self._constraint_type = (value, True)

    @property
    def value_type(self):
        """
        The type of value this axis will have for collected data. *(permitted
        values: INTEGER, BOOLEAN, STRING, HISTOGRAM, AVERAGE)*

        :rtype: ``str``
        """
        return self._value_type[0]

    @value_type.setter
    def value_type(self, value):
        self._value_type = (value, True)

    @property
    def stream_attribute(self):
        """
        Whether this axis appears as an attribute of a datapoint stream or of
        datapoints themselves.

        :rtype: ``bool``
        """
        return self._stream_attribute[0]

    @stream_attribute.setter
    def stream_attribute(self, value):
        self._stream_attribute = (value, True)

