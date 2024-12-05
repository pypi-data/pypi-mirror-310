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
#     /delphix-oracle-asm-layout.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleASMLayout(TypedObject):
    """
    *(extends* :py:class:`v1_11_23.web.vo.TypedObject` *)* ASM diskgroups for
    datafiles, archive logs/redo logs.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleASMLayout", True)
        self._default_data_diskgroup = (self.__undef__, True)
        self._redo_diskgroup = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._default_data_diskgroup = (data.get("defaultDataDiskgroup", obj.__undef__), dirty)
        if obj._default_data_diskgroup[0] is not None and obj._default_data_diskgroup[0] is not obj.__undef__:
            assert isinstance(obj._default_data_diskgroup[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._default_data_diskgroup[0], type(obj._default_data_diskgroup[0])))
            common.validate_format(obj._default_data_diskgroup[0], "None", None, None)
        obj._redo_diskgroup = (data.get("redoDiskgroup", obj.__undef__), dirty)
        if obj._redo_diskgroup[0] is not None and obj._redo_diskgroup[0] is not obj.__undef__:
            assert isinstance(obj._redo_diskgroup[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._redo_diskgroup[0], type(obj._redo_diskgroup[0])))
            common.validate_format(obj._redo_diskgroup[0], "None", None, None)
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
        if "default_data_diskgroup" == "type" or (self.default_data_diskgroup is not self.__undef__ and (not (dirty and not self._default_data_diskgroup[1]) or self.is_dirty_list(self.default_data_diskgroup, self._default_data_diskgroup) or belongs_to_parent)):
            dct["defaultDataDiskgroup"] = dictify(self.default_data_diskgroup)
        if "redo_diskgroup" == "type" or (self.redo_diskgroup is not self.__undef__ and (not (dirty and not self._redo_diskgroup[1]) or self.is_dirty_list(self.redo_diskgroup, self._redo_diskgroup) or belongs_to_parent)):
            dct["redoDiskgroup"] = dictify(self.redo_diskgroup)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._default_data_diskgroup = (self._default_data_diskgroup[0], True)
        self._redo_diskgroup = (self._redo_diskgroup[0], True)

    def is_dirty(self):
        return any([self._default_data_diskgroup[1], self._redo_diskgroup[1]])

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
        if not isinstance(other, OracleASMLayout):
            return False
        return super().__eq__(other) and \
               self.default_data_diskgroup == other.default_data_diskgroup and \
               self.redo_diskgroup == other.redo_diskgroup

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def default_data_diskgroup(self):
        """
        Default diskgroup for datafiles.

        :rtype: ``str``
        """
        return self._default_data_diskgroup[0]

    @default_data_diskgroup.setter
    def default_data_diskgroup(self, value):
        self._default_data_diskgroup = (value, True)

    @property
    def redo_diskgroup(self):
        """
        Diskgroup for archive logs. Optional as it is not required for PDB
        databases.

        :rtype: ``str``
        """
        return self._redo_diskgroup[0]

    @redo_diskgroup.setter
    def redo_diskgroup(self, value):
        self._redo_diskgroup = (value, True)

