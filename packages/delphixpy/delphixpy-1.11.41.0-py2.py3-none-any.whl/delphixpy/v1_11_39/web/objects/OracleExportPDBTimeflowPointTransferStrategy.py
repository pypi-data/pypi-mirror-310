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
#     /delphix-oracle-export-pdb-timeflow-point-transfer-strategy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.OracleExportPDBTransferStrategy import OracleExportPDBTransferStrategy
from delphixpy.v1_11_39 import factory
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleExportPDBTimeflowPointTransferStrategy(OracleExportPDBTransferStrategy):
    """
    *(extends* :py:class:`v1_11_39.web.vo.OracleExportPDBTransferStrategy` *)*
    Create a physical pluggable database from a TimeFlow point.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleExportPDBTimeflowPointTransferStrategy", True)
        self._source_config = (self.__undef__, True)
        self._timeflow_point_parameters = (self.__undef__, True)
        self._mount_base = (self.__undef__, True)
        self._config_params = (self.__undef__, True)
        self._parent_tde_keystore_path = (self.__undef__, True)
        self._parent_tde_keystore_password = (self.__undef__, True)
        self._tde_exported_key_file_secret = (self.__undef__, True)
        self._tde_key_identifier = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "sourceConfig" not in data:
            raise ValueError("Missing required property \"sourceConfig\".")
        if "sourceConfig" in data and data["sourceConfig"] is not None:
            obj._source_config = (factory.create_object(data["sourceConfig"], "OraclePDBConfig"), dirty)
            factory.validate_type(obj._source_config[0], "OraclePDBConfig")
        else:
            obj._source_config = (obj.__undef__, dirty)
        if "timeflowPointParameters" not in data:
            raise ValueError("Missing required property \"timeflowPointParameters\".")
        if "timeflowPointParameters" in data and data["timeflowPointParameters"] is not None:
            obj._timeflow_point_parameters = (factory.create_object(data["timeflowPointParameters"], "TimeflowPointParameters"), dirty)
            factory.validate_type(obj._timeflow_point_parameters[0], "TimeflowPointParameters")
        else:
            obj._timeflow_point_parameters = (obj.__undef__, dirty)
        obj._mount_base = (data.get("mountBase", obj.__undef__), dirty)
        if obj._mount_base[0] is not None and obj._mount_base[0] is not obj.__undef__:
            assert isinstance(obj._mount_base[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_base[0], type(obj._mount_base[0])))
            common.validate_format(obj._mount_base[0], "unixrestrictedpath", None, 256)
        obj._config_params = (data.get("configParams", obj.__undef__), dirty)
        if obj._config_params[0] is not None and obj._config_params[0] is not obj.__undef__:
            assert isinstance(obj._config_params[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._config_params[0], type(obj._config_params[0])))
            common.validate_format(obj._config_params[0], "None", None, None)
        obj._parent_tde_keystore_path = (data.get("parentTdeKeystorePath", obj.__undef__), dirty)
        if obj._parent_tde_keystore_path[0] is not None and obj._parent_tde_keystore_path[0] is not obj.__undef__:
            assert isinstance(obj._parent_tde_keystore_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent_tde_keystore_path[0], type(obj._parent_tde_keystore_path[0])))
            common.validate_format(obj._parent_tde_keystore_path[0], "unixrestrictedpath", None, 512)
        obj._parent_tde_keystore_password = (data.get("parentTdeKeystorePassword", obj.__undef__), dirty)
        if obj._parent_tde_keystore_password[0] is not None and obj._parent_tde_keystore_password[0] is not obj.__undef__:
            assert isinstance(obj._parent_tde_keystore_password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent_tde_keystore_password[0], type(obj._parent_tde_keystore_password[0])))
            common.validate_format(obj._parent_tde_keystore_password[0], "password", 1, 128)
        obj._tde_exported_key_file_secret = (data.get("tdeExportedKeyFileSecret", obj.__undef__), dirty)
        if obj._tde_exported_key_file_secret[0] is not None and obj._tde_exported_key_file_secret[0] is not obj.__undef__:
            assert isinstance(obj._tde_exported_key_file_secret[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tde_exported_key_file_secret[0], type(obj._tde_exported_key_file_secret[0])))
            common.validate_format(obj._tde_exported_key_file_secret[0], "password", 1, 128)
        obj._tde_key_identifier = (data.get("tdeKeyIdentifier", obj.__undef__), dirty)
        if obj._tde_key_identifier[0] is not None and obj._tde_key_identifier[0] is not obj.__undef__:
            assert isinstance(obj._tde_key_identifier[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._tde_key_identifier[0], type(obj._tde_key_identifier[0])))
            common.validate_format(obj._tde_key_identifier[0], "None", 34, 78)
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
        if "source_config" == "type" or (self.source_config is not self.__undef__ and (not (dirty and not self._source_config[1]) or self.is_dirty_list(self.source_config, self._source_config) or belongs_to_parent)):
            dct["sourceConfig"] = dictify(self.source_config, prop_is_list_or_vo=True)
        if "timeflow_point_parameters" == "type" or (self.timeflow_point_parameters is not self.__undef__ and (not (dirty and not self._timeflow_point_parameters[1]) or self.is_dirty_list(self.timeflow_point_parameters, self._timeflow_point_parameters) or belongs_to_parent)):
            dct["timeflowPointParameters"] = dictify(self.timeflow_point_parameters, prop_is_list_or_vo=True)
        if "mount_base" == "type" or (self.mount_base is not self.__undef__ and (not (dirty and not self._mount_base[1]) or self.is_dirty_list(self.mount_base, self._mount_base) or belongs_to_parent)):
            dct["mountBase"] = dictify(self.mount_base)
        if "config_params" == "type" or (self.config_params is not self.__undef__ and (not (dirty and not self._config_params[1]) or self.is_dirty_list(self.config_params, self._config_params) or belongs_to_parent)):
            dct["configParams"] = dictify(self.config_params, prop_is_list_or_vo=True)
        if "parent_tde_keystore_path" == "type" or (self.parent_tde_keystore_path is not self.__undef__ and (not (dirty and not self._parent_tde_keystore_path[1]) or self.is_dirty_list(self.parent_tde_keystore_path, self._parent_tde_keystore_path) or belongs_to_parent)):
            dct["parentTdeKeystorePath"] = dictify(self.parent_tde_keystore_path)
        if "parent_tde_keystore_password" == "type" or (self.parent_tde_keystore_password is not self.__undef__ and (not (dirty and not self._parent_tde_keystore_password[1]) or self.is_dirty_list(self.parent_tde_keystore_password, self._parent_tde_keystore_password) or belongs_to_parent)):
            dct["parentTdeKeystorePassword"] = dictify(self.parent_tde_keystore_password)
        if "tde_exported_key_file_secret" == "type" or (self.tde_exported_key_file_secret is not self.__undef__ and (not (dirty and not self._tde_exported_key_file_secret[1]) or self.is_dirty_list(self.tde_exported_key_file_secret, self._tde_exported_key_file_secret) or belongs_to_parent)):
            dct["tdeExportedKeyFileSecret"] = dictify(self.tde_exported_key_file_secret)
        if "tde_key_identifier" == "type" or (self.tde_key_identifier is not self.__undef__ and (not (dirty and not self._tde_key_identifier[1]) or self.is_dirty_list(self.tde_key_identifier, self._tde_key_identifier) or belongs_to_parent)):
            dct["tdeKeyIdentifier"] = dictify(self.tde_key_identifier)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._source_config = (self._source_config[0], True)
        self._timeflow_point_parameters = (self._timeflow_point_parameters[0], True)
        self._mount_base = (self._mount_base[0], True)
        self._config_params = (self._config_params[0], True)
        self._parent_tde_keystore_path = (self._parent_tde_keystore_path[0], True)
        self._parent_tde_keystore_password = (self._parent_tde_keystore_password[0], True)
        self._tde_exported_key_file_secret = (self._tde_exported_key_file_secret[0], True)
        self._tde_key_identifier = (self._tde_key_identifier[0], True)

    def is_dirty(self):
        return any([self._source_config[1], self._timeflow_point_parameters[1], self._mount_base[1], self._config_params[1], self._parent_tde_keystore_path[1], self._parent_tde_keystore_password[1], self._tde_exported_key_file_secret[1], self._tde_key_identifier[1]])

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
        if not isinstance(other, OracleExportPDBTimeflowPointTransferStrategy):
            return False
        return super().__eq__(other) and \
               self.source_config == other.source_config and \
               self.timeflow_point_parameters == other.timeflow_point_parameters and \
               self.mount_base == other.mount_base and \
               self.config_params == other.config_params and \
               self.parent_tde_keystore_path == other.parent_tde_keystore_path and \
               self.parent_tde_keystore_password == other.parent_tde_keystore_password and \
               self.tde_exported_key_file_secret == other.tde_exported_key_file_secret and \
               self.tde_key_identifier == other.tde_key_identifier

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def source_config(self):
        """
        The source config of the physical database.

        :rtype: :py:class:`v1_11_39.web.vo.OraclePDBConfig`
        """
        return self._source_config[0]

    @source_config.setter
    def source_config(self, value):
        self._source_config = (value, True)

    @property
    def timeflow_point_parameters(self):
        """
        The TimeFlow point, bookmark, or semantic location from which the
        physical database will be created.

        :rtype: :py:class:`v1_11_39.web.vo.TimeflowPointParameters`
        """
        return self._timeflow_point_parameters[0]

    @timeflow_point_parameters.setter
    def timeflow_point_parameters(self, value):
        self._timeflow_point_parameters = (value, True)

    @property
    def mount_base(self):
        """
        The base mount point to use for the NFS mounts for the temporary vPDB.

        :rtype: ``str``
        """
        return self._mount_base[0]

    @mount_base.setter
    def mount_base(self, value):
        self._mount_base = (value, True)

    @property
    def config_params(self):
        """
        Oracle database configuration parameter overrides.

        :rtype: ``dict``
        """
        return self._config_params[0]

    @config_params.setter
    def config_params(self, value):
        self._config_params = (value, True)

    @property
    def parent_tde_keystore_path(self):
        """
        Path to a copy of the parent's Oracle transparent data encryption
        keystore on the target host. Required to provision from snapshots
        containing encrypted database files.

        :rtype: ``str``
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

