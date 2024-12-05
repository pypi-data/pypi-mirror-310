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
#     /delphix-oracle-pdb-link-from-staging.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.OracleBaseStagingLinkData import OracleBaseStagingLinkData
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OraclePDBLinkFromStaging(OracleBaseStagingLinkData):
    """
    *(extends* :py:class:`v1_11_34.web.vo.OracleBaseStagingLinkData` *)*
    Represents parameters to link a pluggable Oracle database using a staging
    database.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OraclePDBLinkFromStaging", True)
        self._database_name = (self.__undef__, True)
        self._cdb_config = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._database_name = (data.get("databaseName", obj.__undef__), dirty)
        if obj._database_name[0] is not None and obj._database_name[0] is not obj.__undef__:
            assert isinstance(obj._database_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._database_name[0], type(obj._database_name[0])))
            common.validate_format(obj._database_name[0], "oraclePDBName", None, 30)
        obj._cdb_config = (data.get("cdbConfig", obj.__undef__), dirty)
        if obj._cdb_config[0] is not None and obj._cdb_config[0] is not obj.__undef__:
            assert isinstance(obj._cdb_config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._cdb_config[0], type(obj._cdb_config[0])))
            common.validate_format(obj._cdb_config[0], "objectReference", None, None)
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
        if "cdb_config" == "type" or (self.cdb_config is not self.__undef__ and (not (dirty and not self._cdb_config[1]) or self.is_dirty_list(self.cdb_config, self._cdb_config) or belongs_to_parent)):
            dct["cdbConfig"] = dictify(self.cdb_config)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._database_name = (self._database_name[0], True)
        self._cdb_config = (self._cdb_config[0], True)

    def is_dirty(self):
        return any([self._database_name[1], self._cdb_config[1]])

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
        if not isinstance(other, OraclePDBLinkFromStaging):
            return False
        return super().__eq__(other) and \
               self.database_name == other.database_name and \
               self.cdb_config == other.cdb_config

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def database_name(self):
        """
        The name of the Oracle pluggable database.

        :rtype: ``str``
        """
        return self._database_name[0]

    @database_name.setter
    def database_name(self, value):
        self._database_name = (value, True)

    @property
    def cdb_config(self):
        """
        Reference of the CDB source config.

        :rtype: ``str``
        """
        return self._cdb_config[0]

    @cdb_config.setter
    def cdb_config(self, value):
        self._cdb_config = (value, True)

