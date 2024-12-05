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
#     /delphix-mssql-attach-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_7.web.objects.AttachData import AttachData
from delphixpy.v1_11_7 import factory
from delphixpy.v1_11_7 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlAttachData(AttachData):
    """
    *(extends* :py:class:`v1_11_7.web.vo.AttachData` *)* Represents the MSSQL
    specific parameters of an attach request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlAttachData", True)
        self._config = (self.__undef__, True)
        self._external_file_path = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._shared_backup_locations = (self.__undef__, True)
        self._backup_location_user = (self.__undef__, True)
        self._backup_location_credentials = (self.__undef__, True)
        self._encryption_key = (self.__undef__, True)
        self._source_host_user = (self.__undef__, True)
        self._mssql_user = (self.__undef__, True)
        self._ppt_repository = (self.__undef__, True)
        self._ppt_host_user = (self.__undef__, True)
        self._staging_pre_script = (self.__undef__, True)
        self._staging_post_script = (self.__undef__, True)
        self._ingestion_strategy = (self.__undef__, True)
        self._mssql_netbackup_config = (self.__undef__, True)
        self._mssql_commvault_config = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "config" not in data:
            raise ValueError("Missing required property \"config\".")
        obj._config = (data.get("config", obj.__undef__), dirty)
        if obj._config[0] is not None and obj._config[0] is not obj.__undef__:
            assert isinstance(obj._config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config[0], type(obj._config[0])))
            common.validate_format(obj._config[0], "objectReference", None, None)
        obj._external_file_path = (data.get("externalFilePath", obj.__undef__), dirty)
        if obj._external_file_path[0] is not None and obj._external_file_path[0] is not obj.__undef__:
            assert isinstance(obj._external_file_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._external_file_path[0], type(obj._external_file_path[0])))
            common.validate_format(obj._external_file_path[0], "None", None, 1024)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "LinkedSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "LinkedSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        obj._shared_backup_locations = []
        for item in data.get("sharedBackupLocations") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, 260)
            obj._shared_backup_locations.append(item)
        obj._shared_backup_locations = (obj._shared_backup_locations, dirty)
        obj._backup_location_user = (data.get("backupLocationUser", obj.__undef__), dirty)
        if obj._backup_location_user[0] is not None and obj._backup_location_user[0] is not obj.__undef__:
            assert isinstance(obj._backup_location_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._backup_location_user[0], type(obj._backup_location_user[0])))
            common.validate_format(obj._backup_location_user[0], "None", None, 256)
        if "backupLocationCredentials" in data and data["backupLocationCredentials"] is not None:
            obj._backup_location_credentials = (factory.create_object(data["backupLocationCredentials"], "PasswordCredential"), dirty)
            factory.validate_type(obj._backup_location_credentials[0], "PasswordCredential")
        else:
            obj._backup_location_credentials = (obj.__undef__, dirty)
        obj._encryption_key = (data.get("encryptionKey", obj.__undef__), dirty)
        if obj._encryption_key[0] is not None and obj._encryption_key[0] is not obj.__undef__:
            assert isinstance(obj._encryption_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._encryption_key[0], type(obj._encryption_key[0])))
            common.validate_format(obj._encryption_key[0], "None", None, None)
        obj._source_host_user = (data.get("sourceHostUser", obj.__undef__), dirty)
        if obj._source_host_user[0] is not None and obj._source_host_user[0] is not obj.__undef__:
            assert isinstance(obj._source_host_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source_host_user[0], type(obj._source_host_user[0])))
            common.validate_format(obj._source_host_user[0], "objectReference", None, None)
        if "mssqlUser" not in data:
            raise ValueError("Missing required property \"mssqlUser\".")
        if "mssqlUser" in data and data["mssqlUser"] is not None:
            obj._mssql_user = (factory.create_object(data["mssqlUser"], "MSSqlUser"), dirty)
            factory.validate_type(obj._mssql_user[0], "MSSqlUser")
        else:
            obj._mssql_user = (obj.__undef__, dirty)
        if "pptRepository" not in data:
            raise ValueError("Missing required property \"pptRepository\".")
        obj._ppt_repository = (data.get("pptRepository", obj.__undef__), dirty)
        if obj._ppt_repository[0] is not None and obj._ppt_repository[0] is not obj.__undef__:
            assert isinstance(obj._ppt_repository[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ppt_repository[0], type(obj._ppt_repository[0])))
            common.validate_format(obj._ppt_repository[0], "objectReference", None, None)
        obj._ppt_host_user = (data.get("pptHostUser", obj.__undef__), dirty)
        if obj._ppt_host_user[0] is not None and obj._ppt_host_user[0] is not obj.__undef__:
            assert isinstance(obj._ppt_host_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ppt_host_user[0], type(obj._ppt_host_user[0])))
            common.validate_format(obj._ppt_host_user[0], "objectReference", None, None)
        obj._staging_pre_script = (data.get("stagingPreScript", obj.__undef__), dirty)
        if obj._staging_pre_script[0] is not None and obj._staging_pre_script[0] is not obj.__undef__:
            assert isinstance(obj._staging_pre_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_pre_script[0], type(obj._staging_pre_script[0])))
            common.validate_format(obj._staging_pre_script[0], "None", None, 1024)
        obj._staging_post_script = (data.get("stagingPostScript", obj.__undef__), dirty)
        if obj._staging_post_script[0] is not None and obj._staging_post_script[0] is not obj.__undef__:
            assert isinstance(obj._staging_post_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_post_script[0], type(obj._staging_post_script[0])))
            common.validate_format(obj._staging_post_script[0], "None", None, 1024)
        if "ingestionStrategy" in data and data["ingestionStrategy"] is not None:
            obj._ingestion_strategy = (factory.create_object(data["ingestionStrategy"], "IngestionStrategy"), dirty)
            factory.validate_type(obj._ingestion_strategy[0], "IngestionStrategy")
        else:
            obj._ingestion_strategy = (obj.__undef__, dirty)
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
        if "external_file_path" == "type" or (self.external_file_path is not self.__undef__ and (not (dirty and not self._external_file_path[1]) or self.is_dirty_list(self.external_file_path, self._external_file_path) or belongs_to_parent)):
            dct["externalFilePath"] = dictify(self.external_file_path)
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "shared_backup_locations" == "type" or (self.shared_backup_locations is not self.__undef__ and (not (dirty and not self._shared_backup_locations[1]) or self.is_dirty_list(self.shared_backup_locations, self._shared_backup_locations) or belongs_to_parent)):
            dct["sharedBackupLocations"] = dictify(self.shared_backup_locations, prop_is_list_or_vo=True)
        if "backup_location_user" == "type" or (self.backup_location_user is not self.__undef__ and (not (dirty and not self._backup_location_user[1]) or self.is_dirty_list(self.backup_location_user, self._backup_location_user) or belongs_to_parent)):
            dct["backupLocationUser"] = dictify(self.backup_location_user)
        if "backup_location_credentials" == "type" or (self.backup_location_credentials is not self.__undef__ and (not (dirty and not self._backup_location_credentials[1]) or self.is_dirty_list(self.backup_location_credentials, self._backup_location_credentials) or belongs_to_parent)):
            dct["backupLocationCredentials"] = dictify(self.backup_location_credentials, prop_is_list_or_vo=True)
        if "encryption_key" == "type" or (self.encryption_key is not self.__undef__ and (not (dirty and not self._encryption_key[1]) or self.is_dirty_list(self.encryption_key, self._encryption_key) or belongs_to_parent)):
            dct["encryptionKey"] = dictify(self.encryption_key)
        if "source_host_user" == "type" or (self.source_host_user is not self.__undef__ and (not (dirty and not self._source_host_user[1]) or self.is_dirty_list(self.source_host_user, self._source_host_user) or belongs_to_parent)):
            dct["sourceHostUser"] = dictify(self.source_host_user)
        if "mssql_user" == "type" or (self.mssql_user is not self.__undef__ and (not (dirty and not self._mssql_user[1]) or self.is_dirty_list(self.mssql_user, self._mssql_user) or belongs_to_parent)):
            dct["mssqlUser"] = dictify(self.mssql_user, prop_is_list_or_vo=True)
        if "ppt_repository" == "type" or (self.ppt_repository is not self.__undef__ and (not (dirty and not self._ppt_repository[1]) or self.is_dirty_list(self.ppt_repository, self._ppt_repository) or belongs_to_parent)):
            dct["pptRepository"] = dictify(self.ppt_repository)
        if "ppt_host_user" == "type" or (self.ppt_host_user is not self.__undef__ and (not (dirty and not self._ppt_host_user[1]) or self.is_dirty_list(self.ppt_host_user, self._ppt_host_user) or belongs_to_parent)):
            dct["pptHostUser"] = dictify(self.ppt_host_user)
        if "staging_pre_script" == "type" or (self.staging_pre_script is not self.__undef__ and (not (dirty and not self._staging_pre_script[1]) or self.is_dirty_list(self.staging_pre_script, self._staging_pre_script) or belongs_to_parent)):
            dct["stagingPreScript"] = dictify(self.staging_pre_script)
        if "staging_post_script" == "type" or (self.staging_post_script is not self.__undef__ and (not (dirty and not self._staging_post_script[1]) or self.is_dirty_list(self.staging_post_script, self._staging_post_script) or belongs_to_parent)):
            dct["stagingPostScript"] = dictify(self.staging_post_script)
        if "ingestion_strategy" == "type" or (self.ingestion_strategy is not self.__undef__ and (not (dirty and not self._ingestion_strategy[1]) or self.is_dirty_list(self.ingestion_strategy, self._ingestion_strategy) or belongs_to_parent)):
            dct["ingestionStrategy"] = dictify(self.ingestion_strategy, prop_is_list_or_vo=True)
        if "mssql_netbackup_config" == "type" or (self.mssql_netbackup_config is not self.__undef__ and (not (dirty and not self._mssql_netbackup_config[1]) or self.is_dirty_list(self.mssql_netbackup_config, self._mssql_netbackup_config) or belongs_to_parent)):
            dct["mssqlNetbackupConfig"] = dictify(self.mssql_netbackup_config)
        if "mssql_commvault_config" == "type" or (self.mssql_commvault_config is not self.__undef__ and (not (dirty and not self._mssql_commvault_config[1]) or self.is_dirty_list(self.mssql_commvault_config, self._mssql_commvault_config) or belongs_to_parent)):
            dct["mssqlCommvaultConfig"] = dictify(self.mssql_commvault_config)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._config = (self._config[0], True)
        self._external_file_path = (self._external_file_path[0], True)
        self._operations = (self._operations[0], True)
        self._shared_backup_locations = (self._shared_backup_locations[0], True)
        self._backup_location_user = (self._backup_location_user[0], True)
        self._backup_location_credentials = (self._backup_location_credentials[0], True)
        self._encryption_key = (self._encryption_key[0], True)
        self._source_host_user = (self._source_host_user[0], True)
        self._mssql_user = (self._mssql_user[0], True)
        self._ppt_repository = (self._ppt_repository[0], True)
        self._ppt_host_user = (self._ppt_host_user[0], True)
        self._staging_pre_script = (self._staging_pre_script[0], True)
        self._staging_post_script = (self._staging_post_script[0], True)
        self._ingestion_strategy = (self._ingestion_strategy[0], True)
        self._mssql_netbackup_config = (self._mssql_netbackup_config[0], True)
        self._mssql_commvault_config = (self._mssql_commvault_config[0], True)

    def is_dirty(self):
        return any([self._config[1], self._external_file_path[1], self._operations[1], self._shared_backup_locations[1], self._backup_location_user[1], self._backup_location_credentials[1], self._encryption_key[1], self._source_host_user[1], self._mssql_user[1], self._ppt_repository[1], self._ppt_host_user[1], self._staging_pre_script[1], self._staging_post_script[1], self._ingestion_strategy[1], self._mssql_netbackup_config[1], self._mssql_commvault_config[1]])

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
        if not isinstance(other, MSSqlAttachData):
            return False
        return super().__eq__(other) and \
               self.config == other.config and \
               self.external_file_path == other.external_file_path and \
               self.operations == other.operations and \
               self.shared_backup_locations == other.shared_backup_locations and \
               self.backup_location_user == other.backup_location_user and \
               self.backup_location_credentials == other.backup_location_credentials and \
               self.encryption_key == other.encryption_key and \
               self.source_host_user == other.source_host_user and \
               self.mssql_user == other.mssql_user and \
               self.ppt_repository == other.ppt_repository and \
               self.ppt_host_user == other.ppt_host_user and \
               self.staging_pre_script == other.staging_pre_script and \
               self.staging_post_script == other.staging_post_script and \
               self.ingestion_strategy == other.ingestion_strategy and \
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
    def external_file_path(self):
        """
        External file path.

        :rtype: ``str``
        """
        return self._external_file_path[0]

    @external_file_path.setter
    def external_file_path(self, value):
        self._external_file_path = (value, True)

    @property
    def operations(self):
        """
        User-specified operation hooks for this source.

        :rtype: :py:class:`v1_11_7.web.vo.LinkedSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

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
    def backup_location_user(self):
        """
        The user for accessing the shared backup location.

        :rtype: ``str``
        """
        return self._backup_location_user[0]

    @backup_location_user.setter
    def backup_location_user(self, value):
        self._backup_location_user = (value, True)

    @property
    def backup_location_credentials(self):
        """
        The password for accessing the shared backup location.

        :rtype: :py:class:`v1_11_7.web.vo.PasswordCredential`
        """
        return self._backup_location_credentials[0]

    @backup_location_credentials.setter
    def backup_location_credentials(self, value):
        self._backup_location_credentials = (value, True)

    @property
    def encryption_key(self):
        """
        The encryption key to use when restoring encrypted backups.

        :rtype: ``str``
        """
        return self._encryption_key[0]

    @encryption_key.setter
    def encryption_key(self, value):
        self._encryption_key = (value, True)

    @property
    def source_host_user(self):
        """
        OS user on the source to use for linking.

        :rtype: ``str``
        """
        return self._source_host_user[0]

    @source_host_user.setter
    def source_host_user(self, value):
        self._source_host_user = (value, True)

    @property
    def mssql_user(self):
        """
        Information about the mssql user for attaching.

        :rtype: :py:class:`v1_11_7.web.vo.MSSqlUser`
        """
        return self._mssql_user[0]

    @mssql_user.setter
    def mssql_user(self, value):
        self._mssql_user = (value, True)

    @property
    def ppt_repository(self):
        """
        The SQL Server instance on the staging environment to use for pre-
        provisioning.

        :rtype: ``str``
        """
        return self._ppt_repository[0]

    @ppt_repository.setter
    def ppt_repository(self, value):
        self._ppt_repository = (value, True)

    @property
    def ppt_host_user(self):
        """
        OS user on the PPT host to use for linking.

        :rtype: ``str``
        """
        return self._ppt_host_user[0]

    @ppt_host_user.setter
    def ppt_host_user(self, value):
        self._ppt_host_user = (value, True)

    @property
    def staging_pre_script(self):
        """
        The path to a user-provided PowerShell script or executable to run
        prior to restoring from a backup during pre-provisioning.

        :rtype: ``str``
        """
        return self._staging_pre_script[0]

    @staging_pre_script.setter
    def staging_pre_script(self, value):
        self._staging_pre_script = (value, True)

    @property
    def staging_post_script(self):
        """
        The path to a user-provided PowerShell script or executable to run
        after restoring from a backup during pre-provisioning.

        :rtype: ``str``
        """
        return self._staging_post_script[0]

    @staging_post_script.setter
    def staging_post_script(self, value):
        self._staging_post_script = (value, True)

    @property
    def ingestion_strategy(self):
        """
        Configuration that determines what ingestion strategy the source will
        use.

        :rtype: :py:class:`v1_11_7.web.vo.IngestionStrategy`
        """
        return self._ingestion_strategy[0]

    @ingestion_strategy.setter
    def ingestion_strategy(self, value):
        self._ingestion_strategy = (value, True)

    @property
    def mssql_netbackup_config(self):
        """
        Configuration for source that allows ingesting NetBackup backups for
        SQL Server.

        :rtype: :py:class:`v1_11_7.web.vo.MSSqlNetbackupConfig`
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

        :rtype: :py:class:`v1_11_7.web.vo.MSSqlCommvaultConfig`
        """
        return self._mssql_commvault_config[0]

    @mssql_commvault_config.setter
    def mssql_commvault_config(self, value):
        self._mssql_commvault_config = (value, True)

