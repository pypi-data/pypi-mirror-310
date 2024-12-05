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
#     /delphix-js-weekly-operation-count.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.JSUsageData import JSUsageData
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSWeeklyOperationCount(JSUsageData):
    """
    *(extends* :py:class:`v1_11_32.web.vo.JSUsageData` *)* Information about
    the number of operations on a data container each week for up to 30 weeks.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSWeeklyOperationCount", True)
        self._weekly_count = (self.__undef__, True)
        self._weekly_duration = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._weekly_count = (data.get("weeklyCount", obj.__undef__), dirty)
        if obj._weekly_count[0] is not None and obj._weekly_count[0] is not obj.__undef__:
            assert isinstance(obj._weekly_count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._weekly_count[0], type(obj._weekly_count[0])))
            common.validate_format(obj._weekly_count[0], "None", None, None)
        obj._weekly_duration = (data.get("weeklyDuration", obj.__undef__), dirty)
        if obj._weekly_duration[0] is not None and obj._weekly_duration[0] is not obj.__undef__:
            assert isinstance(obj._weekly_duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._weekly_duration[0], type(obj._weekly_duration[0])))
            common.validate_format(obj._weekly_duration[0], "None", None, None)
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
        if "weekly_count" == "type" or (self.weekly_count is not self.__undef__ and (not (dirty and not self._weekly_count[1]))):
            dct["weeklyCount"] = dictify(self.weekly_count)
        if "weekly_duration" == "type" or (self.weekly_duration is not self.__undef__ and (not (dirty and not self._weekly_duration[1]))):
            dct["weeklyDuration"] = dictify(self.weekly_duration)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._weekly_count = (self._weekly_count[0], True)
        self._weekly_duration = (self._weekly_duration[0], True)

    def is_dirty(self):
        return any([self._weekly_count[1], self._weekly_duration[1]])

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
        if not isinstance(other, JSWeeklyOperationCount):
            return False
        return super().__eq__(other) and \
               self.weekly_count == other.weekly_count and \
               self.weekly_duration == other.weekly_duration

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def weekly_count(self):
        """
        The number of operations run against a data container in the specified
        week.

        :rtype: ``int``
        """
        return self._weekly_count[0]

    @weekly_count.setter
    def weekly_count(self, value):
        self._weekly_count = (value, True)

    @property
    def weekly_duration(self):
        """
        The total time spent in seconds running all operations during the
        specified week.

        :rtype: ``int``
        """
        return self._weekly_duration[0]

    @weekly_duration.setter
    def weekly_duration(self, value):
        self._weekly_duration = (value, True)

