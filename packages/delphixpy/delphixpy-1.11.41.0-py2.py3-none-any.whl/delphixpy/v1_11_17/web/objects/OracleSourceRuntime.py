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
#     /delphix-oracle-source-runtime.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_17.web.objects.OracleBaseSourceRuntime import OracleBaseSourceRuntime
from delphixpy.v1_11_17 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleSourceRuntime(OracleBaseSourceRuntime):
    """
    *(extends* :py:class:`v1_11_17.web.vo.OracleBaseSourceRuntime` *)* Runtime
    (non-persistent) properties of an Oracle source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleSourceRuntime", True)
        self._bct_enabled = (self.__undef__, True)
        self._rac_enabled = (self.__undef__, True)
        self._dnfs_enabled = (self.__undef__, True)
        self._archivelog_enabled = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._bct_enabled = (data.get("bctEnabled", obj.__undef__), dirty)
        if obj._bct_enabled[0] is not None and obj._bct_enabled[0] is not obj.__undef__:
            assert isinstance(obj._bct_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._bct_enabled[0], type(obj._bct_enabled[0])))
            common.validate_format(obj._bct_enabled[0], "None", None, None)
        obj._rac_enabled = (data.get("racEnabled", obj.__undef__), dirty)
        if obj._rac_enabled[0] is not None and obj._rac_enabled[0] is not obj.__undef__:
            assert isinstance(obj._rac_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._rac_enabled[0], type(obj._rac_enabled[0])))
            common.validate_format(obj._rac_enabled[0], "None", None, None)
        obj._dnfs_enabled = (data.get("dnfsEnabled", obj.__undef__), dirty)
        if obj._dnfs_enabled[0] is not None and obj._dnfs_enabled[0] is not obj.__undef__:
            assert isinstance(obj._dnfs_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._dnfs_enabled[0], type(obj._dnfs_enabled[0])))
            common.validate_format(obj._dnfs_enabled[0], "None", None, None)
        obj._archivelog_enabled = (data.get("archivelogEnabled", obj.__undef__), dirty)
        if obj._archivelog_enabled[0] is not None and obj._archivelog_enabled[0] is not obj.__undef__:
            assert isinstance(obj._archivelog_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._archivelog_enabled[0], type(obj._archivelog_enabled[0])))
            common.validate_format(obj._archivelog_enabled[0], "None", None, None)
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
        if "bct_enabled" == "type" or (self.bct_enabled is not self.__undef__ and (not (dirty and not self._bct_enabled[1]))):
            dct["bctEnabled"] = dictify(self.bct_enabled)
        if "rac_enabled" == "type" or (self.rac_enabled is not self.__undef__ and (not (dirty and not self._rac_enabled[1]))):
            dct["racEnabled"] = dictify(self.rac_enabled)
        if "dnfs_enabled" == "type" or (self.dnfs_enabled is not self.__undef__ and (not (dirty and not self._dnfs_enabled[1]))):
            dct["dnfsEnabled"] = dictify(self.dnfs_enabled)
        if "archivelog_enabled" == "type" or (self.archivelog_enabled is not self.__undef__ and (not (dirty and not self._archivelog_enabled[1]))):
            dct["archivelogEnabled"] = dictify(self.archivelog_enabled)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._bct_enabled = (self._bct_enabled[0], True)
        self._rac_enabled = (self._rac_enabled[0], True)
        self._dnfs_enabled = (self._dnfs_enabled[0], True)
        self._archivelog_enabled = (self._archivelog_enabled[0], True)

    def is_dirty(self):
        return any([self._bct_enabled[1], self._rac_enabled[1], self._dnfs_enabled[1], self._archivelog_enabled[1]])

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
        if not isinstance(other, OracleSourceRuntime):
            return False
        return super().__eq__(other) and \
               self.bct_enabled == other.bct_enabled and \
               self.rac_enabled == other.rac_enabled and \
               self.dnfs_enabled == other.dnfs_enabled and \
               self.archivelog_enabled == other.archivelog_enabled

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def bct_enabled(self):
        """
        True if block change tracking is enabled.

        :rtype: ``bool``
        """
        return self._bct_enabled[0]

    @bct_enabled.setter
    def bct_enabled(self, value):
        self._bct_enabled = (value, True)

    @property
    def rac_enabled(self):
        """
        True for a RAC source database.

        :rtype: ``bool``
        """
        return self._rac_enabled[0]

    @rac_enabled.setter
    def rac_enabled(self, value):
        self._rac_enabled = (value, True)

    @property
    def dnfs_enabled(self):
        """
        True if the database has Oracle Direct NFS client enabled.

        :rtype: ``bool``
        """
        return self._dnfs_enabled[0]

    @dnfs_enabled.setter
    def dnfs_enabled(self, value):
        self._dnfs_enabled = (value, True)

    @property
    def archivelog_enabled(self):
        """
        True if the database is running in ARCHIVELOG mode.

        :rtype: ``bool``
        """
        return self._archivelog_enabled[0]

    @archivelog_enabled.setter
    def archivelog_enabled(self, value):
        self._archivelog_enabled = (value, True)

