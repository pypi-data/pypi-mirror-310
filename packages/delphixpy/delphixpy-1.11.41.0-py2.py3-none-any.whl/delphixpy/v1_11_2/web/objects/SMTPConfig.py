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
#     /delphix-smtp-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_2.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_2 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SMTPConfig(TypedObject):
    """
    *(extends* :py:class:`v1_11_2.web.vo.TypedObject` *)* SMTP configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SMTPConfig", True)
        self._enabled = (self.__undef__, True)
        self._server = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._authentication_enabled = (self.__undef__, True)
        self._tls_enabled = (self.__undef__, True)
        self._username = (self.__undef__, True)
        self._password = (self.__undef__, True)
        self._from_address = (self.__undef__, True)
        self._send_timeout = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._server = (data.get("server", obj.__undef__), dirty)
        if obj._server[0] is not None and obj._server[0] is not obj.__undef__:
            assert isinstance(obj._server[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._server[0], type(obj._server[0])))
            common.validate_format(obj._server[0], "host", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        obj._authentication_enabled = (data.get("authenticationEnabled", obj.__undef__), dirty)
        if obj._authentication_enabled[0] is not None and obj._authentication_enabled[0] is not obj.__undef__:
            assert isinstance(obj._authentication_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._authentication_enabled[0], type(obj._authentication_enabled[0])))
            common.validate_format(obj._authentication_enabled[0], "None", None, None)
        obj._tls_enabled = (data.get("tlsEnabled", obj.__undef__), dirty)
        if obj._tls_enabled[0] is not None and obj._tls_enabled[0] is not obj.__undef__:
            assert isinstance(obj._tls_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._tls_enabled[0], type(obj._tls_enabled[0])))
            common.validate_format(obj._tls_enabled[0], "None", None, None)
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        obj._password = (data.get("password", obj.__undef__), dirty)
        if obj._password[0] is not None and obj._password[0] is not obj.__undef__:
            assert isinstance(obj._password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._password[0], type(obj._password[0])))
            common.validate_format(obj._password[0], "password", None, None)
        obj._from_address = (data.get("fromAddress", obj.__undef__), dirty)
        if obj._from_address[0] is not None and obj._from_address[0] is not obj.__undef__:
            assert isinstance(obj._from_address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._from_address[0], type(obj._from_address[0])))
            common.validate_format(obj._from_address[0], "email", None, None)
        obj._send_timeout = (data.get("sendTimeout", obj.__undef__), dirty)
        if obj._send_timeout[0] is not None and obj._send_timeout[0] is not obj.__undef__:
            assert isinstance(obj._send_timeout[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._send_timeout[0], type(obj._send_timeout[0])))
            common.validate_format(obj._send_timeout[0], "None", None, None)
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
        if "server" == "type" or (self.server is not self.__undef__ and (not (dirty and not self._server[1]) or self.is_dirty_list(self.server, self._server) or belongs_to_parent)):
            dct["server"] = dictify(self.server)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        elif belongs_to_parent and self.port is self.__undef__:
            dct["port"] = -1
        if "authentication_enabled" == "type" or (self.authentication_enabled is not self.__undef__ and (not (dirty and not self._authentication_enabled[1]) or self.is_dirty_list(self.authentication_enabled, self._authentication_enabled) or belongs_to_parent)):
            dct["authenticationEnabled"] = dictify(self.authentication_enabled)
        elif belongs_to_parent and self.authentication_enabled is self.__undef__:
            dct["authenticationEnabled"] = False
        if "tls_enabled" == "type" or (self.tls_enabled is not self.__undef__ and (not (dirty and not self._tls_enabled[1]) or self.is_dirty_list(self.tls_enabled, self._tls_enabled) or belongs_to_parent)):
            dct["tlsEnabled"] = dictify(self.tls_enabled)
        elif belongs_to_parent and self.tls_enabled is self.__undef__:
            dct["tlsEnabled"] = False
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]) or self.is_dirty_list(self.username, self._username) or belongs_to_parent)):
            dct["username"] = dictify(self.username)
        if "password" == "type" or (self.password is not self.__undef__ and (not (dirty and not self._password[1]) or self.is_dirty_list(self.password, self._password) or belongs_to_parent)):
            dct["password"] = dictify(self.password)
        if "from_address" == "type" or (self.from_address is not self.__undef__ and (not (dirty and not self._from_address[1]) or self.is_dirty_list(self.from_address, self._from_address) or belongs_to_parent)):
            dct["fromAddress"] = dictify(self.from_address)
        if "send_timeout" == "type" or (self.send_timeout is not self.__undef__ and (not (dirty and not self._send_timeout[1]) or self.is_dirty_list(self.send_timeout, self._send_timeout) or belongs_to_parent)):
            dct["sendTimeout"] = dictify(self.send_timeout)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._server = (self._server[0], True)
        self._port = (self._port[0], True)
        self._authentication_enabled = (self._authentication_enabled[0], True)
        self._tls_enabled = (self._tls_enabled[0], True)
        self._username = (self._username[0], True)
        self._password = (self._password[0], True)
        self._from_address = (self._from_address[0], True)
        self._send_timeout = (self._send_timeout[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._server[1], self._port[1], self._authentication_enabled[1], self._tls_enabled[1], self._username[1], self._password[1], self._from_address[1], self._send_timeout[1]])

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
        if not isinstance(other, SMTPConfig):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.server == other.server and \
               self.port == other.port and \
               self.authentication_enabled == other.authentication_enabled and \
               self.tls_enabled == other.tls_enabled and \
               self.username == other.username and \
               self.password == other.password and \
               self.from_address == other.from_address and \
               self.send_timeout == other.send_timeout

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        True if outbound email is enabled.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def server(self):
        """
        IP address or hostname of SMTP relay server.

        :rtype: ``str``
        """
        return self._server[0]

    @server.setter
    def server(self, value):
        self._server = (value, True)

    @property
    def port(self):
        """
        *(default value: -1)* Port number to use. A value of -1 indicates the
        default (25 or 587 for TLS).

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def authentication_enabled(self):
        """
        True if username/password authentication should be used.

        :rtype: ``bool``
        """
        return self._authentication_enabled[0]

    @authentication_enabled.setter
    def authentication_enabled(self, value):
        self._authentication_enabled = (value, True)

    @property
    def tls_enabled(self):
        """
        True if TLS (transport layer security) should be used.

        :rtype: ``bool``
        """
        return self._tls_enabled[0]

    @tls_enabled.setter
    def tls_enabled(self, value):
        self._tls_enabled = (value, True)

    @property
    def username(self):
        """
        If authentication is enabled, username to use when authenticating to
        the server.

        :rtype: ``str``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def password(self):
        """
        If authentication is enabled, password to use when authenticating to
        the server.

        :rtype: ``str``
        """
        return self._password[0]

    @password.setter
    def password(self, value):
        self._password = (value, True)

    @property
    def from_address(self):
        """
        From address to use when sending mail. If unspecified,
        'noreply@delphix.com' is used.

        :rtype: ``str``
        """
        return self._from_address[0]

    @from_address.setter
    def from_address(self, value):
        self._from_address = (value, True)

    @property
    def send_timeout(self):
        """
        Maximum timeout to wait, in seconds, when sending mail.

        :rtype: ``int``
        """
        return self._send_timeout[0]

    @send_timeout.setter
    def send_timeout(self, value):
        self._send_timeout = (value, True)

