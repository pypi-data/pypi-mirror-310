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
#     /delphix-oracle-provision-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_15.web.objects.OracleBaseProvisionParameters import OracleBaseProvisionParameters
from delphixpy.v1_11_15 import factory
from delphixpy.v1_11_15 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleProvisionParameters(OracleBaseProvisionParameters):
    """
    *(extends* :py:class:`v1_11_15.web.vo.OracleBaseProvisionParameters` *)*
    The parameters to use as input to provision Oracle (non-multitenant)
    databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleProvisionParameters", True)
        self._source_config = (self.__undef__, True)
        self._open_resetlogs = (self.__undef__, True)
        self._physical_standby = (self.__undef__, True)
        self._new_dbid = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "sourceConfig" not in data:
            raise ValueError("Missing required property \"sourceConfig\".")
        if "sourceConfig" in data and data["sourceConfig"] is not None:
            obj._source_config = (factory.create_object(data["sourceConfig"], "OracleDBConfig"), dirty)
            factory.validate_type(obj._source_config[0], "OracleDBConfig")
        else:
            obj._source_config = (obj.__undef__, dirty)
        obj._open_resetlogs = (data.get("openResetlogs", obj.__undef__), dirty)
        if obj._open_resetlogs[0] is not None and obj._open_resetlogs[0] is not obj.__undef__:
            assert isinstance(obj._open_resetlogs[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._open_resetlogs[0], type(obj._open_resetlogs[0])))
            common.validate_format(obj._open_resetlogs[0], "None", None, None)
        obj._physical_standby = (data.get("physicalStandby", obj.__undef__), dirty)
        if obj._physical_standby[0] is not None and obj._physical_standby[0] is not obj.__undef__:
            assert isinstance(obj._physical_standby[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._physical_standby[0], type(obj._physical_standby[0])))
            common.validate_format(obj._physical_standby[0], "None", None, None)
        obj._new_dbid = (data.get("newDBID", obj.__undef__), dirty)
        if obj._new_dbid[0] is not None and obj._new_dbid[0] is not obj.__undef__:
            assert isinstance(obj._new_dbid[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._new_dbid[0], type(obj._new_dbid[0])))
            common.validate_format(obj._new_dbid[0], "None", None, None)
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
        if "source_config" == "type" or (self.source_config is not self.__undef__ and (not (dirty and not self._source_config[1]) or self.is_dirty_list(self.source_config, self._source_config) or belongs_to_parent)):
            dct["sourceConfig"] = dictify(self.source_config, prop_is_list_or_vo=True)
        if "open_resetlogs" == "type" or (self.open_resetlogs is not self.__undef__ and (not (dirty and not self._open_resetlogs[1]) or self.is_dirty_list(self.open_resetlogs, self._open_resetlogs) or belongs_to_parent)):
            dct["openResetlogs"] = dictify(self.open_resetlogs)
        elif belongs_to_parent and self.open_resetlogs is self.__undef__:
            dct["openResetlogs"] = True
        if "physical_standby" == "type" or (self.physical_standby is not self.__undef__ and (not (dirty and not self._physical_standby[1]) or self.is_dirty_list(self.physical_standby, self._physical_standby) or belongs_to_parent)):
            dct["physicalStandby"] = dictify(self.physical_standby)
        elif belongs_to_parent and self.physical_standby is self.__undef__:
            dct["physicalStandby"] = False
        if "new_dbid" == "type" or (self.new_dbid is not self.__undef__ and (not (dirty and not self._new_dbid[1]) or self.is_dirty_list(self.new_dbid, self._new_dbid) or belongs_to_parent)):
            dct["newDBID"] = dictify(self.new_dbid)
        elif belongs_to_parent and self.new_dbid is self.__undef__:
            dct["newDBID"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._source_config = (self._source_config[0], True)
        self._open_resetlogs = (self._open_resetlogs[0], True)
        self._physical_standby = (self._physical_standby[0], True)
        self._new_dbid = (self._new_dbid[0], True)

    def is_dirty(self):
        return any([self._source_config[1], self._open_resetlogs[1], self._physical_standby[1], self._new_dbid[1]])

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
        if not isinstance(other, OracleProvisionParameters):
            return False
        return super().__eq__(other) and \
               self.source_config == other.source_config and \
               self.open_resetlogs == other.open_resetlogs and \
               self.physical_standby == other.physical_standby and \
               self.new_dbid == other.new_dbid

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def source_config(self):
        """
        The source config including dynamically discovered attributes of the
        source.

        :rtype: :py:class:`v1_11_15.web.vo.OracleDBConfig`
        """
        return self._source_config[0]

    @source_config.setter
    def source_config(self, value):
        self._source_config = (value, True)

    @property
    def open_resetlogs(self):
        """
        *(default value: True)* Flag indicating whether to open the database
        after provision.

        :rtype: ``bool``
        """
        return self._open_resetlogs[0]

    @open_resetlogs.setter
    def open_resetlogs(self, value):
        self._open_resetlogs = (value, True)

    @property
    def physical_standby(self):
        """
        Flag indicating whether the virtual database is provisioned as a
        physical standby database.

        :rtype: ``bool``
        """
        return self._physical_standby[0]

    @physical_standby.setter
    def physical_standby(self, value):
        self._physical_standby = (value, True)

    @property
    def new_dbid(self):
        """
        Flag indicating whether to generate a new DBID for the provisioned
        database.

        :rtype: ``bool``
        """
        return self._new_dbid[0]

    @new_dbid.setter
    def new_dbid(self, value):
        self._new_dbid = (value, True)

