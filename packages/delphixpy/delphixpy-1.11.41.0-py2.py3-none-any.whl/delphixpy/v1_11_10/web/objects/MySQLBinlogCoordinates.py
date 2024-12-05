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
#     /delphix-mysql-binlog-coordinates.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_10.web.objects.MySQLReplicationCoordinates import MySQLReplicationCoordinates
from delphixpy.v1_11_10 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MySQLBinlogCoordinates(MySQLReplicationCoordinates):
    """
    *(extends* :py:class:`v1_11_10.web.vo.MySQLReplicationCoordinates` *)* The
    current position in the master binary logs when a MySQL backup was taken.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MySQLBinlogCoordinates", True)
        self._master_log_name = (self.__undef__, True)
        self._master_log_pos = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "masterLogName" not in data:
            raise ValueError("Missing required property \"masterLogName\".")
        obj._master_log_name = (data.get("masterLogName", obj.__undef__), dirty)
        if obj._master_log_name[0] is not None and obj._master_log_name[0] is not obj.__undef__:
            assert isinstance(obj._master_log_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._master_log_name[0], type(obj._master_log_name[0])))
            common.validate_format(obj._master_log_name[0], "None", None, None)
        if "masterLogPos" not in data:
            raise ValueError("Missing required property \"masterLogPos\".")
        obj._master_log_pos = (data.get("masterLogPos", obj.__undef__), dirty)
        if obj._master_log_pos[0] is not None and obj._master_log_pos[0] is not obj.__undef__:
            assert isinstance(obj._master_log_pos[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._master_log_pos[0], type(obj._master_log_pos[0])))
            common.validate_format(obj._master_log_pos[0], "None", None, None)
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
        if "master_log_name" == "type" or (self.master_log_name is not self.__undef__ and (not (dirty and not self._master_log_name[1]) or self.is_dirty_list(self.master_log_name, self._master_log_name) or belongs_to_parent)):
            dct["masterLogName"] = dictify(self.master_log_name)
        if "master_log_pos" == "type" or (self.master_log_pos is not self.__undef__ and (not (dirty and not self._master_log_pos[1]) or self.is_dirty_list(self.master_log_pos, self._master_log_pos) or belongs_to_parent)):
            dct["masterLogPos"] = dictify(self.master_log_pos)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._master_log_name = (self._master_log_name[0], True)
        self._master_log_pos = (self._master_log_pos[0], True)

    def is_dirty(self):
        return any([self._master_log_name[1], self._master_log_pos[1]])

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
        if not isinstance(other, MySQLBinlogCoordinates):
            return False
        return super().__eq__(other) and \
               self.master_log_name == other.master_log_name and \
               self.master_log_pos == other.master_log_pos

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def master_log_name(self):
        """
        Name of the master log file to start replication from.

        :rtype: ``str``
        """
        return self._master_log_name[0]

    @master_log_name.setter
    def master_log_name(self, value):
        self._master_log_name = (value, True)

    @property
    def master_log_pos(self):
        """
        Position within the master log file to start replication from.

        :rtype: ``int``
        """
        return self._master_log_pos[0]

    @master_log_pos.setter
    def master_log_pos(self, value):
        self._master_log_pos = (value, True)

