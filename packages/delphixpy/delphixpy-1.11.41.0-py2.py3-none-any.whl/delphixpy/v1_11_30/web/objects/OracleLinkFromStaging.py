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
#     /delphix-oracle-link-from-staging.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_30.web.objects.OracleBaseStagingLinkData import OracleBaseStagingLinkData
from delphixpy.v1_11_30 import factory
from delphixpy.v1_11_30 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleLinkFromStaging(OracleBaseStagingLinkData):
    """
    *(extends* :py:class:`v1_11_30.web.vo.OracleBaseStagingLinkData` *)*
    Represents parameters to link a non-pluggable Oracle database using a
    staging database.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleLinkFromStaging", True)
        self._database_name = (self.__undef__, True)
        self._unique_name = (self.__undef__, True)
        self._container_type = (self.__undef__, True)
        self._staging_source_parameters = (self.__undef__, True)
        self._tde_keystore_config_type = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._database_name = (data.get("databaseName", obj.__undef__), dirty)
        if obj._database_name[0] is not None and obj._database_name[0] is not obj.__undef__:
            assert isinstance(obj._database_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._database_name[0], type(obj._database_name[0])))
            common.validate_format(obj._database_name[0], "oracleDatabaseName", None, 8)
        obj._unique_name = (data.get("uniqueName", obj.__undef__), dirty)
        if obj._unique_name[0] is not None and obj._unique_name[0] is not obj.__undef__:
            assert isinstance(obj._unique_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._unique_name[0], type(obj._unique_name[0])))
            common.validate_format(obj._unique_name[0], "oracleDbUniqueName", None, 30)
        obj._container_type = (data.get("containerType", obj.__undef__), dirty)
        if obj._container_type[0] is not None and obj._container_type[0] is not obj.__undef__:
            assert isinstance(obj._container_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container_type[0], type(obj._container_type[0])))
            assert obj._container_type[0] in ['ROOT_CDB', 'NON_CDB'], "Expected enum ['ROOT_CDB', 'NON_CDB'] but got %s" % obj._container_type[0]
            common.validate_format(obj._container_type[0], "None", None, None)
        if "stagingSourceParameters" in data and data["stagingSourceParameters"] is not None:
            obj._staging_source_parameters = (factory.create_object(data["stagingSourceParameters"], "OracleStagingSourceParameters"), dirty)
            factory.validate_type(obj._staging_source_parameters[0], "OracleStagingSourceParameters")
        else:
            obj._staging_source_parameters = (obj.__undef__, dirty)
        obj._tde_keystore_config_type = (data.get("tdeKeystoreConfigType", obj.__undef__), dirty)
        if obj._tde_keystore_config_type[0] is not None and obj._tde_keystore_config_type[0] is not obj.__undef__:
            assert isinstance(obj._tde_keystore_config_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tde_keystore_config_type[0], type(obj._tde_keystore_config_type[0])))
            assert obj._tde_keystore_config_type[0] in ['FILE', 'OKV', 'HSM'], "Expected enum ['FILE', 'OKV', 'HSM'] but got %s" % obj._tde_keystore_config_type[0]
            common.validate_format(obj._tde_keystore_config_type[0], "None", None, None)
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
        if "database_name" == "type" or (self.database_name is not self.__undef__ and (not (dirty and not self._database_name[1]) or self.is_dirty_list(self.database_name, self._database_name) or belongs_to_parent)):
            dct["databaseName"] = dictify(self.database_name)
        if "unique_name" == "type" or (self.unique_name is not self.__undef__ and (not (dirty and not self._unique_name[1]) or self.is_dirty_list(self.unique_name, self._unique_name) or belongs_to_parent)):
            dct["uniqueName"] = dictify(self.unique_name)
        if "container_type" == "type" or (self.container_type is not self.__undef__ and (not (dirty and not self._container_type[1]) or self.is_dirty_list(self.container_type, self._container_type) or belongs_to_parent)):
            dct["containerType"] = dictify(self.container_type)
        if "staging_source_parameters" == "type" or (self.staging_source_parameters is not self.__undef__ and (not (dirty and not self._staging_source_parameters[1]) or self.is_dirty_list(self.staging_source_parameters, self._staging_source_parameters) or belongs_to_parent)):
            dct["stagingSourceParameters"] = dictify(self.staging_source_parameters, prop_is_list_or_vo=True)
        if "tde_keystore_config_type" == "type" or (self.tde_keystore_config_type is not self.__undef__ and (not (dirty and not self._tde_keystore_config_type[1]) or self.is_dirty_list(self.tde_keystore_config_type, self._tde_keystore_config_type) or belongs_to_parent)):
            dct["tdeKeystoreConfigType"] = dictify(self.tde_keystore_config_type)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._database_name = (self._database_name[0], True)
        self._unique_name = (self._unique_name[0], True)
        self._container_type = (self._container_type[0], True)
        self._staging_source_parameters = (self._staging_source_parameters[0], True)
        self._tde_keystore_config_type = (self._tde_keystore_config_type[0], True)

    def is_dirty(self):
        return any([self._database_name[1], self._unique_name[1], self._container_type[1], self._staging_source_parameters[1], self._tde_keystore_config_type[1]])

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
        if not isinstance(other, OracleLinkFromStaging):
            return False
        return super().__eq__(other) and \
               self.database_name == other.database_name and \
               self.unique_name == other.unique_name and \
               self.container_type == other.container_type and \
               self.staging_source_parameters == other.staging_source_parameters and \
               self.tde_keystore_config_type == other.tde_keystore_config_type

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def database_name(self):
        """
        The name of the database.

        :rtype: ``str``
        """
        return self._database_name[0]

    @database_name.setter
    def database_name(self, value):
        self._database_name = (value, True)

    @property
    def unique_name(self):
        """
        The unique name of the database.

        :rtype: ``str``
        """
        return self._unique_name[0]

    @unique_name.setter
    def unique_name(self, value):
        self._unique_name = (value, True)

    @property
    def container_type(self):
        """
        The container type of this database. *(permitted values: ROOT_CDB,
        NON_CDB)*

        :rtype: ``str``
        """
        return self._container_type[0]

    @container_type.setter
    def container_type(self, value):
        self._container_type = (value, True)

    @property
    def staging_source_parameters(self):
        """
        Parameters needed to create a staging database.

        :rtype: :py:class:`v1_11_30.web.vo.OracleStagingSourceParameters`
        """
        return self._staging_source_parameters[0]

    @staging_source_parameters.setter
    def staging_source_parameters(self, value):
        self._staging_source_parameters = (value, True)

    @property
    def tde_keystore_config_type(self):
        """
        TDE keystore configuration type of this staging database. *(permitted
        values: FILE, OKV, HSM)*

        :rtype: ``str``
        """
        return self._tde_keystore_config_type[0]

    @tde_keystore_config_type.setter
    def tde_keystore_config_type(self, value):
        self._tde_keystore_config_type = (value, True)

