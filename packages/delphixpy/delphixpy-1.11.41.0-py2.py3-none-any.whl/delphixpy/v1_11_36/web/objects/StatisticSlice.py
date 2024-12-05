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
#     /delphix-analytics-statistic-slice.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_36 import factory
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StatisticSlice(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.NamedUserObject` *)* Collects a slice
    of a multidimensional analytics statistic.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StatisticSlice", True)
        self._statistic_type = (self.__undef__, True)
        self._collection_interval = (self.__undef__, True)
        self._state = (self.__undef__, True)
        self._collection_axes = (self.__undef__, True)
        self._axis_constraints = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._statistic_type = (data.get("statisticType", obj.__undef__), dirty)
        if obj._statistic_type[0] is not None and obj._statistic_type[0] is not obj.__undef__:
            assert isinstance(obj._statistic_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._statistic_type[0], type(obj._statistic_type[0])))
            common.validate_format(obj._statistic_type[0], "None", None, None)
        obj._collection_interval = (data.get("collectionInterval", obj.__undef__), dirty)
        if obj._collection_interval[0] is not None and obj._collection_interval[0] is not obj.__undef__:
            assert isinstance(obj._collection_interval[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._collection_interval[0], type(obj._collection_interval[0])))
            common.validate_format(obj._collection_interval[0], "None", None, None)
        obj._state = (data.get("state", obj.__undef__), dirty)
        if obj._state[0] is not None and obj._state[0] is not obj.__undef__:
            assert isinstance(obj._state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state[0], type(obj._state[0])))
            assert obj._state[0] in ['INITIALIZED', 'RUNNING', 'PAUSED', 'FAILED'], "Expected enum ['INITIALIZED', 'RUNNING', 'PAUSED', 'FAILED'] but got %s" % obj._state[0]
            common.validate_format(obj._state[0], "None", None, None)
        obj._collection_axes = []
        for item in data.get("collectionAxes") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._collection_axes.append(item)
        obj._collection_axes = (obj._collection_axes, dirty)
        obj._axis_constraints = []
        for item in data.get("axisConstraints") or []:
            obj._axis_constraints.append(factory.create_object(item))
            factory.validate_type(obj._axis_constraints[-1], "AxisConstraint")
        obj._axis_constraints = (obj._axis_constraints, dirty)
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
        if "statistic_type" == "type" or (self.statistic_type is not self.__undef__ and (not (dirty and not self._statistic_type[1]) or self.is_dirty_list(self.statistic_type, self._statistic_type) or belongs_to_parent)):
            dct["statisticType"] = dictify(self.statistic_type)
        if "collection_interval" == "type" or (self.collection_interval is not self.__undef__ and (not (dirty and not self._collection_interval[1]) or self.is_dirty_list(self.collection_interval, self._collection_interval) or belongs_to_parent)):
            dct["collectionInterval"] = dictify(self.collection_interval)
        if "state" == "type" or (self.state is not self.__undef__ and (not (dirty and not self._state[1]))):
            dct["state"] = dictify(self.state)
        if "collection_axes" == "type" or (self.collection_axes is not self.__undef__ and (not (dirty and not self._collection_axes[1]) or self.is_dirty_list(self.collection_axes, self._collection_axes) or belongs_to_parent)):
            dct["collectionAxes"] = dictify(self.collection_axes, prop_is_list_or_vo=True)
        if "axis_constraints" == "type" or (self.axis_constraints is not self.__undef__ and (not (dirty and not self._axis_constraints[1]) or self.is_dirty_list(self.axis_constraints, self._axis_constraints) or belongs_to_parent)):
            dct["axisConstraints"] = dictify(self.axis_constraints, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._statistic_type = (self._statistic_type[0], True)
        self._collection_interval = (self._collection_interval[0], True)
        self._state = (self._state[0], True)
        self._collection_axes = (self._collection_axes[0], True)
        self._axis_constraints = (self._axis_constraints[0], True)

    def is_dirty(self):
        return any([self._statistic_type[1], self._collection_interval[1], self._state[1], self._collection_axes[1], self._axis_constraints[1]])

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
        if not isinstance(other, StatisticSlice):
            return False
        return super().__eq__(other) and \
               self.statistic_type == other.statistic_type and \
               self.collection_interval == other.collection_interval and \
               self.state == other.state and \
               self.collection_axes == other.collection_axes and \
               self.axis_constraints == other.axis_constraints

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def statistic_type(self):
        """
        The type name for the data this can collect.

        :rtype: ``str``
        """
        return self._statistic_type[0]

    @statistic_type.setter
    def statistic_type(self, value):
        self._statistic_type = (value, True)

    @property
    def collection_interval(self):
        """
        The minimum interval between each reading for this statistic.

        :rtype: ``int``
        """
        return self._collection_interval[0]

    @collection_interval.setter
    def collection_interval(self, value):
        self._collection_interval = (value, True)

    @property
    def state(self):
        """
        Collection state of the slice. *(permitted values: INITIALIZED,
        RUNNING, PAUSED, FAILED)*

        :rtype: ``str``
        """
        return self._state[0]

    @state.setter
    def state(self, value):
        self._state = (value, True)

    @property
    def collection_axes(self):
        """
        The set of axes to collect (usually these are not constrained axes).

        :rtype: ``list`` of ``str``
        """
        return self._collection_axes[0]

    @collection_axes.setter
    def collection_axes(self, value):
        self._collection_axes = (value, True)

    @property
    def axis_constraints(self):
        """
        Axis constraints act as per-axis filters on data that is being
        collected.

        :rtype: ``list`` of :py:class:`v1_11_36.web.vo.AxisConstraint`
        """
        return self._axis_constraints[0]

    @axis_constraints.setter
    def axis_constraints(self, value):
        self._axis_constraints = (value, True)

