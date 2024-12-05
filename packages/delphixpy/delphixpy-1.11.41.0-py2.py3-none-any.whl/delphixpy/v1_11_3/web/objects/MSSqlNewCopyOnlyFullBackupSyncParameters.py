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
#     /delphix-mssql-new-copy-only-full-backup-sync-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_3.web.objects.MSSqlSyncParameters import MSSqlSyncParameters
from delphixpy.v1_11_3 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlNewCopyOnlyFullBackupSyncParameters(MSSqlSyncParameters):
    """
    *(extends* :py:class:`v1_11_3.web.vo.MSSqlSyncParameters` *)* The
    parameters to use as input to sync MSSQL databases using a new copy-only
    full backup taken by Delphix.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlNewCopyOnlyFullBackupSyncParameters", True)
        self._compression_enabled = (self.__undef__, True)
        self._backup_policy = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "compressionEnabled" not in data:
            raise ValueError("Missing required property \"compressionEnabled\".")
        obj._compression_enabled = (data.get("compressionEnabled", obj.__undef__), dirty)
        if obj._compression_enabled[0] is not None and obj._compression_enabled[0] is not obj.__undef__:
            assert isinstance(obj._compression_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._compression_enabled[0], type(obj._compression_enabled[0])))
            common.validate_format(obj._compression_enabled[0], "None", None, None)
        obj._backup_policy = (data.get("backupPolicy", obj.__undef__), dirty)
        if obj._backup_policy[0] is not None and obj._backup_policy[0] is not obj.__undef__:
            assert isinstance(obj._backup_policy[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._backup_policy[0], type(obj._backup_policy[0])))
            assert obj._backup_policy[0] in ['PRIMARY', 'SECONDARY_ONLY', 'PREFER_SECONDARY'], "Expected enum ['PRIMARY', 'SECONDARY_ONLY', 'PREFER_SECONDARY'] but got %s" % obj._backup_policy[0]
            common.validate_format(obj._backup_policy[0], "None", None, None)
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
        if "compression_enabled" == "type" or (self.compression_enabled is not self.__undef__ and (not (dirty and not self._compression_enabled[1]) or self.is_dirty_list(self.compression_enabled, self._compression_enabled) or belongs_to_parent)):
            dct["compressionEnabled"] = dictify(self.compression_enabled)
        if "backup_policy" == "type" or (self.backup_policy is not self.__undef__ and (not (dirty and not self._backup_policy[1]) or self.is_dirty_list(self.backup_policy, self._backup_policy) or belongs_to_parent)):
            dct["backupPolicy"] = dictify(self.backup_policy)
        elif belongs_to_parent and self.backup_policy is self.__undef__:
            dct["backupPolicy"] = "PRIMARY"
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._compression_enabled = (self._compression_enabled[0], True)
        self._backup_policy = (self._backup_policy[0], True)

    def is_dirty(self):
        return any([self._compression_enabled[1], self._backup_policy[1]])

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
        if not isinstance(other, MSSqlNewCopyOnlyFullBackupSyncParameters):
            return False
        return super().__eq__(other) and \
               self.compression_enabled == other.compression_enabled and \
               self.backup_policy == other.backup_policy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def compression_enabled(self):
        """
        If this parameter is set to true, Delphix will take a compressed copy
        only full backup of the source database. When set to false, Delphix
        will use the SQL Server instance's compression default.

        :rtype: ``bool``
        """
        return self._compression_enabled[0]

    @compression_enabled.setter
    def compression_enabled(self, value):
        self._compression_enabled = (value, True)

    @property
    def backup_policy(self):
        """
        *(default value: PRIMARY)* Specify which node of an availability group
        to run the copy-only full backup on. *(permitted values: PRIMARY,
        SECONDARY_ONLY, PREFER_SECONDARY)*

        :rtype: ``str``
        """
        return self._backup_policy[0]

    @backup_policy.setter
    def backup_policy(self, value):
        self._backup_policy = (value, True)

