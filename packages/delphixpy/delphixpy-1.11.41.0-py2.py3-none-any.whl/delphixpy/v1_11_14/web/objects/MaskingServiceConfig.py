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
#     /delphix-masking-service-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.UserObject import UserObject
from delphixpy.v1_11_14 import factory
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MaskingServiceConfig(UserObject):
    """
    *(extends* :py:class:`v1_11_14.web.vo.UserObject` *)* Configuration for the
    Masking Service this Engine communicates with.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MaskingServiceConfig", True)
        self._name = (self.__undef__, True)
        self._server = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._username = (self.__undef__, True)
        self._credentials = (self.__undef__, True)
        self._scheme = (self.__undef__, True)
        self._max_job_fetch_count = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, 256)
        obj._server = (data.get("server", obj.__undef__), dirty)
        if obj._server[0] is not None and obj._server[0] is not obj.__undef__:
            assert isinstance(obj._server[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._server[0], type(obj._server[0])))
            common.validate_format(obj._server[0], "host", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        if "credentials" in data and data["credentials"] is not None:
            obj._credentials = (factory.create_object(data["credentials"], "Credential"), dirty)
            factory.validate_type(obj._credentials[0], "Credential")
        else:
            obj._credentials = (obj.__undef__, dirty)
        obj._scheme = (data.get("scheme", obj.__undef__), dirty)
        if obj._scheme[0] is not None and obj._scheme[0] is not obj.__undef__:
            assert isinstance(obj._scheme[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._scheme[0], type(obj._scheme[0])))
            assert obj._scheme[0] in ['HTTP', 'HTTPS'], "Expected enum ['HTTP', 'HTTPS'] but got %s" % obj._scheme[0]
            common.validate_format(obj._scheme[0], "None", None, None)
        obj._max_job_fetch_count = (data.get("maxJobFetchCount", obj.__undef__), dirty)
        if obj._max_job_fetch_count[0] is not None and obj._max_job_fetch_count[0] is not obj.__undef__:
            assert isinstance(obj._max_job_fetch_count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._max_job_fetch_count[0], type(obj._max_job_fetch_count[0])))
            common.validate_format(obj._max_job_fetch_count[0], "None", None, None)
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
        if "server" == "type" or (self.server is not self.__undef__ and (not (dirty and not self._server[1]) or self.is_dirty_list(self.server, self._server) or belongs_to_parent)):
            dct["server"] = dictify(self.server)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]) or self.is_dirty_list(self.username, self._username) or belongs_to_parent)):
            dct["username"] = dictify(self.username)
        if "credentials" == "type" or (self.credentials is not self.__undef__ and (not (dirty and not self._credentials[1]) or self.is_dirty_list(self.credentials, self._credentials) or belongs_to_parent)):
            dct["credentials"] = dictify(self.credentials, prop_is_list_or_vo=True)
        if "scheme" == "type" or (self.scheme is not self.__undef__ and (not (dirty and not self._scheme[1]) or self.is_dirty_list(self.scheme, self._scheme) or belongs_to_parent)):
            dct["scheme"] = dictify(self.scheme)
        if "max_job_fetch_count" == "type" or (self.max_job_fetch_count is not self.__undef__ and (not (dirty and not self._max_job_fetch_count[1]) or self.is_dirty_list(self.max_job_fetch_count, self._max_job_fetch_count) or belongs_to_parent)):
            dct["maxJobFetchCount"] = dictify(self.max_job_fetch_count)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._server = (self._server[0], True)
        self._port = (self._port[0], True)
        self._username = (self._username[0], True)
        self._credentials = (self._credentials[0], True)
        self._scheme = (self._scheme[0], True)
        self._max_job_fetch_count = (self._max_job_fetch_count[0], True)

    def is_dirty(self):
        return any([self._name[1], self._server[1], self._port[1], self._username[1], self._credentials[1], self._scheme[1], self._max_job_fetch_count[1]])

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
        if not isinstance(other, MaskingServiceConfig):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.server == other.server and \
               self.port == other.port and \
               self.username == other.username and \
               self.credentials == other.credentials and \
               self.scheme == other.scheme and \
               self.max_job_fetch_count == other.max_job_fetch_count

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        Object name.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def server(self):
        """
        IP address or hostname of server hosting Masking Service.

        :rtype: ``str``
        """
        return self._server[0]

    @server.setter
    def server(self, value):
        self._server = (value, True)

    @property
    def port(self):
        """
        Port number to use.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def username(self):
        """
        Username to use when authenticating to the server.

        :rtype: ``str``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def credentials(self):
        """
        Password to use when authenticating to the server.

        :rtype: :py:class:`v1_11_14.web.vo.Credential`
        """
        return self._credentials[0]

    @credentials.setter
    def credentials(self, value):
        self._credentials = (value, True)

    @property
    def scheme(self):
        """
        Protocol scheme for use when communicating with server. *(permitted
        values: HTTP, HTTPS)*

        :rtype: ``str``
        """
        return self._scheme[0]

    @scheme.setter
    def scheme(self, value):
        self._scheme = (value, True)

    @property
    def max_job_fetch_count(self):
        """
        Maximum number of jobs to fetch from masking service. Defaults to 500.

        :rtype: ``int``
        """
        return self._max_job_fetch_count[0]

    @max_job_fetch_count.setter
    def max_job_fetch_count(self, value):
        self._max_job_fetch_count = (value, True)

