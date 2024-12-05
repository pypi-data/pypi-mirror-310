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
#     /delphix-mssql-snapshot.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TimeflowSnapshot import TimeflowSnapshot
from delphixpy.v1_11_36 import factory
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlSnapshot(TimeflowSnapshot):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TimeflowSnapshot` *)* Provisionable
    snapshot of a MSSQL TimeFlow.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlSnapshot", True)
        self._internal_version = (self.__undef__, True)
        self._runtime = (self.__undef__, True)
        self._backup_set_uuid = (self.__undef__, True)
        self._first_change_point = (self.__undef__, True)
        self._latest_change_point = (self.__undef__, True)
        self._backup_software_type = (self.__undef__, True)
        self._backup_location_type = (self.__undef__, True)
        self._empty_snapshot = (self.__undef__, True)
        self._additional_database_parameters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._internal_version = (data.get("internalVersion", obj.__undef__), dirty)
        if obj._internal_version[0] is not None and obj._internal_version[0] is not obj.__undef__:
            assert isinstance(obj._internal_version[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._internal_version[0], type(obj._internal_version[0])))
            common.validate_format(obj._internal_version[0], "None", None, None)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "MSSqlSnapshotRuntime"), dirty)
            factory.validate_type(obj._runtime[0], "MSSqlSnapshotRuntime")
        else:
            obj._runtime = (obj.__undef__, dirty)
        obj._backup_set_uuid = (data.get("backupSetUUID", obj.__undef__), dirty)
        if obj._backup_set_uuid[0] is not None and obj._backup_set_uuid[0] is not obj.__undef__:
            assert isinstance(obj._backup_set_uuid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._backup_set_uuid[0], type(obj._backup_set_uuid[0])))
            common.validate_format(obj._backup_set_uuid[0], "None", None, None)
        if "firstChangePoint" in data and data["firstChangePoint"] is not None:
            obj._first_change_point = (factory.create_object(data["firstChangePoint"], "MSSqlTimeflowPoint"), dirty)
            factory.validate_type(obj._first_change_point[0], "MSSqlTimeflowPoint")
        else:
            obj._first_change_point = (obj.__undef__, dirty)
        if "latestChangePoint" in data and data["latestChangePoint"] is not None:
            obj._latest_change_point = (factory.create_object(data["latestChangePoint"], "MSSqlTimeflowPoint"), dirty)
            factory.validate_type(obj._latest_change_point[0], "MSSqlTimeflowPoint")
        else:
            obj._latest_change_point = (obj.__undef__, dirty)
        obj._backup_software_type = (data.get("backupSoftwareType", obj.__undef__), dirty)
        if obj._backup_software_type[0] is not None and obj._backup_software_type[0] is not obj.__undef__:
            assert isinstance(obj._backup_software_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._backup_software_type[0], type(obj._backup_software_type[0])))
            assert obj._backup_software_type[0] in ['NATIVE', 'LITESPEED', 'REDGATE', 'NETBACKUP', 'COMMVAULT'], "Expected enum ['NATIVE', 'LITESPEED', 'REDGATE', 'NETBACKUP', 'COMMVAULT'] but got %s" % obj._backup_software_type[0]
            common.validate_format(obj._backup_software_type[0], "None", None, None)
        obj._backup_location_type = (data.get("backupLocationType", obj.__undef__), dirty)
        if obj._backup_location_type[0] is not None and obj._backup_location_type[0] is not obj.__undef__:
            assert isinstance(obj._backup_location_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._backup_location_type[0], type(obj._backup_location_type[0])))
            assert obj._backup_location_type[0] in ['DISK', 'AZURE', 'BACKUP_SERVER'], "Expected enum ['DISK', 'AZURE', 'BACKUP_SERVER'] but got %s" % obj._backup_location_type[0]
            common.validate_format(obj._backup_location_type[0], "None", None, None)
        obj._empty_snapshot = (data.get("emptySnapshot", obj.__undef__), dirty)
        if obj._empty_snapshot[0] is not None and obj._empty_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._empty_snapshot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._empty_snapshot[0], type(obj._empty_snapshot[0])))
            common.validate_format(obj._empty_snapshot[0], "None", None, None)
        if "additionalDatabaseParameters" in data and data["additionalDatabaseParameters"] is not None:
            obj._additional_database_parameters = (factory.create_object(data["additionalDatabaseParameters"], "MSSqlAdditionalDatabaseParameters"), dirty)
            factory.validate_type(obj._additional_database_parameters[0], "MSSqlAdditionalDatabaseParameters")
        else:
            obj._additional_database_parameters = (obj.__undef__, dirty)
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
        if "internal_version" == "type" or (self.internal_version is not self.__undef__ and (not (dirty and not self._internal_version[1]))):
            dct["internalVersion"] = dictify(self.internal_version)
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        if "backup_set_uuid" == "type" or (self.backup_set_uuid is not self.__undef__ and (not (dirty and not self._backup_set_uuid[1]))):
            dct["backupSetUUID"] = dictify(self.backup_set_uuid)
        if "first_change_point" == "type" or (self.first_change_point is not self.__undef__ and (not (dirty and not self._first_change_point[1]))):
            dct["firstChangePoint"] = dictify(self.first_change_point)
        if "latest_change_point" == "type" or (self.latest_change_point is not self.__undef__ and (not (dirty and not self._latest_change_point[1]))):
            dct["latestChangePoint"] = dictify(self.latest_change_point)
        if "backup_software_type" == "type" or (self.backup_software_type is not self.__undef__ and (not (dirty and not self._backup_software_type[1]))):
            dct["backupSoftwareType"] = dictify(self.backup_software_type)
        if dirty and "backupSoftwareType" in dct:
            del dct["backupSoftwareType"]
        if "backup_location_type" == "type" or (self.backup_location_type is not self.__undef__ and (not (dirty and not self._backup_location_type[1]))):
            dct["backupLocationType"] = dictify(self.backup_location_type)
        if dirty and "backupLocationType" in dct:
            del dct["backupLocationType"]
        if "empty_snapshot" == "type" or (self.empty_snapshot is not self.__undef__ and (not (dirty and not self._empty_snapshot[1]))):
            dct["emptySnapshot"] = dictify(self.empty_snapshot)
        if dirty and "emptySnapshot" in dct:
            del dct["emptySnapshot"]
        if "additional_database_parameters" == "type" or (self.additional_database_parameters is not self.__undef__ and (not (dirty and not self._additional_database_parameters[1]))):
            dct["additionalDatabaseParameters"] = dictify(self.additional_database_parameters)
        if dirty and "additionalDatabaseParameters" in dct:
            del dct["additionalDatabaseParameters"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._internal_version = (self._internal_version[0], True)
        self._runtime = (self._runtime[0], True)
        self._backup_set_uuid = (self._backup_set_uuid[0], True)
        self._first_change_point = (self._first_change_point[0], True)
        self._latest_change_point = (self._latest_change_point[0], True)
        self._backup_software_type = (self._backup_software_type[0], True)
        self._backup_location_type = (self._backup_location_type[0], True)
        self._empty_snapshot = (self._empty_snapshot[0], True)
        self._additional_database_parameters = (self._additional_database_parameters[0], True)

    def is_dirty(self):
        return any([self._internal_version[1], self._runtime[1], self._backup_set_uuid[1], self._first_change_point[1], self._latest_change_point[1], self._backup_software_type[1], self._backup_location_type[1], self._empty_snapshot[1], self._additional_database_parameters[1]])

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
        if not isinstance(other, MSSqlSnapshot):
            return False
        return super().__eq__(other) and \
               self.internal_version == other.internal_version and \
               self.runtime == other.runtime and \
               self.backup_set_uuid == other.backup_set_uuid and \
               self.first_change_point == other.first_change_point and \
               self.latest_change_point == other.latest_change_point and \
               self.backup_software_type == other.backup_software_type and \
               self.backup_location_type == other.backup_location_type and \
               self.empty_snapshot == other.empty_snapshot and \
               self.additional_database_parameters == other.additional_database_parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def internal_version(self):
        """
        Internal version of the source database at the time the snapshot was
        taken.

        :rtype: ``int``
        """
        return self._internal_version[0]

    @internal_version.setter
    def internal_version(self, value):
        self._internal_version = (value, True)

    @property
    def runtime(self):
        """
        Runtime properties of the snapshot.

        :rtype: :py:class:`v1_11_36.web.vo.MSSqlSnapshotRuntime`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

    @property
    def backup_set_uuid(self):
        """
        UUID of the source database backup that was restored for this snapshot.

        :rtype: ``str``
        """
        return self._backup_set_uuid[0]

    @backup_set_uuid.setter
    def backup_set_uuid(self, value):
        self._backup_set_uuid = (value, True)

    @property
    def first_change_point(self):
        """
        The location within the parent TimeFlow at which this snapshot was
        initiated.

        :rtype: :py:class:`v1_11_36.web.vo.MSSqlTimeflowPoint`
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

        :rtype: :py:class:`v1_11_36.web.vo.MSSqlTimeflowPoint`
        """
        return self._latest_change_point[0]

    @latest_change_point.setter
    def latest_change_point(self, value):
        self._latest_change_point = (value, True)

    @property
    def backup_software_type(self):
        """
        Backup software used to restore the source database backup for this
        snapshot. *(permitted values: NATIVE, LITESPEED, REDGATE, NETBACKUP,
        COMMVAULT)*

        :rtype: ``str``
        """
        return self._backup_software_type[0]

    @property
    def backup_location_type(self):
        """
        The type of backup location where the source database backup was
        present. *(permitted values: DISK, AZURE, BACKUP_SERVER)*

        :rtype: ``str``
        """
        return self._backup_location_type[0]

    @property
    def empty_snapshot(self):
        """
        True if the staging push dSource snapshot is empty.

        :rtype: ``bool``
        """
        return self._empty_snapshot[0]

    @property
    def additional_database_parameters(self):
        """
        Collection of all the parameters that are not inherited during
        provisioning of a vdb.

        :rtype: :py:class:`v1_11_36.web.vo.MSSqlAdditionalDatabaseParameters`
        """
        return self._additional_database_parameters[0]

