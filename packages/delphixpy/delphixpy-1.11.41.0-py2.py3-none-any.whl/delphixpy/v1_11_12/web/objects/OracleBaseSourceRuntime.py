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
#     /delphix-oracle-base-source-runtime.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_12.web.objects.SourceRuntime import SourceRuntime
from delphixpy.v1_11_12 import factory
from delphixpy.v1_11_12 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleBaseSourceRuntime(SourceRuntime):
    """
    *(extends* :py:class:`v1_11_12.web.vo.SourceRuntime` *)* Runtime (non-
    persistent) properties common to all Oracle sources.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleBaseSourceRuntime", True)
        self._database_mode = (self.__undef__, True)
        self._database_role = (self.__undef__, True)
        self._last_non_logged_location = (self.__undef__, True)
        self._active_instances = (self.__undef__, True)
        self._database_stats = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._database_mode = (data.get("databaseMode", obj.__undef__), dirty)
        if obj._database_mode[0] is not None and obj._database_mode[0] is not obj.__undef__:
            assert isinstance(obj._database_mode[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._database_mode[0], type(obj._database_mode[0])))
            assert obj._database_mode[0] in ['READ_WRITE', 'READ_ONLY', 'STANDBY_READ_ONLY', 'MOUNTED_ONLY', 'MIGRATE', 'UNKNOWN'], "Expected enum ['READ_WRITE', 'READ_ONLY', 'STANDBY_READ_ONLY', 'MOUNTED_ONLY', 'MIGRATE', 'UNKNOWN'] but got %s" % obj._database_mode[0]
            common.validate_format(obj._database_mode[0], "None", None, None)
        obj._database_role = (data.get("databaseRole", obj.__undef__), dirty)
        if obj._database_role[0] is not None and obj._database_role[0] is not obj.__undef__:
            assert isinstance(obj._database_role[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._database_role[0], type(obj._database_role[0])))
            assert obj._database_role[0] in ['PHYSICAL_STANDBY', 'LOGICAL_STANDBY', 'SNAPSHOT_STANDBY', 'FAR_SYNC', 'PRIMARY', 'UNKNOWN'], "Expected enum ['PHYSICAL_STANDBY', 'LOGICAL_STANDBY', 'SNAPSHOT_STANDBY', 'FAR_SYNC', 'PRIMARY', 'UNKNOWN'] but got %s" % obj._database_role[0]
            common.validate_format(obj._database_role[0], "None", None, None)
        obj._last_non_logged_location = (data.get("lastNonLoggedLocation", obj.__undef__), dirty)
        if obj._last_non_logged_location[0] is not None and obj._last_non_logged_location[0] is not obj.__undef__:
            assert isinstance(obj._last_non_logged_location[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_non_logged_location[0], type(obj._last_non_logged_location[0])))
            common.validate_format(obj._last_non_logged_location[0], "None", None, None)
        obj._active_instances = []
        for item in data.get("activeInstances") or []:
            obj._active_instances.append(factory.create_object(item))
            factory.validate_type(obj._active_instances[-1], "OracleActiveInstance")
        obj._active_instances = (obj._active_instances, dirty)
        obj._database_stats = []
        for item in data.get("databaseStats") or []:
            obj._database_stats.append(factory.create_object(item))
            factory.validate_type(obj._database_stats[-1], "OracleDatabaseStatsSection")
        obj._database_stats = (obj._database_stats, dirty)
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
        if "database_mode" == "type" or (self.database_mode is not self.__undef__ and (not (dirty and not self._database_mode[1]))):
            dct["databaseMode"] = dictify(self.database_mode)
        if "database_role" == "type" or (self.database_role is not self.__undef__ and (not (dirty and not self._database_role[1]))):
            dct["databaseRole"] = dictify(self.database_role)
        if "last_non_logged_location" == "type" or (self.last_non_logged_location is not self.__undef__ and (not (dirty and not self._last_non_logged_location[1]))):
            dct["lastNonLoggedLocation"] = dictify(self.last_non_logged_location)
        if "active_instances" == "type" or (self.active_instances is not self.__undef__ and (not (dirty and not self._active_instances[1]))):
            dct["activeInstances"] = dictify(self.active_instances)
        if "database_stats" == "type" or (self.database_stats is not self.__undef__ and (not (dirty and not self._database_stats[1]))):
            dct["databaseStats"] = dictify(self.database_stats)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._database_mode = (self._database_mode[0], True)
        self._database_role = (self._database_role[0], True)
        self._last_non_logged_location = (self._last_non_logged_location[0], True)
        self._active_instances = (self._active_instances[0], True)
        self._database_stats = (self._database_stats[0], True)

    def is_dirty(self):
        return any([self._database_mode[1], self._database_role[1], self._last_non_logged_location[1], self._active_instances[1], self._database_stats[1]])

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
        if not isinstance(other, OracleBaseSourceRuntime):
            return False
        return super().__eq__(other) and \
               self.database_mode == other.database_mode and \
               self.database_role == other.database_role and \
               self.last_non_logged_location == other.last_non_logged_location and \
               self.active_instances == other.active_instances and \
               self.database_stats == other.database_stats

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def database_mode(self):
        """
        *(default value: UNKNOWN)* Operating mode of the database. *(permitted
        values: READ_WRITE, READ_ONLY, STANDBY_READ_ONLY, MOUNTED_ONLY,
        MIGRATE, UNKNOWN)*

        :rtype: ``str``
        """
        return self._database_mode[0]

    @database_mode.setter
    def database_mode(self, value):
        self._database_mode = (value, True)

    @property
    def database_role(self):
        """
        *(default value: UNKNOWN)* The current role of the database.
        *(permitted values: PHYSICAL_STANDBY, LOGICAL_STANDBY,
        SNAPSHOT_STANDBY, FAR_SYNC, PRIMARY, UNKNOWN)*

        :rtype: ``str``
        """
        return self._database_role[0]

    @database_role.setter
    def database_role(self, value):
        self._database_role = (value, True)

    @property
    def last_non_logged_location(self):
        """
        Highest SCN at which non-logged changes were generated.

        :rtype: ``str``
        """
        return self._last_non_logged_location[0]

    @last_non_logged_location.setter
    def last_non_logged_location(self, value):
        self._last_non_logged_location = (value, True)

    @property
    def active_instances(self):
        """
        List of active database instances for the source.

        :rtype: ``list`` of :py:class:`v1_11_12.web.vo.OracleActiveInstance`
        """
        return self._active_instances[0]

    @active_instances.setter
    def active_instances(self, value):
        self._active_instances = (value, True)

    @property
    def database_stats(self):
        """
        Table of key database performance statistics.

        :rtype: ``list`` of
            :py:class:`v1_11_12.web.vo.OracleDatabaseStatsSection`
        """
        return self._database_stats[0]

    @database_stats.setter
    def database_stats(self, value):
        self._database_stats = (value, True)

