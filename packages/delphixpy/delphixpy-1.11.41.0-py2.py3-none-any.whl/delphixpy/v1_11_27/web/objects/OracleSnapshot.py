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
#     /delphix-oracle-snapshot.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.TimeflowSnapshot import TimeflowSnapshot
from delphixpy.v1_11_27 import factory
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleSnapshot(TimeflowSnapshot):
    """
    *(extends* :py:class:`v1_11_27.web.vo.TimeflowSnapshot` *)* Provisionable
    snapshot of an Oracle TimeFlow.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleSnapshot", True)
        self._runtime = (self.__undef__, True)
        self._from_physical_standby_vdb = (self.__undef__, True)
        self._first_change_point = (self.__undef__, True)
        self._latest_change_point = (self.__undef__, True)
        self._redo_log_size_in_bytes = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "OracleSnapshotRuntime"), dirty)
            factory.validate_type(obj._runtime[0], "OracleSnapshotRuntime")
        else:
            obj._runtime = (obj.__undef__, dirty)
        obj._from_physical_standby_vdb = (data.get("fromPhysicalStandbyVdb", obj.__undef__), dirty)
        if obj._from_physical_standby_vdb[0] is not None and obj._from_physical_standby_vdb[0] is not obj.__undef__:
            assert isinstance(obj._from_physical_standby_vdb[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._from_physical_standby_vdb[0], type(obj._from_physical_standby_vdb[0])))
            common.validate_format(obj._from_physical_standby_vdb[0], "None", None, None)
        if "firstChangePoint" in data and data["firstChangePoint"] is not None:
            obj._first_change_point = (factory.create_object(data["firstChangePoint"], "OracleTimeflowPoint"), dirty)
            factory.validate_type(obj._first_change_point[0], "OracleTimeflowPoint")
        else:
            obj._first_change_point = (obj.__undef__, dirty)
        if "latestChangePoint" in data and data["latestChangePoint"] is not None:
            obj._latest_change_point = (factory.create_object(data["latestChangePoint"], "OracleTimeflowPoint"), dirty)
            factory.validate_type(obj._latest_change_point[0], "OracleTimeflowPoint")
        else:
            obj._latest_change_point = (obj.__undef__, dirty)
        obj._redo_log_size_in_bytes = (data.get("redoLogSizeInBytes", obj.__undef__), dirty)
        if obj._redo_log_size_in_bytes[0] is not None and obj._redo_log_size_in_bytes[0] is not obj.__undef__:
            assert isinstance(obj._redo_log_size_in_bytes[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._redo_log_size_in_bytes[0], type(obj._redo_log_size_in_bytes[0])))
            common.validate_format(obj._redo_log_size_in_bytes[0], "None", None, None)
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
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        if "from_physical_standby_vdb" == "type" or (self.from_physical_standby_vdb is not self.__undef__ and (not (dirty and not self._from_physical_standby_vdb[1]) or self.is_dirty_list(self.from_physical_standby_vdb, self._from_physical_standby_vdb) or belongs_to_parent)):
            dct["fromPhysicalStandbyVdb"] = dictify(self.from_physical_standby_vdb)
        elif belongs_to_parent and self.from_physical_standby_vdb is self.__undef__:
            dct["fromPhysicalStandbyVdb"] = False
        if "first_change_point" == "type" or (self.first_change_point is not self.__undef__ and (not (dirty and not self._first_change_point[1]))):
            dct["firstChangePoint"] = dictify(self.first_change_point)
        if "latest_change_point" == "type" or (self.latest_change_point is not self.__undef__ and (not (dirty and not self._latest_change_point[1]))):
            dct["latestChangePoint"] = dictify(self.latest_change_point)
        if "redo_log_size_in_bytes" == "type" or (self.redo_log_size_in_bytes is not self.__undef__ and (not (dirty and not self._redo_log_size_in_bytes[1]) or self.is_dirty_list(self.redo_log_size_in_bytes, self._redo_log_size_in_bytes) or belongs_to_parent)):
            dct["redoLogSizeInBytes"] = dictify(self.redo_log_size_in_bytes)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._runtime = (self._runtime[0], True)
        self._from_physical_standby_vdb = (self._from_physical_standby_vdb[0], True)
        self._first_change_point = (self._first_change_point[0], True)
        self._latest_change_point = (self._latest_change_point[0], True)
        self._redo_log_size_in_bytes = (self._redo_log_size_in_bytes[0], True)

    def is_dirty(self):
        return any([self._runtime[1], self._from_physical_standby_vdb[1], self._first_change_point[1], self._latest_change_point[1], self._redo_log_size_in_bytes[1]])

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
        if not isinstance(other, OracleSnapshot):
            return False
        return super().__eq__(other) and \
               self.runtime == other.runtime and \
               self.from_physical_standby_vdb == other.from_physical_standby_vdb and \
               self.first_change_point == other.first_change_point and \
               self.latest_change_point == other.latest_change_point and \
               self.redo_log_size_in_bytes == other.redo_log_size_in_bytes

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def runtime(self):
        """
        Runtime properties of the snapshot.

        :rtype: :py:class:`v1_11_27.web.vo.OracleSnapshotRuntime`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

    @property
    def from_physical_standby_vdb(self):
        """
        True if this snapshot was taken of a standby database.

        :rtype: ``bool``
        """
        return self._from_physical_standby_vdb[0]

    @from_physical_standby_vdb.setter
    def from_physical_standby_vdb(self, value):
        self._from_physical_standby_vdb = (value, True)

    @property
    def first_change_point(self):
        """
        The location within the parent TimeFlow at which this snapshot was
        initiated.

        :rtype: :py:class:`v1_11_27.web.vo.OracleTimeflowPoint`
        """
        return self._first_change_point[0]

    @first_change_point.setter
    def first_change_point(self, value):
        self._first_change_point = (value, True)

    @property
    def latest_change_point(self):
        """
        The location of the snapshot within the parent TimeFlow represented by
        this snapshot.

        :rtype: :py:class:`v1_11_27.web.vo.OracleTimeflowPoint`
        """
        return self._latest_change_point[0]

    @latest_change_point.setter
    def latest_change_point(self, value):
        self._latest_change_point = (value, True)

    @property
    def redo_log_size_in_bytes(self):
        """
        Online redo log size in bytes when this snapshot was taken.

        :rtype: ``int``
        """
        return self._redo_log_size_in_bytes[0]

    @redo_log_size_in_bytes.setter
    def redo_log_size_in_bytes(self, value):
        self._redo_log_size_in_bytes = (value, True)

