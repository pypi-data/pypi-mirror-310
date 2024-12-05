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
#     /delphix-schedule-policy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_17.web.objects.Policy import Policy
from delphixpy.v1_11_17 import factory
from delphixpy.v1_11_17 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SchedulePolicy(Policy):
    """
    *(extends* :py:class:`v1_11_17.web.vo.Policy` *)* The base type for all
    schedule policies.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SchedulePolicy", True)
        self._schedule_list = (self.__undef__, True)
        self._timezone = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._schedule_list = []
        for item in data.get("scheduleList") or []:
            obj._schedule_list.append(factory.create_object(item))
            factory.validate_type(obj._schedule_list[-1], "Schedule")
        obj._schedule_list = (obj._schedule_list, dirty)
        if "timezone" in data and data["timezone"] is not None:
            obj._timezone = (factory.create_object(data["timezone"], "TimeZone"), dirty)
            factory.validate_type(obj._timezone[0], "TimeZone")
        else:
            obj._timezone = (obj.__undef__, dirty)
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
        if "schedule_list" == "type" or (self.schedule_list is not self.__undef__ and (not (dirty and not self._schedule_list[1]) or self.is_dirty_list(self.schedule_list, self._schedule_list) or belongs_to_parent)):
            dct["scheduleList"] = dictify(self.schedule_list, prop_is_list_or_vo=True)
        if "timezone" == "type" or (self.timezone is not self.__undef__ and (not (dirty and not self._timezone[1]) or self.is_dirty_list(self.timezone, self._timezone) or belongs_to_parent)):
            dct["timezone"] = dictify(self.timezone, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._schedule_list = (self._schedule_list[0], True)
        self._timezone = (self._timezone[0], True)

    def is_dirty(self):
        return any([self._schedule_list[1], self._timezone[1]])

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
        if not isinstance(other, SchedulePolicy):
            return False
        return super().__eq__(other) and \
               self.schedule_list == other.schedule_list and \
               self.timezone == other.timezone

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def schedule_list(self):
        """
        List of Schedule objects representing when the policy will execute.

        :rtype: ``list`` of :py:class:`v1_11_17.web.vo.Schedule`
        """
        return self._schedule_list[0]

    @schedule_list.setter
    def schedule_list(self, value):
        self._schedule_list = (value, True)

    @property
    def timezone(self):
        """
        The timezone of this policy. If not specified, defaults to the Delphix
        Engine's timezone.

        :rtype: :py:class:`v1_11_17.web.vo.TimeZone`
        """
        return self._timezone[0]

    @timezone.setter
    def timezone(self, value):
        self._timezone = (value, True)

