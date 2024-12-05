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
#     /delphix-proxy-configuration.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_4.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_4 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ProxyConfiguration(TypedObject):
    """
    *(extends* :py:class:`v1_11_4.web.vo.TypedObject` *)* Proxy configuration
    for a specific protocol.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ProxyConfiguration", True)
        self._enabled = (self.__undef__, True)
        self._host = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._username = (self.__undef__, True)
        self._password = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._host = (data.get("host", obj.__undef__), dirty)
        if obj._host[0] is not None and obj._host[0] is not obj.__undef__:
            assert isinstance(obj._host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._host[0], type(obj._host[0])))
            common.validate_format(obj._host[0], "host", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        obj._password = (data.get("password", obj.__undef__), dirty)
        if obj._password[0] is not None and obj._password[0] is not obj.__undef__:
            assert isinstance(obj._password[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._password[0], type(obj._password[0])))
            common.validate_format(obj._password[0], "password", None, None)
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
        if "enabled" == "type" or (self.enabled is not self.__undef__ and (not (dirty and not self._enabled[1]) or self.is_dirty_list(self.enabled, self._enabled) or belongs_to_parent)):
            dct["enabled"] = dictify(self.enabled)
        if "host" == "type" or (self.host is not self.__undef__ and (not (dirty and not self._host[1]) or self.is_dirty_list(self.host, self._host) or belongs_to_parent)):
            dct["host"] = dictify(self.host)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]) or self.is_dirty_list(self.username, self._username) or belongs_to_parent)):
            dct["username"] = dictify(self.username)
        if "password" == "type" or (self.password is not self.__undef__ and (not (dirty and not self._password[1]) or self.is_dirty_list(self.password, self._password) or belongs_to_parent)):
            dct["password"] = dictify(self.password)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._host = (self._host[0], True)
        self._port = (self._port[0], True)
        self._username = (self._username[0], True)
        self._password = (self._password[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._host[1], self._port[1], self._username[1], self._password[1]])

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
        if not isinstance(other, ProxyConfiguration):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.host == other.host and \
               self.port == other.port and \
               self.username == other.username and \
               self.password == other.password

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        True if the proxy is enabled.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def host(self):
        """
        Host or IP address to use as proxy.

        :rtype: ``str``
        """
        return self._host[0]

    @host.setter
    def host(self, value):
        self._host = (value, True)

    @property
    def port(self):
        """
        Port to use when connecting to the proxy host.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def username(self):
        """
        If authentication is required, the username to use when connecting to
        the proxy.

        :rtype: ``str`` *or* ``null``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def password(self):
        """
        If authentication is required, the password to use when connecting to
        the proxy.

        :rtype: ``str`` *or* ``null``
        """
        return self._password[0]

    @password.setter
    def password(self, value):
        self._password = (value, True)

