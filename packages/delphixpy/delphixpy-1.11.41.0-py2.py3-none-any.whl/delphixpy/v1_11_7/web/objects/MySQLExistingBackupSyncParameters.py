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
#     /delphix-mysql-existing-backup-sync-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_7.web.objects.MySQLSyncParameters import MySQLSyncParameters
from delphixpy.v1_11_7 import factory
from delphixpy.v1_11_7 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MySQLExistingBackupSyncParameters(MySQLSyncParameters):
    """
    *(extends* :py:class:`v1_11_7.web.vo.MySQLSyncParameters` *)* The
    parameters to use as input to sync requests for MySQL databases using an
    existing backup.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MySQLExistingBackupSyncParameters", True)
        self._backup_location = (self.__undef__, True)
        self._replication_coordinates = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "backupLocation" not in data:
            raise ValueError("Missing required property \"backupLocation\".")
        obj._backup_location = (data.get("backupLocation", obj.__undef__), dirty)
        if obj._backup_location[0] is not None and obj._backup_location[0] is not obj.__undef__:
            assert isinstance(obj._backup_location[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._backup_location[0], type(obj._backup_location[0])))
            common.validate_format(obj._backup_location[0], "None", None, None)
        if "replicationCoordinates" in data and data["replicationCoordinates"] is not None:
            obj._replication_coordinates = (factory.create_object(data["replicationCoordinates"], "MySQLReplicationCoordinates"), dirty)
            factory.validate_type(obj._replication_coordinates[0], "MySQLReplicationCoordinates")
        else:
            obj._replication_coordinates = (obj.__undef__, dirty)
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
        if "backup_location" == "type" or (self.backup_location is not self.__undef__ and (not (dirty and not self._backup_location[1]) or self.is_dirty_list(self.backup_location, self._backup_location) or belongs_to_parent)):
            dct["backupLocation"] = dictify(self.backup_location)
        if "replication_coordinates" == "type" or (self.replication_coordinates is not self.__undef__ and (not (dirty and not self._replication_coordinates[1]) or self.is_dirty_list(self.replication_coordinates, self._replication_coordinates) or belongs_to_parent)):
            dct["replicationCoordinates"] = dictify(self.replication_coordinates, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._backup_location = (self._backup_location[0], True)
        self._replication_coordinates = (self._replication_coordinates[0], True)

    def is_dirty(self):
        return any([self._backup_location[1], self._replication_coordinates[1]])

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
        if not isinstance(other, MySQLExistingBackupSyncParameters):
            return False
        return super().__eq__(other) and \
               self.backup_location == other.backup_location and \
               self.replication_coordinates == other.replication_coordinates

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def backup_location(self):
        """
        Path to the existing backup to be loaded.

        :rtype: ``str``
        """
        return self._backup_location[0]

    @backup_location.setter
    def backup_location(self, value):
        self._backup_location = (value, True)

    @property
    def replication_coordinates(self):
        """
        The coordinates corresponding to the MySQL backup to start replication
        from.

        :rtype: :py:class:`v1_11_7.web.vo.MySQLReplicationCoordinates`
        """
        return self._replication_coordinates[0]

    @replication_coordinates.setter
    def replication_coordinates(self, value):
        self._replication_coordinates = (value, True)

