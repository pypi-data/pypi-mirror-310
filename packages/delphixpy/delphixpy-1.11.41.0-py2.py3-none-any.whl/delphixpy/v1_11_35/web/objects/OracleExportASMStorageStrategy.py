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
#     /delphix-oracle-export-asm-storage-strategy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_35.web.objects.OracleExportStorageStrategy import OracleExportStorageStrategy
from delphixpy.v1_11_35 import factory
from delphixpy.v1_11_35 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleExportASMStorageStrategy(OracleExportStorageStrategy):
    """
    *(extends* :py:class:`v1_11_35.web.vo.OracleExportStorageStrategy` *)*
    Storage strategy for exporting database files to ASM.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleExportASMStorageStrategy", True)
        self._asm_layout = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "asmLayout" in data and data["asmLayout"] is not None:
            obj._asm_layout = (factory.create_object(data["asmLayout"], "OracleASMLayout"), dirty)
            factory.validate_type(obj._asm_layout[0], "OracleASMLayout")
        else:
            obj._asm_layout = (obj.__undef__, dirty)
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
        if "asm_layout" == "type" or (self.asm_layout is not self.__undef__ and (not (dirty and not self._asm_layout[1]) or self.is_dirty_list(self.asm_layout, self._asm_layout) or belongs_to_parent)):
            dct["asmLayout"] = dictify(self.asm_layout, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._asm_layout = (self._asm_layout[0], True)

    def is_dirty(self):
        return any([self._asm_layout[1]])

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
        if not isinstance(other, OracleExportASMStorageStrategy):
            return False
        return super().__eq__(other) and \
               self.asm_layout == other.asm_layout

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def asm_layout(self):
        """
        The ASM configuration of the exported database.

        :rtype: :py:class:`v1_11_35.web.vo.OracleASMLayout`
        """
        return self._asm_layout[0]

    @asm_layout.setter
    def asm_layout(self, value):
        self._asm_layout = (value, True)

