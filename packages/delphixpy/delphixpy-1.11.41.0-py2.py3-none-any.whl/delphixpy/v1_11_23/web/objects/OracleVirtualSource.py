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
#     /delphix-oracle-virtual-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.OracleManagedSource import OracleManagedSource
from delphixpy.v1_11_23 import factory
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleVirtualSource(OracleManagedSource):
    """
    *(extends* :py:class:`v1_11_23.web.vo.OracleManagedSource` *)* A virtual
    Oracle source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleVirtualSource", True)
        self._operations = (self.__undef__, True)
        self._file_mapping_rules = (self.__undef__, True)
        self._redo_log_size_in_mb = (self.__undef__, True)
        self._redo_log_groups = (self.__undef__, True)
        self._archivelog_mode = (self.__undef__, True)
        self._custom_env_vars = (self.__undef__, True)
        self._allow_auto_vdb_restart_on_host_reboot = (self.__undef__, True)
        self._new_dbid = (self.__undef__, True)
        self._tde_key_identifier = (self.__undef__, True)
        self._source_status = (self.__undef__, True)
        self._invoke_datapatch = (self.__undef__, True)
        self._allow_refresh_rewind_post_v2_p = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "VirtualSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "VirtualSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        obj._file_mapping_rules = (data.get("fileMappingRules", obj.__undef__), dirty)
        if obj._file_mapping_rules[0] is not None and obj._file_mapping_rules[0] is not obj.__undef__:
            assert isinstance(obj._file_mapping_rules[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._file_mapping_rules[0], type(obj._file_mapping_rules[0])))
            common.validate_format(obj._file_mapping_rules[0], "None", None, None)
        obj._redo_log_size_in_mb = (data.get("redoLogSizeInMB", obj.__undef__), dirty)
        if obj._redo_log_size_in_mb[0] is not None and obj._redo_log_size_in_mb[0] is not obj.__undef__:
            assert isinstance(obj._redo_log_size_in_mb[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._redo_log_size_in_mb[0], type(obj._redo_log_size_in_mb[0])))
            common.validate_format(obj._redo_log_size_in_mb[0], "None", None, None)
        obj._redo_log_groups = (data.get("redoLogGroups", obj.__undef__), dirty)
        if obj._redo_log_groups[0] is not None and obj._redo_log_groups[0] is not obj.__undef__:
            assert isinstance(obj._redo_log_groups[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._redo_log_groups[0], type(obj._redo_log_groups[0])))
            common.validate_format(obj._redo_log_groups[0], "None", None, None)
        obj._archivelog_mode = (data.get("archivelogMode", obj.__undef__), dirty)
        if obj._archivelog_mode[0] is not None and obj._archivelog_mode[0] is not obj.__undef__:
            assert isinstance(obj._archivelog_mode[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._archivelog_mode[0], type(obj._archivelog_mode[0])))
            common.validate_format(obj._archivelog_mode[0], "None", None, None)
        obj._custom_env_vars = []
        for item in data.get("customEnvVars") or []:
            obj._custom_env_vars.append(factory.create_object(item))
            factory.validate_type(obj._custom_env_vars[-1], "OracleCustomEnvVar")
        obj._custom_env_vars = (obj._custom_env_vars, dirty)
        obj._allow_auto_vdb_restart_on_host_reboot = (data.get("allowAutoVDBRestartOnHostReboot", obj.__undef__), dirty)
        if obj._allow_auto_vdb_restart_on_host_reboot[0] is not None and obj._allow_auto_vdb_restart_on_host_reboot[0] is not obj.__undef__:
            assert isinstance(obj._allow_auto_vdb_restart_on_host_reboot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._allow_auto_vdb_restart_on_host_reboot[0], type(obj._allow_auto_vdb_restart_on_host_reboot[0])))
            common.validate_format(obj._allow_auto_vdb_restart_on_host_reboot[0], "None", None, None)
        obj._new_dbid = (data.get("newDBID", obj.__undef__), dirty)
        if obj._new_dbid[0] is not None and obj._new_dbid[0] is not obj.__undef__:
            assert isinstance(obj._new_dbid[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._new_dbid[0], type(obj._new_dbid[0])))
            common.validate_format(obj._new_dbid[0], "None", None, None)
        obj._tde_key_identifier = (data.get("tdeKeyIdentifier", obj.__undef__), dirty)
        if obj._tde_key_identifier[0] is not None and obj._tde_key_identifier[0] is not obj.__undef__:
            assert isinstance(obj._tde_key_identifier[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._tde_key_identifier[0], type(obj._tde_key_identifier[0])))
            common.validate_format(obj._tde_key_identifier[0], "None", 34, 78)
        obj._source_status = (data.get("sourceStatus", obj.__undef__), dirty)
        if obj._source_status[0] is not None and obj._source_status[0] is not obj.__undef__:
            assert isinstance(obj._source_status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source_status[0], type(obj._source_status[0])))
            assert obj._source_status[0] in ['DEFAULT', 'PENDING_V2P_SETUP', 'PENDING_V2P_BACKUP_AS_COPY', 'PENDING_V2P_SWITCH_TO_COPY', 'PENDING_V2P_CLEANUP_ON_SUCCESS', 'DISABLED_POST_V2P'], "Expected enum ['DEFAULT', 'PENDING_V2P_SETUP', 'PENDING_V2P_BACKUP_AS_COPY', 'PENDING_V2P_SWITCH_TO_COPY', 'PENDING_V2P_CLEANUP_ON_SUCCESS', 'DISABLED_POST_V2P'] but got %s" % obj._source_status[0]
            common.validate_format(obj._source_status[0], "None", None, None)
        obj._invoke_datapatch = (data.get("invokeDatapatch", obj.__undef__), dirty)
        if obj._invoke_datapatch[0] is not None and obj._invoke_datapatch[0] is not obj.__undef__:
            assert isinstance(obj._invoke_datapatch[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._invoke_datapatch[0], type(obj._invoke_datapatch[0])))
            common.validate_format(obj._invoke_datapatch[0], "None", None, None)
        obj._allow_refresh_rewind_post_v2_p = (data.get("allowRefreshRewindPostV2P", obj.__undef__), dirty)
        if obj._allow_refresh_rewind_post_v2_p[0] is not None and obj._allow_refresh_rewind_post_v2_p[0] is not obj.__undef__:
            assert isinstance(obj._allow_refresh_rewind_post_v2_p[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._allow_refresh_rewind_post_v2_p[0], type(obj._allow_refresh_rewind_post_v2_p[0])))
            common.validate_format(obj._allow_refresh_rewind_post_v2_p[0], "None", None, None)
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
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "file_mapping_rules" == "type" or (self.file_mapping_rules is not self.__undef__ and (not (dirty and not self._file_mapping_rules[1]) or self.is_dirty_list(self.file_mapping_rules, self._file_mapping_rules) or belongs_to_parent)):
            dct["fileMappingRules"] = dictify(self.file_mapping_rules)
        if "redo_log_size_in_mb" == "type" or (self.redo_log_size_in_mb is not self.__undef__ and (not (dirty and not self._redo_log_size_in_mb[1]) or self.is_dirty_list(self.redo_log_size_in_mb, self._redo_log_size_in_mb) or belongs_to_parent)):
            dct["redoLogSizeInMB"] = dictify(self.redo_log_size_in_mb)
        if "redo_log_groups" == "type" or (self.redo_log_groups is not self.__undef__ and (not (dirty and not self._redo_log_groups[1]) or self.is_dirty_list(self.redo_log_groups, self._redo_log_groups) or belongs_to_parent)):
            dct["redoLogGroups"] = dictify(self.redo_log_groups)
        elif belongs_to_parent and self.redo_log_groups is self.__undef__:
            dct["redoLogGroups"] = 3
        if "archivelog_mode" == "type" or (self.archivelog_mode is not self.__undef__ and (not (dirty and not self._archivelog_mode[1]) or self.is_dirty_list(self.archivelog_mode, self._archivelog_mode) or belongs_to_parent)):
            dct["archivelogMode"] = dictify(self.archivelog_mode)
        elif belongs_to_parent and self.archivelog_mode is self.__undef__:
            dct["archivelogMode"] = True
        if "custom_env_vars" == "type" or (self.custom_env_vars is not self.__undef__ and (not (dirty and not self._custom_env_vars[1]) or self.is_dirty_list(self.custom_env_vars, self._custom_env_vars) or belongs_to_parent)):
            dct["customEnvVars"] = dictify(self.custom_env_vars, prop_is_list_or_vo=True)
        if "allow_auto_vdb_restart_on_host_reboot" == "type" or (self.allow_auto_vdb_restart_on_host_reboot is not self.__undef__ and (not (dirty and not self._allow_auto_vdb_restart_on_host_reboot[1]) or self.is_dirty_list(self.allow_auto_vdb_restart_on_host_reboot, self._allow_auto_vdb_restart_on_host_reboot) or belongs_to_parent)):
            dct["allowAutoVDBRestartOnHostReboot"] = dictify(self.allow_auto_vdb_restart_on_host_reboot)
        if "new_dbid" == "type" or (self.new_dbid is not self.__undef__ and (not (dirty and not self._new_dbid[1]) or self.is_dirty_list(self.new_dbid, self._new_dbid) or belongs_to_parent)):
            dct["newDBID"] = dictify(self.new_dbid)
        elif belongs_to_parent and self.new_dbid is self.__undef__:
            dct["newDBID"] = False
        if "tde_key_identifier" == "type" or (self.tde_key_identifier is not self.__undef__ and (not (dirty and not self._tde_key_identifier[1]) or self.is_dirty_list(self.tde_key_identifier, self._tde_key_identifier) or belongs_to_parent)):
            dct["tdeKeyIdentifier"] = dictify(self.tde_key_identifier)
        if "source_status" == "type" or (self.source_status is not self.__undef__ and (not (dirty and not self._source_status[1]))):
            dct["sourceStatus"] = dictify(self.source_status)
        if dirty and "sourceStatus" in dct:
            del dct["sourceStatus"]
        if "invoke_datapatch" == "type" or (self.invoke_datapatch is not self.__undef__ and (not (dirty and not self._invoke_datapatch[1]) or self.is_dirty_list(self.invoke_datapatch, self._invoke_datapatch) or belongs_to_parent)):
            dct["invokeDatapatch"] = dictify(self.invoke_datapatch)
        if "allow_refresh_rewind_post_v2_p" == "type" or (self.allow_refresh_rewind_post_v2_p is not self.__undef__ and (not (dirty and not self._allow_refresh_rewind_post_v2_p[1]) or self.is_dirty_list(self.allow_refresh_rewind_post_v2_p, self._allow_refresh_rewind_post_v2_p) or belongs_to_parent)):
            dct["allowRefreshRewindPostV2P"] = dictify(self.allow_refresh_rewind_post_v2_p)
        elif belongs_to_parent and self.allow_refresh_rewind_post_v2_p is self.__undef__:
            dct["allowRefreshRewindPostV2P"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._operations = (self._operations[0], True)
        self._file_mapping_rules = (self._file_mapping_rules[0], True)
        self._redo_log_size_in_mb = (self._redo_log_size_in_mb[0], True)
        self._redo_log_groups = (self._redo_log_groups[0], True)
        self._archivelog_mode = (self._archivelog_mode[0], True)
        self._custom_env_vars = (self._custom_env_vars[0], True)
        self._allow_auto_vdb_restart_on_host_reboot = (self._allow_auto_vdb_restart_on_host_reboot[0], True)
        self._new_dbid = (self._new_dbid[0], True)
        self._tde_key_identifier = (self._tde_key_identifier[0], True)
        self._source_status = (self._source_status[0], True)
        self._invoke_datapatch = (self._invoke_datapatch[0], True)
        self._allow_refresh_rewind_post_v2_p = (self._allow_refresh_rewind_post_v2_p[0], True)

    def is_dirty(self):
        return any([self._operations[1], self._file_mapping_rules[1], self._redo_log_size_in_mb[1], self._redo_log_groups[1], self._archivelog_mode[1], self._custom_env_vars[1], self._allow_auto_vdb_restart_on_host_reboot[1], self._new_dbid[1], self._tde_key_identifier[1], self._source_status[1], self._invoke_datapatch[1], self._allow_refresh_rewind_post_v2_p[1]])

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
        if not isinstance(other, OracleVirtualSource):
            return False
        return super().__eq__(other) and \
               self.operations == other.operations and \
               self.file_mapping_rules == other.file_mapping_rules and \
               self.redo_log_size_in_mb == other.redo_log_size_in_mb and \
               self.redo_log_groups == other.redo_log_groups and \
               self.archivelog_mode == other.archivelog_mode and \
               self.custom_env_vars == other.custom_env_vars and \
               self.allow_auto_vdb_restart_on_host_reboot == other.allow_auto_vdb_restart_on_host_reboot and \
               self.new_dbid == other.new_dbid and \
               self.tde_key_identifier == other.tde_key_identifier and \
               self.source_status == other.source_status and \
               self.invoke_datapatch == other.invoke_datapatch and \
               self.allow_refresh_rewind_post_v2_p == other.allow_refresh_rewind_post_v2_p

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def operations(self):
        """
        User-specified operation hooks for this source.

        :rtype: :py:class:`v1_11_23.web.vo.VirtualSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

    @property
    def file_mapping_rules(self):
        """
        Database file mapping rules.

        :rtype: ``str``
        """
        return self._file_mapping_rules[0]

    @file_mapping_rules.setter
    def file_mapping_rules(self, value):
        self._file_mapping_rules = (value, True)

    @property
    def redo_log_size_in_mb(self):
        """
        Online Redo Log size in MB.

        :rtype: ``int``
        """
        return self._redo_log_size_in_mb[0]

    @redo_log_size_in_mb.setter
    def redo_log_size_in_mb(self, value):
        self._redo_log_size_in_mb = (value, True)

    @property
    def redo_log_groups(self):
        """
        *(default value: 3)* Number of Online Redo Log Groups.

        :rtype: ``int``
        """
        return self._redo_log_groups[0]

    @redo_log_groups.setter
    def redo_log_groups(self, value):
        self._redo_log_groups = (value, True)

    @property
    def archivelog_mode(self):
        """
        *(default value: True)* Archive Log Mode of the Oracle virtual
        database.

        :rtype: ``bool``
        """
        return self._archivelog_mode[0]

    @archivelog_mode.setter
    def archivelog_mode(self, value):
        self._archivelog_mode = (value, True)

    @property
    def custom_env_vars(self):
        """
        Custom environment variables for Oracle databases.

        :rtype: ``list`` of :py:class:`v1_11_23.web.vo.OracleCustomEnvVar`
        """
        return self._custom_env_vars[0]

    @custom_env_vars.setter
    def custom_env_vars(self, value):
        self._custom_env_vars = (value, True)

    @property
    def allow_auto_vdb_restart_on_host_reboot(self):
        """
        Indicates whether Delphix should automatically restart this virtual
        source when target host reboot is detected.

        :rtype: ``bool``
        """
        return self._allow_auto_vdb_restart_on_host_reboot[0]

    @allow_auto_vdb_restart_on_host_reboot.setter
    def allow_auto_vdb_restart_on_host_reboot(self, value):
        self._allow_auto_vdb_restart_on_host_reboot = (value, True)

    @property
    def new_dbid(self):
        """
        Indicates whether Delphix will generate a new DBID during VDB provision
        or refresh.

        :rtype: ``bool``
        """
        return self._new_dbid[0]

    @new_dbid.setter
    def new_dbid(self, value):
        self._new_dbid = (value, True)

    @property
    def tde_key_identifier(self):
        """
        ID of the key created by Delphix, as recorded in
        v$encryption_keys.key_id.

        :rtype: ``str`` *or* ``null``
        """
        return self._tde_key_identifier[0]

    @tde_key_identifier.setter
    def tde_key_identifier(self, value):
        self._tde_key_identifier = (value, True)

    @property
    def source_status(self):
        """
        *(default value: DEFAULT)* Virtual source status following a V2P
        operation. *(permitted values: DEFAULT, PENDING_V2P_SETUP,
        PENDING_V2P_BACKUP_AS_COPY, PENDING_V2P_SWITCH_TO_COPY,
        PENDING_V2P_CLEANUP_ON_SUCCESS, DISABLED_POST_V2P)*

        :rtype: ``str``
        """
        return self._source_status[0]

    @property
    def invoke_datapatch(self):
        """
        Indicates whether to invoke Oracle's datapatch utility in various
        Delphix workflows.

        :rtype: ``bool``
        """
        return self._invoke_datapatch[0]

    @invoke_datapatch.setter
    def invoke_datapatch(self, value):
        self._invoke_datapatch = (value, True)

    @property
    def allow_refresh_rewind_post_v2_p(self):
        """
        Indicates whether refresh/rewind operation allowed on virtual source
        post V2P.

        :rtype: ``bool``
        """
        return self._allow_refresh_rewind_post_v2_p[0]

    @allow_refresh_rewind_post_v2_p.setter
    def allow_refresh_rewind_post_v2_p(self, value):
        self._allow_refresh_rewind_post_v2_p = (value, True)

