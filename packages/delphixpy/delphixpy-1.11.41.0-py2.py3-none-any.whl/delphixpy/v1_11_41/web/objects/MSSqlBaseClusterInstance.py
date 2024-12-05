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
#     /delphix-mssql-base-cluster-instance.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_41.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_41 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlBaseClusterInstance(TypedObject):
    """
    *(extends* :py:class:`v1_11_41.web.vo.TypedObject` *)* The representation
    of a SQL Server Instance on a clustered node.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlBaseClusterInstance", True)
        self._name = (self.__undef__, True)
        self._version = (self.__undef__, True)
        self._instance_owner = (self.__undef__, True)
        self._server_name = (self.__undef__, True)
        self._node = (self.__undef__, True)
        self._port = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, 16)
        obj._version = (data.get("version", obj.__undef__), dirty)
        if obj._version[0] is not None and obj._version[0] is not obj.__undef__:
            assert isinstance(obj._version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._version[0], type(obj._version[0])))
            common.validate_format(obj._version[0], "None", None, None)
        obj._instance_owner = (data.get("instanceOwner", obj.__undef__), dirty)
        if obj._instance_owner[0] is not None and obj._instance_owner[0] is not obj.__undef__:
            assert isinstance(obj._instance_owner[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._instance_owner[0], type(obj._instance_owner[0])))
            common.validate_format(obj._instance_owner[0], "None", None, None)
        obj._server_name = (data.get("serverName", obj.__undef__), dirty)
        if obj._server_name[0] is not None and obj._server_name[0] is not obj.__undef__:
            assert isinstance(obj._server_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._server_name[0], type(obj._server_name[0])))
            common.validate_format(obj._server_name[0], "None", None, None)
        obj._node = (data.get("node", obj.__undef__), dirty)
        if obj._node[0] is not None and obj._node[0] is not obj.__undef__:
            assert isinstance(obj._node[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._node[0], type(obj._node[0])))
            common.validate_format(obj._node[0], "objectReference", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]))):
            dct["name"] = dictify(self.name)
        if "version" == "type" or (self.version is not self.__undef__ and (not (dirty and not self._version[1]))):
            dct["version"] = dictify(self.version)
        if "instance_owner" == "type" or (self.instance_owner is not self.__undef__ and (not (dirty and not self._instance_owner[1]))):
            dct["instanceOwner"] = dictify(self.instance_owner)
        if "server_name" == "type" or (self.server_name is not self.__undef__ and (not (dirty and not self._server_name[1]))):
            dct["serverName"] = dictify(self.server_name)
        if "node" == "type" or (self.node is not self.__undef__ and (not (dirty and not self._node[1]))):
            dct["node"] = dictify(self.node)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]))):
            dct["port"] = dictify(self.port)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._version = (self._version[0], True)
        self._instance_owner = (self._instance_owner[0], True)
        self._server_name = (self._server_name[0], True)
        self._node = (self._node[0], True)
        self._port = (self._port[0], True)

    def is_dirty(self):
        return any([self._name[1], self._version[1], self._instance_owner[1], self._server_name[1], self._node[1], self._port[1]])

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
        if not isinstance(other, MSSqlBaseClusterInstance):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.version == other.version and \
               self.instance_owner == other.instance_owner and \
               self.server_name == other.server_name and \
               self.node == other.node and \
               self.port == other.port

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        The name of the SQL Server Instance.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def version(self):
        """
        The version of the SQL Server Instance.

        :rtype: ``str``
        """
        return self._version[0]

    @version.setter
    def version(self, value):
        self._version = (value, True)

    @property
    def instance_owner(self):
        """
        The owner of the SQL Server Instance.

        :rtype: ``str``
        """
        return self._instance_owner[0]

    @instance_owner.setter
    def instance_owner(self, value):
        self._instance_owner = (value, True)

    @property
    def server_name(self):
        """
        The Servername of the SQL Server Instance.

        :rtype: ``str``
        """
        return self._server_name[0]

    @server_name.setter
    def server_name(self, value):
        self._server_name = (value, True)

    @property
    def node(self):
        """
        A reference to the Windows Cluster Node for this instance.

        :rtype: ``str``
        """
        return self._node[0]

    @node.setter
    def node(self, value):
        self._node = (value, True)

    @property
    def port(self):
        """
        The port to connect to the SQL Server Instance.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

