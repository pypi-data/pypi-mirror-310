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
#     /delphix-ldap-server.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.ReadonlyNamedUserObject import ReadonlyNamedUserObject
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class LdapServer(ReadonlyNamedUserObject):
    """
    *(extends* :py:class:`v1_11_18.web.vo.ReadonlyNamedUserObject` *)* LDAP
    Server Configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("LdapServer", True)
        self._host = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._auth_method = (self.__undef__, True)
        self._use_ssl = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "host" not in data:
            raise ValueError("Missing required property \"host\".")
        obj._host = (data.get("host", obj.__undef__), dirty)
        if obj._host[0] is not None and obj._host[0] is not obj.__undef__:
            assert isinstance(obj._host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._host[0], type(obj._host[0])))
            common.validate_format(obj._host[0], "host", None, None)
        if "port" not in data:
            raise ValueError("Missing required property \"port\".")
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        if "authMethod" not in data:
            raise ValueError("Missing required property \"authMethod\".")
        obj._auth_method = (data.get("authMethod", obj.__undef__), dirty)
        if obj._auth_method[0] is not None and obj._auth_method[0] is not obj.__undef__:
            assert isinstance(obj._auth_method[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._auth_method[0], type(obj._auth_method[0])))
            assert obj._auth_method[0] in ['SIMPLE', 'DIGEST_MD5'], "Expected enum ['SIMPLE', 'DIGEST_MD5'] but got %s" % obj._auth_method[0]
            common.validate_format(obj._auth_method[0], "None", None, None)
        if "useSSL" not in data:
            raise ValueError("Missing required property \"useSSL\".")
        obj._use_ssl = (data.get("useSSL", obj.__undef__), dirty)
        if obj._use_ssl[0] is not None and obj._use_ssl[0] is not obj.__undef__:
            assert isinstance(obj._use_ssl[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._use_ssl[0], type(obj._use_ssl[0])))
            common.validate_format(obj._use_ssl[0], "None", None, None)
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
        if "host" == "type" or (self.host is not self.__undef__ and (not (dirty and not self._host[1]) or self.is_dirty_list(self.host, self._host) or belongs_to_parent)):
            dct["host"] = dictify(self.host)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        if "auth_method" == "type" or (self.auth_method is not self.__undef__ and (not (dirty and not self._auth_method[1]) or self.is_dirty_list(self.auth_method, self._auth_method) or belongs_to_parent)):
            dct["authMethod"] = dictify(self.auth_method)
        if "use_ssl" == "type" or (self.use_ssl is not self.__undef__ and (not (dirty and not self._use_ssl[1]) or self.is_dirty_list(self.use_ssl, self._use_ssl) or belongs_to_parent)):
            dct["useSSL"] = dictify(self.use_ssl)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._host = (self._host[0], True)
        self._port = (self._port[0], True)
        self._auth_method = (self._auth_method[0], True)
        self._use_ssl = (self._use_ssl[0], True)

    def is_dirty(self):
        return any([self._host[1], self._port[1], self._auth_method[1], self._use_ssl[1]])

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
        if not isinstance(other, LdapServer):
            return False
        return super().__eq__(other) and \
               self.host == other.host and \
               self.port == other.port and \
               self.auth_method == other.auth_method and \
               self.use_ssl == other.use_ssl

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def host(self):
        """
        LDAP server host name.

        :rtype: ``str``
        """
        return self._host[0]

    @host.setter
    def host(self, value):
        self._host = (value, True)

    @property
    def port(self):
        """
        LDAP server port.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def auth_method(self):
        """
        LDAP authentication method. *(permitted values: SIMPLE, DIGEST_MD5)*

        :rtype: ``str``
        """
        return self._auth_method[0]

    @auth_method.setter
    def auth_method(self, value):
        self._auth_method = (value, True)

    @property
    def use_ssl(self):
        """
        Authenticate using SSL.

        :rtype: ``bool``
        """
        return self._use_ssl[0]

    @use_ssl.setter
    def use_ssl(self, value):
        self._use_ssl = (value, True)

