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
#     /delphix-oracle-virtual-pdb-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_35.web.objects.OracleVirtualSource import OracleVirtualSource
from delphixpy.v1_11_35 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleVirtualPdbSource(OracleVirtualSource):
    """
    *(extends* :py:class:`v1_11_35.web.vo.OracleVirtualSource` *)* A virtual
    Oracle multitenant pluggable database source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleVirtualPdbSource", True)
        self._archivelog_mode = (self.__undef__, True)
        self._config_params = (self.__undef__, True)
        self._config_template = (self.__undef__, True)
        self._node_listeners = (self.__undef__, True)
        self._redo_log_size_in_mb = (self.__undef__, True)
        self._redo_log_groups = (self.__undef__, True)
        self._parent_tde_keystore_path = (self.__undef__, True)
        self._parent_tde_keystore_password = (self.__undef__, True)
        self._tde_exported_key_file_secret = (self.__undef__, True)
        self._tde_uuid = (self.__undef__, True)
        self._tde_key_identifier = (self.__undef__, True)
        self._target_vcdb_tde_keystore_path = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._archivelog_mode = (data.get("archivelogMode", obj.__undef__), dirty)
        if obj._archivelog_mode[0] is not None and obj._archivelog_mode[0] is not obj.__undef__:
            assert isinstance(obj._archivelog_mode[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._archivelog_mode[0], type(obj._archivelog_mode[0])))
            common.validate_format(obj._archivelog_mode[0], "None", None, None)
        obj._config_params = (data.get("configParams", obj.__undef__), dirty)
        if obj._config_params[0] is not None and obj._config_params[0] is not obj.__undef__:
            assert isinstance(obj._config_params[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._config_params[0], type(obj._config_params[0])))
            common.validate_format(obj._config_params[0], "None", None, None)
        obj._config_template = (data.get("configTemplate", obj.__undef__), dirty)
        if obj._config_template[0] is not None and obj._config_template[0] is not obj.__undef__:
            assert isinstance(obj._config_template[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config_template[0], type(obj._config_template[0])))
            common.validate_format(obj._config_template[0], "objectReference", None, None)
        obj._node_listeners = []
        for item in data.get("nodeListeners") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "objectReference", None, None)
            obj._node_listeners.append(item)
        obj._node_listeners = (obj._node_listeners, dirty)
        obj._redo_log_size_in_mb = (data.get("redoLogSizeInMB", obj.__undef__), dirty)
        if obj._redo_log_size_in_mb[0] is not None and obj._redo_log_size_in_mb[0] is not obj.__undef__:
            assert isinstance(obj._redo_log_size_in_mb[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._redo_log_size_in_mb[0], type(obj._redo_log_size_in_mb[0])))
            common.validate_format(obj._redo_log_size_in_mb[0], "None", None, None)
        obj._redo_log_groups = (data.get("redoLogGroups", obj.__undef__), dirty)
        if obj._redo_log_groups[0] is not None and obj._redo_log_groups[0] is not obj.__undef__:
            assert isinstance(obj._redo_log_groups[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._redo_log_groups[0], type(obj._redo_log_groups[0])))
            common.validate_format(obj._redo_log_groups[0], "None", None, None)
        obj._parent_tde_keystore_path = (data.get("parentTdeKeystorePath", obj.__undef__), dirty)
        if obj._parent_tde_keystore_path[0] is not None and obj._parent_tde_keystore_path[0] is not obj.__undef__:
            assert isinstance(obj._parent_tde_keystore_path[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._parent_tde_keystore_path[0], type(obj._parent_tde_keystore_path[0])))
            common.validate_format(obj._parent_tde_keystore_path[0], "unixrestrictedpath", None, 512)
        obj._parent_tde_keystore_password = (data.get("parentTdeKeystorePassword", obj.__undef__), dirty)
        if obj._parent_tde_keystore_password[0] is not None and obj._parent_tde_keystore_password[0] is not obj.__undef__:
            assert isinstance(obj._parent_tde_keystore_password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent_tde_keystore_password[0], type(obj._parent_tde_keystore_password[0])))
            common.validate_format(obj._parent_tde_keystore_password[0], "password", 1, 128)
        obj._tde_exported_key_file_secret = (data.get("tdeExportedKeyFileSecret", obj.__undef__), dirty)
        if obj._tde_exported_key_file_secret[0] is not None and obj._tde_exported_key_file_secret[0] is not obj.__undef__:
            assert isinstance(obj._tde_exported_key_file_secret[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tde_exported_key_file_secret[0], type(obj._tde_exported_key_file_secret[0])))
            common.validate_format(obj._tde_exported_key_file_secret[0], "password", 1, 128)
        obj._tde_uuid = (data.get("tdeUUID", obj.__undef__), dirty)
        if obj._tde_uuid[0] is not None and obj._tde_uuid[0] is not obj.__undef__:
            assert isinstance(obj._tde_uuid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tde_uuid[0], type(obj._tde_uuid[0])))
            common.validate_format(obj._tde_uuid[0], "None", None, None)
        obj._tde_key_identifier = (data.get("tdeKeyIdentifier", obj.__undef__), dirty)
        if obj._tde_key_identifier[0] is not None and obj._tde_key_identifier[0] is not obj.__undef__:
            assert isinstance(obj._tde_key_identifier[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._tde_key_identifier[0], type(obj._tde_key_identifier[0])))
            common.validate_format(obj._tde_key_identifier[0], "None", 34, 78)
        obj._target_vcdb_tde_keystore_path = (data.get("targetVcdbTdeKeystorePath", obj.__undef__), dirty)
        if obj._target_vcdb_tde_keystore_path[0] is not None and obj._target_vcdb_tde_keystore_path[0] is not obj.__undef__:
            assert isinstance(obj._target_vcdb_tde_keystore_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_vcdb_tde_keystore_path[0], type(obj._target_vcdb_tde_keystore_path[0])))
            common.validate_format(obj._target_vcdb_tde_keystore_path[0], "unixrestrictedpath", 1, None)
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
        if "archivelog_mode" == "type" or (self.archivelog_mode is not self.__undef__ and (not (dirty and not self._archivelog_mode[1]))):
            dct["archivelogMode"] = dictify(self.archivelog_mode)
        if dirty and "archivelogMode" in dct:
            del dct["archivelogMode"]
        if "config_params" == "type" or (self.config_params is not self.__undef__ and (not (dirty and not self._config_params[1]))):
            dct["configParams"] = dictify(self.config_params)
        if dirty and "configParams" in dct:
            del dct["configParams"]
        if "config_template" == "type" or (self.config_template is not self.__undef__ and (not (dirty and not self._config_template[1]))):
            dct["configTemplate"] = dictify(self.config_template)
        if dirty and "configTemplate" in dct:
            del dct["configTemplate"]
        if "node_listeners" == "type" or (self.node_listeners is not self.__undef__ and (not (dirty and not self._node_listeners[1]))):
            dct["nodeListeners"] = dictify(self.node_listeners)
        if dirty and "nodeListeners" in dct:
            del dct["nodeListeners"]
        if "redo_log_size_in_mb" == "type" or (self.redo_log_size_in_mb is not self.__undef__ and (not (dirty and not self._redo_log_size_in_mb[1]))):
            dct["redoLogSizeInMB"] = dictify(self.redo_log_size_in_mb)
        if dirty and "redoLogSizeInMB" in dct:
            del dct["redoLogSizeInMB"]
        if "redo_log_groups" == "type" or (self.redo_log_groups is not self.__undef__ and (not (dirty and not self._redo_log_groups[1]))):
            dct["redoLogGroups"] = dictify(self.redo_log_groups)
        if dirty and "redoLogGroups" in dct:
            del dct["redoLogGroups"]
        if "parent_tde_keystore_path" == "type" or (self.parent_tde_keystore_path is not self.__undef__ and (not (dirty and not self._parent_tde_keystore_path[1]) or self.is_dirty_list(self.parent_tde_keystore_path, self._parent_tde_keystore_path) or belongs_to_parent)):
            dct["parentTdeKeystorePath"] = dictify(self.parent_tde_keystore_path)
        if "parent_tde_keystore_password" == "type" or (self.parent_tde_keystore_password is not self.__undef__ and (not (dirty and not self._parent_tde_keystore_password[1]) or self.is_dirty_list(self.parent_tde_keystore_password, self._parent_tde_keystore_password) or belongs_to_parent)):
            dct["parentTdeKeystorePassword"] = dictify(self.parent_tde_keystore_password)
        if "tde_exported_key_file_secret" == "type" or (self.tde_exported_key_file_secret is not self.__undef__ and (not (dirty and not self._tde_exported_key_file_secret[1]) or self.is_dirty_list(self.tde_exported_key_file_secret, self._tde_exported_key_file_secret) or belongs_to_parent)):
            dct["tdeExportedKeyFileSecret"] = dictify(self.tde_exported_key_file_secret)
        if "tde_uuid" == "type" or (self.tde_uuid is not self.__undef__ and (not (dirty and not self._tde_uuid[1]))):
            dct["tdeUUID"] = dictify(self.tde_uuid)
        if dirty and "tdeUUID" in dct:
            del dct["tdeUUID"]
        if "tde_key_identifier" == "type" or (self.tde_key_identifier is not self.__undef__ and (not (dirty and not self._tde_key_identifier[1]) or self.is_dirty_list(self.tde_key_identifier, self._tde_key_identifier) or belongs_to_parent)):
            dct["tdeKeyIdentifier"] = dictify(self.tde_key_identifier)
        if "target_vcdb_tde_keystore_path" == "type" or (self.target_vcdb_tde_keystore_path is not self.__undef__ and (not (dirty and not self._target_vcdb_tde_keystore_path[1]) or self.is_dirty_list(self.target_vcdb_tde_keystore_path, self._target_vcdb_tde_keystore_path) or belongs_to_parent)):
            dct["targetVcdbTdeKeystorePath"] = dictify(self.target_vcdb_tde_keystore_path)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._archivelog_mode = (self._archivelog_mode[0], True)
        self._config_params = (self._config_params[0], True)
        self._config_template = (self._config_template[0], True)
        self._node_listeners = (self._node_listeners[0], True)
        self._redo_log_size_in_mb = (self._redo_log_size_in_mb[0], True)
        self._redo_log_groups = (self._redo_log_groups[0], True)
        self._parent_tde_keystore_path = (self._parent_tde_keystore_path[0], True)
        self._parent_tde_keystore_password = (self._parent_tde_keystore_password[0], True)
        self._tde_exported_key_file_secret = (self._tde_exported_key_file_secret[0], True)
        self._tde_uuid = (self._tde_uuid[0], True)
        self._tde_key_identifier = (self._tde_key_identifier[0], True)
        self._target_vcdb_tde_keystore_path = (self._target_vcdb_tde_keystore_path[0], True)

    def is_dirty(self):
        return any([self._archivelog_mode[1], self._config_params[1], self._config_template[1], self._node_listeners[1], self._redo_log_size_in_mb[1], self._redo_log_groups[1], self._parent_tde_keystore_path[1], self._parent_tde_keystore_password[1], self._tde_exported_key_file_secret[1], self._tde_uuid[1], self._tde_key_identifier[1], self._target_vcdb_tde_keystore_path[1]])

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
        if not isinstance(other, OracleVirtualPdbSource):
            return False
        return super().__eq__(other) and \
               self.archivelog_mode == other.archivelog_mode and \
               self.config_params == other.config_params and \
               self.config_template == other.config_template and \
               self.node_listeners == other.node_listeners and \
               self.redo_log_size_in_mb == other.redo_log_size_in_mb and \
               self.redo_log_groups == other.redo_log_groups and \
               self.parent_tde_keystore_path == other.parent_tde_keystore_path and \
               self.parent_tde_keystore_password == other.parent_tde_keystore_password and \
               self.tde_exported_key_file_secret == other.tde_exported_key_file_secret and \
               self.tde_uuid == other.tde_uuid and \
               self.tde_key_identifier == other.tde_key_identifier and \
               self.target_vcdb_tde_keystore_path == other.target_vcdb_tde_keystore_path

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def archivelog_mode(self):
        """
        Archive Log Mode of the Oracle virtual database. This is not applicable
        to pluggable databases.

        :rtype: ``bool``
        """
        return self._archivelog_mode[0]

    @property
    def config_params(self):
        """
        Oracle database configuration parameter overrides. This is currently
        not supported for pluggable databases.

        :rtype: ``dict``
        """
        return self._config_params[0]

    @property
    def config_template(self):
        """
        Optional database template to use for provisioning and refresh. If set,
        configParams will be ignored on provision or refresh. This is currently
        not supported for pluggable databases.

        :rtype: ``str``
        """
        return self._config_template[0]

    @property
    def node_listeners(self):
        """
        A list of object references to Oracle Node Listeners selected for this
        Virtual Database. Delphix picks one default listener from the target
        environment if this list is empty at virtual database provision time.
        This is not applicable to pluggable databases.

        :rtype: ``list`` of ``str``
        """
        return self._node_listeners[0]

    @property
    def redo_log_size_in_mb(self):
        """
        Online Redo Log size in MB. This is not applicable to pluggable
        databases.

        :rtype: ``int``
        """
        return self._redo_log_size_in_mb[0]

    @property
    def redo_log_groups(self):
        """
        Number of Online Redo Log Groups. This is not applicable to pluggable
        databases.

        :rtype: ``int``
        """
        return self._redo_log_groups[0]

    @property
    def parent_tde_keystore_path(self):
        """
        Path to a copy of the parent's Oracle transparent data encryption
        keystore on the target host. Required to provision from snapshots
        containing encrypted database files.

        :rtype: ``str`` *or* ``null``
        """
        return self._parent_tde_keystore_path[0]

    @parent_tde_keystore_path.setter
    def parent_tde_keystore_path(self, value):
        self._parent_tde_keystore_path = (value, True)

    @property
    def parent_tde_keystore_password(self):
        """
        The password of the keystore specified in parentTdeKeystorePath.

        :rtype: ``str``
        """
        return self._parent_tde_keystore_password[0]

    @parent_tde_keystore_password.setter
    def parent_tde_keystore_password(self, value):
        self._parent_tde_keystore_password = (value, True)

    @property
    def tde_exported_key_file_secret(self):
        """
        Secret to be used while exporting and importing vPDB encryption keys if
        Transparent Data Encryption is enabled on the vPDB.

        :rtype: ``str``
        """
        return self._tde_exported_key_file_secret[0]

    @tde_exported_key_file_secret.setter
    def tde_exported_key_file_secret(self, value):
        self._tde_exported_key_file_secret = (value, True)

    @property
    def tde_uuid(self):
        """
        Unique identifier for PDB-specific TDE objects that reside outside of
        Delphix storage.

        :rtype: ``str``
        """
        return self._tde_uuid[0]

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
    def target_vcdb_tde_keystore_path(self):
        """
        Path to the keystore of the target vCDB.

        :rtype: ``str``
        """
        return self._target_vcdb_tde_keystore_path[0]

    @target_vcdb_tde_keystore_path.setter
    def target_vcdb_tde_keystore_path(self, value):
        self._target_vcdb_tde_keystore_path = (value, True)

