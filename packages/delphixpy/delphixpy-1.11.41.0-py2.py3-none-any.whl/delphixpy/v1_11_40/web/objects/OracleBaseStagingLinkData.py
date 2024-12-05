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
#     /delphix-oracle-base-staging-link-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.OracleBaseLinkData import OracleBaseLinkData
from delphixpy.v1_11_40 import factory
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleBaseStagingLinkData(OracleBaseLinkData):
    """
    *(extends* :py:class:`v1_11_40.web.vo.OracleBaseLinkData` *)* Represents
    common parameters to link an Oracle database using a staging database.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleBaseStagingLinkData", True)
        self._sync_strategy = (self.__undef__, True)
        self._allow_auto_staging_restart_on_host_reboot = (self.__undef__, True)
        self._sync_parameters = (self.__undef__, True)
        self._custom_env_vars = (self.__undef__, True)
        self._sourcing_policy = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "syncStrategy" in data and data["syncStrategy"] is not None:
            obj._sync_strategy = (factory.create_object(data["syncStrategy"], "OracleSourceLessSyncStrategy"), dirty)
            factory.validate_type(obj._sync_strategy[0], "OracleSourceLessSyncStrategy")
        else:
            obj._sync_strategy = (obj.__undef__, dirty)
        obj._allow_auto_staging_restart_on_host_reboot = (data.get("allowAutoStagingRestartOnHostReboot", obj.__undef__), dirty)
        if obj._allow_auto_staging_restart_on_host_reboot[0] is not None and obj._allow_auto_staging_restart_on_host_reboot[0] is not obj.__undef__:
            assert isinstance(obj._allow_auto_staging_restart_on_host_reboot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._allow_auto_staging_restart_on_host_reboot[0], type(obj._allow_auto_staging_restart_on_host_reboot[0])))
            common.validate_format(obj._allow_auto_staging_restart_on_host_reboot[0], "None", None, None)
        if "syncParameters" in data and data["syncParameters"] is not None:
            obj._sync_parameters = (factory.create_object(data["syncParameters"], "OracleSyncFromStagingParameters"), dirty)
            factory.validate_type(obj._sync_parameters[0], "OracleSyncFromStagingParameters")
        else:
            obj._sync_parameters = (obj.__undef__, dirty)
        obj._custom_env_vars = []
        for item in data.get("customEnvVars") or []:
            obj._custom_env_vars.append(factory.create_object(item))
            factory.validate_type(obj._custom_env_vars[-1], "OracleCustomEnvVar")
        obj._custom_env_vars = (obj._custom_env_vars, dirty)
        if "sourcingPolicy" in data and data["sourcingPolicy"] is not None:
            obj._sourcing_policy = (factory.create_object(data["sourcingPolicy"], "OracleStagingSourcingPolicy"), dirty)
            factory.validate_type(obj._sourcing_policy[0], "OracleStagingSourcingPolicy")
        else:
            obj._sourcing_policy = (obj.__undef__, dirty)
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
        if "sync_strategy" == "type" or (self.sync_strategy is not self.__undef__ and (not (dirty and not self._sync_strategy[1]) or self.is_dirty_list(self.sync_strategy, self._sync_strategy) or belongs_to_parent)):
            dct["syncStrategy"] = dictify(self.sync_strategy, prop_is_list_or_vo=True)
        if "allow_auto_staging_restart_on_host_reboot" == "type" or (self.allow_auto_staging_restart_on_host_reboot is not self.__undef__ and (not (dirty and not self._allow_auto_staging_restart_on_host_reboot[1]) or self.is_dirty_list(self.allow_auto_staging_restart_on_host_reboot, self._allow_auto_staging_restart_on_host_reboot) or belongs_to_parent)):
            dct["allowAutoStagingRestartOnHostReboot"] = dictify(self.allow_auto_staging_restart_on_host_reboot)
        if "sync_parameters" == "type" or (self.sync_parameters is not self.__undef__ and (not (dirty and not self._sync_parameters[1]) or self.is_dirty_list(self.sync_parameters, self._sync_parameters) or belongs_to_parent)):
            dct["syncParameters"] = dictify(self.sync_parameters, prop_is_list_or_vo=True)
        if "custom_env_vars" == "type" or (self.custom_env_vars is not self.__undef__ and (not (dirty and not self._custom_env_vars[1]) or self.is_dirty_list(self.custom_env_vars, self._custom_env_vars) or belongs_to_parent)):
            dct["customEnvVars"] = dictify(self.custom_env_vars, prop_is_list_or_vo=True)
        if "sourcing_policy" == "type" or (self.sourcing_policy is not self.__undef__ and (not (dirty and not self._sourcing_policy[1]) or self.is_dirty_list(self.sourcing_policy, self._sourcing_policy) or belongs_to_parent)):
            dct["sourcingPolicy"] = dictify(self.sourcing_policy, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._sync_strategy = (self._sync_strategy[0], True)
        self._allow_auto_staging_restart_on_host_reboot = (self._allow_auto_staging_restart_on_host_reboot[0], True)
        self._sync_parameters = (self._sync_parameters[0], True)
        self._custom_env_vars = (self._custom_env_vars[0], True)
        self._sourcing_policy = (self._sourcing_policy[0], True)

    def is_dirty(self):
        return any([self._sync_strategy[1], self._allow_auto_staging_restart_on_host_reboot[1], self._sync_parameters[1], self._custom_env_vars[1], self._sourcing_policy[1]])

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
        if not isinstance(other, OracleBaseStagingLinkData):
            return False
        return super().__eq__(other) and \
               self.sync_strategy == other.sync_strategy and \
               self.allow_auto_staging_restart_on_host_reboot == other.allow_auto_staging_restart_on_host_reboot and \
               self.sync_parameters == other.sync_parameters and \
               self.custom_env_vars == other.custom_env_vars and \
               self.sourcing_policy == other.sourcing_policy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def sync_strategy(self):
        """
        Persistent parameters to sync the container.

        :rtype: :py:class:`v1_11_40.web.vo.OracleSourceLessSyncStrategy`
        """
        return self._sync_strategy[0]

    @sync_strategy.setter
    def sync_strategy(self, value):
        self._sync_strategy = (value, True)

    @property
    def allow_auto_staging_restart_on_host_reboot(self):
        """
        Indicates whether Delphix should automatically restart this staging
        database when staging host reboot is detected.

        :rtype: ``bool``
        """
        return self._allow_auto_staging_restart_on_host_reboot[0]

    @allow_auto_staging_restart_on_host_reboot.setter
    def allow_auto_staging_restart_on_host_reboot(self, value):
        self._allow_auto_staging_restart_on_host_reboot = (value, True)

    @property
    def sync_parameters(self):
        """
        Parameters used to initially sync the database.

        :rtype: :py:class:`v1_11_40.web.vo.OracleSyncFromStagingParameters`
        """
        return self._sync_parameters[0]

    @sync_parameters.setter
    def sync_parameters(self, value):
        self._sync_parameters = (value, True)

    @property
    def custom_env_vars(self):
        """
        Custom environment variables for Oracle databases.

        :rtype: ``list`` of :py:class:`v1_11_40.web.vo.OracleCustomEnvVar`
        """
        return self._custom_env_vars[0]

    @custom_env_vars.setter
    def custom_env_vars(self, value):
        self._custom_env_vars = (value, True)

    @property
    def sourcing_policy(self):
        """
        Policies for managing LogSync for staging sources.

        :rtype: :py:class:`v1_11_40.web.vo.OracleStagingSourcingPolicy`
        """
        return self._sourcing_policy[0]

    @sourcing_policy.setter
    def sourcing_policy(self, value):
        self._sourcing_policy = (value, True)

