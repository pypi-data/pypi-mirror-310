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
#     /delphix-js-daily-operation-duration.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.JSUsageData import JSUsageData
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSDailyOperationDuration(JSUsageData):
    """
    *(extends* :py:class:`v1_11_34.web.vo.JSUsageData` *)* Information about
    the durations of a specific operation type for a data container over the
    past week.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSDailyOperationDuration", True)
        self._operation = (self.__undef__, True)
        self._daily_count = (self.__undef__, True)
        self._daily_average_duration = (self.__undef__, True)
        self._daily_min_duration = (self.__undef__, True)
        self._daily_max_duration = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._operation = (data.get("operation", obj.__undef__), dirty)
        if obj._operation[0] is not None and obj._operation[0] is not obj.__undef__:
            assert isinstance(obj._operation[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._operation[0], type(obj._operation[0])))
            assert obj._operation[0] in ['REFRESH', 'RESET', 'CREATE_BRANCH', 'RESTORE', 'UNDO'], "Expected enum ['REFRESH', 'RESET', 'CREATE_BRANCH', 'RESTORE', 'UNDO'] but got %s" % obj._operation[0]
            common.validate_format(obj._operation[0], "None", None, None)
        obj._daily_count = (data.get("dailyCount", obj.__undef__), dirty)
        if obj._daily_count[0] is not None and obj._daily_count[0] is not obj.__undef__:
            assert isinstance(obj._daily_count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._daily_count[0], type(obj._daily_count[0])))
            common.validate_format(obj._daily_count[0], "None", None, None)
        obj._daily_average_duration = (data.get("dailyAverageDuration", obj.__undef__), dirty)
        if obj._daily_average_duration[0] is not None and obj._daily_average_duration[0] is not obj.__undef__:
            assert isinstance(obj._daily_average_duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._daily_average_duration[0], type(obj._daily_average_duration[0])))
            common.validate_format(obj._daily_average_duration[0], "None", None, None)
        obj._daily_min_duration = (data.get("dailyMinDuration", obj.__undef__), dirty)
        if obj._daily_min_duration[0] is not None and obj._daily_min_duration[0] is not obj.__undef__:
            assert isinstance(obj._daily_min_duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._daily_min_duration[0], type(obj._daily_min_duration[0])))
            common.validate_format(obj._daily_min_duration[0], "None", None, None)
        obj._daily_max_duration = (data.get("dailyMaxDuration", obj.__undef__), dirty)
        if obj._daily_max_duration[0] is not None and obj._daily_max_duration[0] is not obj.__undef__:
            assert isinstance(obj._daily_max_duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._daily_max_duration[0], type(obj._daily_max_duration[0])))
            common.validate_format(obj._daily_max_duration[0], "None", None, None)
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
        if "operation" == "type" or (self.operation is not self.__undef__ and (not (dirty and not self._operation[1]))):
            dct["operation"] = dictify(self.operation)
        if "daily_count" == "type" or (self.daily_count is not self.__undef__ and (not (dirty and not self._daily_count[1]))):
            dct["dailyCount"] = dictify(self.daily_count)
        if "daily_average_duration" == "type" or (self.daily_average_duration is not self.__undef__ and (not (dirty and not self._daily_average_duration[1]))):
            dct["dailyAverageDuration"] = dictify(self.daily_average_duration)
        if "daily_min_duration" == "type" or (self.daily_min_duration is not self.__undef__ and (not (dirty and not self._daily_min_duration[1]))):
            dct["dailyMinDuration"] = dictify(self.daily_min_duration)
        if "daily_max_duration" == "type" or (self.daily_max_duration is not self.__undef__ and (not (dirty and not self._daily_max_duration[1]))):
            dct["dailyMaxDuration"] = dictify(self.daily_max_duration)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._operation = (self._operation[0], True)
        self._daily_count = (self._daily_count[0], True)
        self._daily_average_duration = (self._daily_average_duration[0], True)
        self._daily_min_duration = (self._daily_min_duration[0], True)
        self._daily_max_duration = (self._daily_max_duration[0], True)

    def is_dirty(self):
        return any([self._operation[1], self._daily_count[1], self._daily_average_duration[1], self._daily_min_duration[1], self._daily_max_duration[1]])

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
        if not isinstance(other, JSDailyOperationDuration):
            return False
        return super().__eq__(other) and \
               self.operation == other.operation and \
               self.daily_count == other.daily_count and \
               self.daily_average_duration == other.daily_average_duration and \
               self.daily_min_duration == other.daily_min_duration and \
               self.daily_max_duration == other.daily_max_duration

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def operation(self):
        """
        The operation performed. *(permitted values: REFRESH, RESET,
        CREATE_BRANCH, RESTORE, UNDO)*

        :rtype: ``str``
        """
        return self._operation[0]

    @operation.setter
    def operation(self, value):
        self._operation = (value, True)

    @property
    def daily_count(self):
        """
        The number of times the specified operation was run in the past day.

        :rtype: ``int``
        """
        return self._daily_count[0]

    @daily_count.setter
    def daily_count(self, value):
        self._daily_count = (value, True)

    @property
    def daily_average_duration(self):
        """
        The average duration in seconds of running the specified operation in
        the past day.

        :rtype: ``int``
        """
        return self._daily_average_duration[0]

    @daily_average_duration.setter
    def daily_average_duration(self, value):
        self._daily_average_duration = (value, True)

    @property
    def daily_min_duration(self):
        """
        The minimum duration in seconds of running the specified operation in
        the past day.

        :rtype: ``int``
        """
        return self._daily_min_duration[0]

    @daily_min_duration.setter
    def daily_min_duration(self, value):
        self._daily_min_duration = (value, True)

    @property
    def daily_max_duration(self):
        """
        The maximum duration in seconds of running the specified operation in
        the past day.

        :rtype: ``int``
        """
        return self._daily_max_duration[0]

    @daily_max_duration.setter
    def daily_max_duration(self, value):
        self._daily_max_duration = (value, True)

