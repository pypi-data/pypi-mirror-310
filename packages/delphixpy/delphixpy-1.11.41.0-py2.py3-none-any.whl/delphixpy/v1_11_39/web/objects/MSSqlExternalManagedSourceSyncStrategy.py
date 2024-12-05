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
#     /delphix-mssql-external-managed-source-sync-strategy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.MSSqlSourceSyncStrategy import MSSqlSourceSyncStrategy
from delphixpy.v1_11_39 import factory
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlExternalManagedSourceSyncStrategy(MSSqlSourceSyncStrategy):
    """
    *(extends* :py:class:`v1_11_39.web.vo.MSSqlSourceSyncStrategy` *)* MSSQL
    specific parameters for externally managed source based sync strategy.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlExternalManagedSourceSyncStrategy", True)
        self._config = (self.__undef__, True)
        self._validated_sync_mode = (self.__undef__, True)
        self._shared_backup_locations = (self.__undef__, True)
        self._mssql_netbackup_config = (self.__undef__, True)
        self._mssql_commvault_config = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._config = (data.get("config", obj.__undef__), dirty)
        if obj._config[0] is not None and obj._config[0] is not obj.__undef__:
            assert isinstance(obj._config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config[0], type(obj._config[0])))
            common.validate_format(obj._config[0], "objectReference", None, None)
        obj._validated_sync_mode = (data.get("validatedSyncMode", obj.__undef__), dirty)
        if obj._validated_sync_mode[0] is not None and obj._validated_sync_mode[0] is not obj.__undef__:
            assert isinstance(obj._validated_sync_mode[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._validated_sync_mode[0], type(obj._validated_sync_mode[0])))
            assert obj._validated_sync_mode[0] in ['TRANSACTION_LOG', 'FULL_OR_DIFFERENTIAL', 'FULL', 'NONE'], "Expected enum ['TRANSACTION_LOG', 'FULL_OR_DIFFERENTIAL', 'FULL', 'NONE'] but got %s" % obj._validated_sync_mode[0]
            common.validate_format(obj._validated_sync_mode[0], "None", None, None)
        obj._shared_backup_locations = []
        for item in data.get("sharedBackupLocations") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, 260)
            obj._shared_backup_locations.append(item)
        obj._shared_backup_locations = (obj._shared_backup_locations, dirty)
        if "mssqlNetbackupConfig" in data and data["mssqlNetbackupConfig"] is not None:
            obj._mssql_netbackup_config = (factory.create_object(data["mssqlNetbackupConfig"], "MSSqlNetbackupConfig"), dirty)
            factory.validate_type(obj._mssql_netbackup_config[0], "MSSqlNetbackupConfig")
        else:
            obj._mssql_netbackup_config = (obj.__undef__, dirty)
        if "mssqlCommvaultConfig" in data and data["mssqlCommvaultConfig"] is not None:
            obj._mssql_commvault_config = (factory.create_object(data["mssqlCommvaultConfig"], "MSSqlCommvaultConfig"), dirty)
            factory.validate_type(obj._mssql_commvault_config[0], "MSSqlCommvaultConfig")
        else:
            obj._mssql_commvault_config = (obj.__undef__, dirty)
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
        if "config" == "type" or (self.config is not self.__undef__ and (not (dirty and not self._config[1]) or self.is_dirty_list(self.config, self._config) or belongs_to_parent)):
            dct["config"] = dictify(self.config)
        if "validated_sync_mode" == "type" or (self.validated_sync_mode is not self.__undef__ and (not (dirty and not self._validated_sync_mode[1]) or self.is_dirty_list(self.validated_sync_mode, self._validated_sync_mode) or belongs_to_parent)):
            dct["validatedSyncMode"] = dictify(self.validated_sync_mode)
        elif belongs_to_parent and self.validated_sync_mode is self.__undef__:
            dct["validatedSyncMode"] = "TRANSACTION_LOG"
        if "shared_backup_locations" == "type" or (self.shared_backup_locations is not self.__undef__ and (not (dirty and not self._shared_backup_locations[1]) or self.is_dirty_list(self.shared_backup_locations, self._shared_backup_locations) or belongs_to_parent)):
            dct["sharedBackupLocations"] = dictify(self.shared_backup_locations, prop_is_list_or_vo=True)
        if "mssql_netbackup_config" == "type" or (self.mssql_netbackup_config is not self.__undef__ and (not (dirty and not self._mssql_netbackup_config[1]) or self.is_dirty_list(self.mssql_netbackup_config, self._mssql_netbackup_config) or belongs_to_parent)):
            dct["mssqlNetbackupConfig"] = dictify(self.mssql_netbackup_config)
        if "mssql_commvault_config" == "type" or (self.mssql_commvault_config is not self.__undef__ and (not (dirty and not self._mssql_commvault_config[1]) or self.is_dirty_list(self.mssql_commvault_config, self._mssql_commvault_config) or belongs_to_parent)):
            dct["mssqlCommvaultConfig"] = dictify(self.mssql_commvault_config)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._config = (self._config[0], True)
        self._validated_sync_mode = (self._validated_sync_mode[0], True)
        self._shared_backup_locations = (self._shared_backup_locations[0], True)
        self._mssql_netbackup_config = (self._mssql_netbackup_config[0], True)
        self._mssql_commvault_config = (self._mssql_commvault_config[0], True)

    def is_dirty(self):
        return any([self._config[1], self._validated_sync_mode[1], self._shared_backup_locations[1], self._mssql_netbackup_config[1], self._mssql_commvault_config[1]])

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
        if not isinstance(other, MSSqlExternalManagedSourceSyncStrategy):
            return False
        return super().__eq__(other) and \
               self.config == other.config and \
               self.validated_sync_mode == other.validated_sync_mode and \
               self.shared_backup_locations == other.shared_backup_locations and \
               self.mssql_netbackup_config == other.mssql_netbackup_config and \
               self.mssql_commvault_config == other.mssql_commvault_config

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def config(self):
        """
        Reference to the configuration for the source.

        :rtype: ``str``
        """
        return self._config[0]

    @config.setter
    def config(self, value):
        self._config = (value, True)

    @property
    def validated_sync_mode(self):
        """
        *(default value: TRANSACTION_LOG)* Specifies the backup types
        ValidatedSync will use to synchronize the dSource with the source
        database. *(permitted values: TRANSACTION_LOG, FULL_OR_DIFFERENTIAL,
        FULL, NONE)*

        :rtype: ``str``
        """
        return self._validated_sync_mode[0]

    @validated_sync_mode.setter
    def validated_sync_mode(self, value):
        self._validated_sync_mode = (value, True)

    @property
    def shared_backup_locations(self):
        """
        Shared source database backup locations.

        :rtype: ``list`` of ``str``
        """
        return self._shared_backup_locations[0]

    @shared_backup_locations.setter
    def shared_backup_locations(self, value):
        self._shared_backup_locations = (value, True)

    @property
    def mssql_netbackup_config(self):
        """
        Configuration for source that allows ingesting NetBackup backups for
        SQL Server.

        :rtype: :py:class:`v1_11_39.web.vo.MSSqlNetbackupConfig`
        """
        return self._mssql_netbackup_config[0]

    @mssql_netbackup_config.setter
    def mssql_netbackup_config(self, value):
        self._mssql_netbackup_config = (value, True)

    @property
    def mssql_commvault_config(self):
        """
        Configuration for source that allows ingesting Commvault backups for
        SQL Server.

        :rtype: :py:class:`v1_11_39.web.vo.MSSqlCommvaultConfig`
        """
        return self._mssql_commvault_config[0]

    @mssql_commvault_config.setter
    def mssql_commvault_config(self, value):
        self._mssql_commvault_config = (value, True)

