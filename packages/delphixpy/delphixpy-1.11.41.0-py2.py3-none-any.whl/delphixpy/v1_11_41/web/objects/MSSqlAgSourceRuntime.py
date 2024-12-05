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
#     /delphix-mssql-ag-source-runtime.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_41.web.objects.MSSqlBaseSourceRuntime import MSSqlBaseSourceRuntime
from delphixpy.v1_11_41 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlAgSourceRuntime(MSSqlBaseSourceRuntime):
    """
    *(extends* :py:class:`v1_11_41.web.vo.MSSqlBaseSourceRuntime` *)* Runtime
    (non-persistent) properties of a MSSQL AG Virtual source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlAgSourceRuntime", True)
        self._healthy_primary_host = (self.__undef__, True)
        self._healthy_secondary_host = (self.__undef__, True)
        self._last_fetched_duration_in_minutes = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._healthy_primary_host = (data.get("healthyPrimaryHost", obj.__undef__), dirty)
        if obj._healthy_primary_host[0] is not None and obj._healthy_primary_host[0] is not obj.__undef__:
            assert isinstance(obj._healthy_primary_host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._healthy_primary_host[0], type(obj._healthy_primary_host[0])))
            common.validate_format(obj._healthy_primary_host[0], "None", None, None)
        obj._healthy_secondary_host = (data.get("healthySecondaryHost", obj.__undef__), dirty)
        if obj._healthy_secondary_host[0] is not None and obj._healthy_secondary_host[0] is not obj.__undef__:
            assert isinstance(obj._healthy_secondary_host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._healthy_secondary_host[0], type(obj._healthy_secondary_host[0])))
            common.validate_format(obj._healthy_secondary_host[0], "None", None, None)
        obj._last_fetched_duration_in_minutes = (data.get("lastFetchedDurationInMinutes", obj.__undef__), dirty)
        if obj._last_fetched_duration_in_minutes[0] is not None and obj._last_fetched_duration_in_minutes[0] is not obj.__undef__:
            assert isinstance(obj._last_fetched_duration_in_minutes[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._last_fetched_duration_in_minutes[0], type(obj._last_fetched_duration_in_minutes[0])))
            common.validate_format(obj._last_fetched_duration_in_minutes[0], "None", None, None)
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
        if "healthy_primary_host" == "type" or (self.healthy_primary_host is not self.__undef__ and (not (dirty and not self._healthy_primary_host[1]))):
            dct["healthyPrimaryHost"] = dictify(self.healthy_primary_host)
        if "healthy_secondary_host" == "type" or (self.healthy_secondary_host is not self.__undef__ and (not (dirty and not self._healthy_secondary_host[1]))):
            dct["healthySecondaryHost"] = dictify(self.healthy_secondary_host)
        if "last_fetched_duration_in_minutes" == "type" or (self.last_fetched_duration_in_minutes is not self.__undef__ and (not (dirty and not self._last_fetched_duration_in_minutes[1]))):
            dct["lastFetchedDurationInMinutes"] = dictify(self.last_fetched_duration_in_minutes)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._healthy_primary_host = (self._healthy_primary_host[0], True)
        self._healthy_secondary_host = (self._healthy_secondary_host[0], True)
        self._last_fetched_duration_in_minutes = (self._last_fetched_duration_in_minutes[0], True)

    def is_dirty(self):
        return any([self._healthy_primary_host[1], self._healthy_secondary_host[1], self._last_fetched_duration_in_minutes[1]])

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
        if not isinstance(other, MSSqlAgSourceRuntime):
            return False
        return super().__eq__(other) and \
               self.healthy_primary_host == other.healthy_primary_host and \
               self.healthy_secondary_host == other.healthy_secondary_host and \
               self.last_fetched_duration_in_minutes == other.last_fetched_duration_in_minutes

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def healthy_primary_host(self):
        """
        Healthy primary host.

        :rtype: ``str``
        """
        return self._healthy_primary_host[0]

    @healthy_primary_host.setter
    def healthy_primary_host(self, value):
        self._healthy_primary_host = (value, True)

    @property
    def healthy_secondary_host(self):
        """
        Healthy secondary host.

        :rtype: ``str``
        """
        return self._healthy_secondary_host[0]

    @healthy_secondary_host.setter
    def healthy_secondary_host(self, value):
        self._healthy_secondary_host = (value, True)

    @property
    def last_fetched_duration_in_minutes(self):
        """
        Duration in minutes when the value last fetched.

        :rtype: ``int``
        """
        return self._last_fetched_duration_in_minutes[0]

    @last_fetched_duration_in_minutes.setter
    def last_fetched_duration_in_minutes(self, value):
        self._last_fetched_duration_in_minutes = (value, True)

