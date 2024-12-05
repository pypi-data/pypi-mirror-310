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
#     /delphix-mssql-source-connection-info.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.SourceConnectionInfo import SourceConnectionInfo
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlSourceConnectionInfo(SourceConnectionInfo):
    """
    *(extends* :py:class:`v1_11_34.web.vo.SourceConnectionInfo` *)* Contains
    information that can be used to connect to a SQL server source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlSourceConnectionInfo", True)
        self._host = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._instance_name = (self.__undef__, True)
        self._database_name = (self.__undef__, True)
        self._instance_jdbc_string = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._host = (data.get("host", obj.__undef__), dirty)
        if obj._host[0] is not None and obj._host[0] is not obj.__undef__:
            assert isinstance(obj._host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._host[0], type(obj._host[0])))
            common.validate_format(obj._host[0], "None", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        obj._instance_name = (data.get("instanceName", obj.__undef__), dirty)
        if obj._instance_name[0] is not None and obj._instance_name[0] is not obj.__undef__:
            assert isinstance(obj._instance_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._instance_name[0], type(obj._instance_name[0])))
            common.validate_format(obj._instance_name[0], "None", None, None)
        obj._database_name = (data.get("databaseName", obj.__undef__), dirty)
        if obj._database_name[0] is not None and obj._database_name[0] is not obj.__undef__:
            assert isinstance(obj._database_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._database_name[0], type(obj._database_name[0])))
            common.validate_format(obj._database_name[0], "None", None, None)
        obj._instance_jdbc_string = (data.get("instanceJDBCString", obj.__undef__), dirty)
        if obj._instance_jdbc_string[0] is not None and obj._instance_jdbc_string[0] is not obj.__undef__:
            assert isinstance(obj._instance_jdbc_string[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._instance_jdbc_string[0], type(obj._instance_jdbc_string[0])))
            common.validate_format(obj._instance_jdbc_string[0], "None", None, None)
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
        if "host" == "type" or (self.host is not self.__undef__ and (not (dirty and not self._host[1]))):
            dct["host"] = dictify(self.host)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]))):
            dct["port"] = dictify(self.port)
        if "instance_name" == "type" or (self.instance_name is not self.__undef__ and (not (dirty and not self._instance_name[1]))):
            dct["instanceName"] = dictify(self.instance_name)
        if "database_name" == "type" or (self.database_name is not self.__undef__ and (not (dirty and not self._database_name[1]))):
            dct["databaseName"] = dictify(self.database_name)
        if "instance_jdbc_string" == "type" or (self.instance_jdbc_string is not self.__undef__ and (not (dirty and not self._instance_jdbc_string[1]))):
            dct["instanceJDBCString"] = dictify(self.instance_jdbc_string)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._host = (self._host[0], True)
        self._port = (self._port[0], True)
        self._instance_name = (self._instance_name[0], True)
        self._database_name = (self._database_name[0], True)
        self._instance_jdbc_string = (self._instance_jdbc_string[0], True)

    def is_dirty(self):
        return any([self._host[1], self._port[1], self._instance_name[1], self._database_name[1], self._instance_jdbc_string[1]])

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
        if not isinstance(other, MSSqlSourceConnectionInfo):
            return False
        return super().__eq__(other) and \
               self.host == other.host and \
               self.port == other.port and \
               self.instance_name == other.instance_name and \
               self.database_name == other.database_name and \
               self.instance_jdbc_string == other.instance_jdbc_string

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def host(self):
        """
        The hostname or IP address of the host where the source resides.

        :rtype: ``str``
        """
        return self._host[0]

    @host.setter
    def host(self, value):
        self._host = (value, True)

    @property
    def port(self):
        """
        The port number used to connect to the source.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def instance_name(self):
        """
        The name of the instance.

        :rtype: ``str``
        """
        return self._instance_name[0]

    @instance_name.setter
    def instance_name(self, value):
        self._instance_name = (value, True)

    @property
    def database_name(self):
        """
        The name of the database.

        :rtype: ``str``
        """
        return self._database_name[0]

    @database_name.setter
    def database_name(self, value):
        self._database_name = (value, True)

    @property
    def instance_jdbc_string(self):
        """
        The JDBC string used to connect to the SQL server instance.

        :rtype: ``str``
        """
        return self._instance_jdbc_string[0]

    @instance_jdbc_string.setter
    def instance_jdbc_string(self, value):
        self._instance_jdbc_string = (value, True)

