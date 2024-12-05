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
#     /delphix-purge-logs-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.TypedObject import TypedObject
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PurgeLogsParameters(TypedObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.TypedObject` *)* Represents the
    parameters of a purgeLogs request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PurgeLogsParameters", True)
        self._storage_space_to_reclaim = (self.__undef__, True)
        self._dry_run = (self.__undef__, True)
        self._delete_snapshot_logs = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "storageSpaceToReclaim" not in data:
            raise ValueError("Missing required property \"storageSpaceToReclaim\".")
        obj._storage_space_to_reclaim = (data.get("storageSpaceToReclaim", obj.__undef__), dirty)
        if obj._storage_space_to_reclaim[0] is not None and obj._storage_space_to_reclaim[0] is not obj.__undef__:
            assert isinstance(obj._storage_space_to_reclaim[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._storage_space_to_reclaim[0], type(obj._storage_space_to_reclaim[0])))
            common.validate_format(obj._storage_space_to_reclaim[0], "None", None, None)
        if "dryRun" not in data:
            raise ValueError("Missing required property \"dryRun\".")
        obj._dry_run = (data.get("dryRun", obj.__undef__), dirty)
        if obj._dry_run[0] is not None and obj._dry_run[0] is not obj.__undef__:
            assert isinstance(obj._dry_run[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._dry_run[0], type(obj._dry_run[0])))
            common.validate_format(obj._dry_run[0], "None", None, None)
        if "deleteSnapshotLogs" not in data:
            raise ValueError("Missing required property \"deleteSnapshotLogs\".")
        obj._delete_snapshot_logs = (data.get("deleteSnapshotLogs", obj.__undef__), dirty)
        if obj._delete_snapshot_logs[0] is not None and obj._delete_snapshot_logs[0] is not obj.__undef__:
            assert isinstance(obj._delete_snapshot_logs[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._delete_snapshot_logs[0], type(obj._delete_snapshot_logs[0])))
            common.validate_format(obj._delete_snapshot_logs[0], "None", None, None)
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
        if "storage_space_to_reclaim" == "type" or (self.storage_space_to_reclaim is not self.__undef__ and (not (dirty and not self._storage_space_to_reclaim[1]) or self.is_dirty_list(self.storage_space_to_reclaim, self._storage_space_to_reclaim) or belongs_to_parent)):
            dct["storageSpaceToReclaim"] = dictify(self.storage_space_to_reclaim)
        if "dry_run" == "type" or (self.dry_run is not self.__undef__ and (not (dirty and not self._dry_run[1]) or self.is_dirty_list(self.dry_run, self._dry_run) or belongs_to_parent)):
            dct["dryRun"] = dictify(self.dry_run)
        if "delete_snapshot_logs" == "type" or (self.delete_snapshot_logs is not self.__undef__ and (not (dirty and not self._delete_snapshot_logs[1]) or self.is_dirty_list(self.delete_snapshot_logs, self._delete_snapshot_logs) or belongs_to_parent)):
            dct["deleteSnapshotLogs"] = dictify(self.delete_snapshot_logs)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._storage_space_to_reclaim = (self._storage_space_to_reclaim[0], True)
        self._dry_run = (self._dry_run[0], True)
        self._delete_snapshot_logs = (self._delete_snapshot_logs[0], True)

    def is_dirty(self):
        return any([self._storage_space_to_reclaim[1], self._dry_run[1], self._delete_snapshot_logs[1]])

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
        if not isinstance(other, PurgeLogsParameters):
            return False
        return super().__eq__(other) and \
               self.storage_space_to_reclaim == other.storage_space_to_reclaim and \
               self.dry_run == other.dry_run and \
               self.delete_snapshot_logs == other.delete_snapshot_logs

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def storage_space_to_reclaim(self):
        """
        Amount of space in bytes to reclaim as part of purgeLogs process.

        :rtype: ``float``
        """
        return self._storage_space_to_reclaim[0]

    @storage_space_to_reclaim.setter
    def storage_space_to_reclaim(self, value):
        self._storage_space_to_reclaim = (value, True)

    @property
    def dry_run(self):
        """
        *(default value: True)* If this is set to true, this operation does not
        actually delete logs. It returns the affected snapshots and truncated
        timeline as if the logs were deleted.

        :rtype: ``bool``
        """
        return self._dry_run[0]

    @dry_run.setter
    def dry_run(self, value):
        self._dry_run = (value, True)

    @property
    def delete_snapshot_logs(self):
        """
        Delete expired logs which have been retained to make snapshots
        consistent.

        :rtype: ``bool``
        """
        return self._delete_snapshot_logs[0]

    @delete_snapshot_logs.setter
    def delete_snapshot_logs(self, value):
        self._delete_snapshot_logs = (value, True)

