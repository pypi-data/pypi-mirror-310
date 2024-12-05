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
#     /delphix-oracle-export-pdb-inplace-transfer-strategy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.OracleExportPDBTransferStrategy import OracleExportPDBTransferStrategy
from delphixpy.v1_11_36 import factory
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleExportPDBInPlaceTransferStrategy(OracleExportPDBTransferStrategy):
    """
    *(extends* :py:class:`v1_11_36.web.vo.OracleExportPDBTransferStrategy` *)*
    Convert a vPDB to a physical PDB in-place.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleExportPDBInPlaceTransferStrategy", True)
        self._pdb_name = (self.__undef__, True)
        self._virtual_source = (self.__undef__, True)
        self._operations_post_v2_p = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._pdb_name = (data.get("pdbName", obj.__undef__), dirty)
        if obj._pdb_name[0] is not None and obj._pdb_name[0] is not obj.__undef__:
            assert isinstance(obj._pdb_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pdb_name[0], type(obj._pdb_name[0])))
            common.validate_format(obj._pdb_name[0], "oraclePDBName", None, 30)
        obj._virtual_source = (data.get("virtualSource", obj.__undef__), dirty)
        if obj._virtual_source[0] is not None and obj._virtual_source[0] is not obj.__undef__:
            assert isinstance(obj._virtual_source[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._virtual_source[0], type(obj._virtual_source[0])))
            common.validate_format(obj._virtual_source[0], "objectReference", None, None)
        if "operationsPostV2P" in data and data["operationsPostV2P"] is not None:
            obj._operations_post_v2_p = (factory.create_object(data["operationsPostV2P"], "OracleExportOperationsPostV2P"), dirty)
            factory.validate_type(obj._operations_post_v2_p[0], "OracleExportOperationsPostV2P")
        else:
            obj._operations_post_v2_p = (obj.__undef__, dirty)
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
        if "pdb_name" == "type" or (self.pdb_name is not self.__undef__ and (not (dirty and not self._pdb_name[1]) or self.is_dirty_list(self.pdb_name, self._pdb_name) or belongs_to_parent)):
            dct["pdbName"] = dictify(self.pdb_name)
        if "virtual_source" == "type" or (self.virtual_source is not self.__undef__ and (not (dirty and not self._virtual_source[1]) or self.is_dirty_list(self.virtual_source, self._virtual_source) or belongs_to_parent)):
            dct["virtualSource"] = dictify(self.virtual_source)
        if "operations_post_v2_p" == "type" or (self.operations_post_v2_p is not self.__undef__ and (not (dirty and not self._operations_post_v2_p[1]) or self.is_dirty_list(self.operations_post_v2_p, self._operations_post_v2_p) or belongs_to_parent)):
            dct["operationsPostV2P"] = dictify(self.operations_post_v2_p, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._pdb_name = (self._pdb_name[0], True)
        self._virtual_source = (self._virtual_source[0], True)
        self._operations_post_v2_p = (self._operations_post_v2_p[0], True)

    def is_dirty(self):
        return any([self._pdb_name[1], self._virtual_source[1], self._operations_post_v2_p[1]])

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
        if not isinstance(other, OracleExportPDBInPlaceTransferStrategy):
            return False
        return super().__eq__(other) and \
               self.pdb_name == other.pdb_name and \
               self.virtual_source == other.virtual_source and \
               self.operations_post_v2_p == other.operations_post_v2_p

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def pdb_name(self):
        """
        The name to be given to the PDB after it is exported in-place.

        :rtype: ``str``
        """
        return self._pdb_name[0]

    @pdb_name.setter
    def pdb_name(self, value):
        self._pdb_name = (value, True)

    @property
    def virtual_source(self):
        """
        Reference to the virtual PDB source which needs to be converted to
        physical.

        :rtype: ``str``
        """
        return self._virtual_source[0]

    @virtual_source.setter
    def virtual_source(self, value):
        self._virtual_source = (value, True)

    @property
    def operations_post_v2_p(self):
        """
        Indicates operations allowed on virtual source post V2P.

        :rtype: :py:class:`v1_11_36.web.vo.OracleExportOperationsPostV2P`
        """
        return self._operations_post_v2_p[0]

    @operations_post_v2_p.setter
    def operations_post_v2_p(self, value):
        self._operations_post_v2_p = (value, True)

