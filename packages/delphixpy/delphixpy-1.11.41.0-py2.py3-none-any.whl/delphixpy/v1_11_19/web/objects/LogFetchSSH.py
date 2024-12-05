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
#     /delphix-log-fetch-ssh.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_19.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_19 import factory
from delphixpy.v1_11_19 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class LogFetchSSH(TypedObject):
    """
    *(extends* :py:class:`v1_11_19.web.vo.TypedObject` *)* Parameters to fetch
    log files that apply to a TimeFlow.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("LogFetchSSH", True)
        self._host = (self.__undef__, True)
        self._username = (self.__undef__, True)
        self._credentials = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._directory = (self.__undef__, True)
        self._ssh_verification_strategy = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "host" not in data:
            raise ValueError("Missing required property \"host\".")
        obj._host = (data.get("host", obj.__undef__), dirty)
        if obj._host[0] is not None and obj._host[0] is not obj.__undef__:
            assert isinstance(obj._host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._host[0], type(obj._host[0])))
            common.validate_format(obj._host[0], "None", None, None)
        if "username" not in data:
            raise ValueError("Missing required property \"username\".")
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        if "credentials" in data and data["credentials"] is not None:
            obj._credentials = (factory.create_object(data["credentials"], "Credential"), dirty)
            factory.validate_type(obj._credentials[0], "Credential")
        else:
            obj._credentials = (obj.__undef__, dirty)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        if "directory" not in data:
            raise ValueError("Missing required property \"directory\".")
        obj._directory = (data.get("directory", obj.__undef__), dirty)
        if obj._directory[0] is not None and obj._directory[0] is not obj.__undef__:
            assert isinstance(obj._directory[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._directory[0], type(obj._directory[0])))
            common.validate_format(obj._directory[0], "None", None, None)
        if "sshVerificationStrategy" in data and data["sshVerificationStrategy"] is not None:
            obj._ssh_verification_strategy = (factory.create_object(data["sshVerificationStrategy"], "SshVerificationStrategy"), dirty)
            factory.validate_type(obj._ssh_verification_strategy[0], "SshVerificationStrategy")
        else:
            obj._ssh_verification_strategy = (obj.__undef__, dirty)
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
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]) or self.is_dirty_list(self.username, self._username) or belongs_to_parent)):
            dct["username"] = dictify(self.username)
        if "credentials" == "type" or (self.credentials is not self.__undef__ and (not (dirty and not self._credentials[1]))):
            dct["credentials"] = dictify(self.credentials)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]))):
            dct["port"] = dictify(self.port)
        if "directory" == "type" or (self.directory is not self.__undef__ and (not (dirty and not self._directory[1]) or self.is_dirty_list(self.directory, self._directory) or belongs_to_parent)):
            dct["directory"] = dictify(self.directory)
        if "ssh_verification_strategy" == "type" or (self.ssh_verification_strategy is not self.__undef__ and (not (dirty and not self._ssh_verification_strategy[1]))):
            dct["sshVerificationStrategy"] = dictify(self.ssh_verification_strategy)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._host = (self._host[0], True)
        self._username = (self._username[0], True)
        self._credentials = (self._credentials[0], True)
        self._port = (self._port[0], True)
        self._directory = (self._directory[0], True)
        self._ssh_verification_strategy = (self._ssh_verification_strategy[0], True)

    def is_dirty(self):
        return any([self._host[1], self._username[1], self._credentials[1], self._port[1], self._directory[1], self._ssh_verification_strategy[1]])

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
        if not isinstance(other, LogFetchSSH):
            return False
        return super().__eq__(other) and \
               self.host == other.host and \
               self.username == other.username and \
               self.credentials == other.credentials and \
               self.port == other.port and \
               self.directory == other.directory and \
               self.ssh_verification_strategy == other.ssh_verification_strategy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def host(self):
        """
        Remote host to connect to.

        :rtype: ``str``
        """
        return self._host[0]

    @host.setter
    def host(self, value):
        self._host = (value, True)

    @property
    def username(self):
        """
        User name to authenticate as.

        :rtype: ``str``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def credentials(self):
        """
        User credentials. If not provided, will use the credentials for the
        environment user 'username'.

        :rtype: :py:class:`v1_11_19.web.vo.Credential`
        """
        return self._credentials[0]

    @credentials.setter
    def credentials(self, value):
        self._credentials = (value, True)

    @property
    def port(self):
        """
        *(default value: 22)* SSH port to connect to.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def directory(self):
        """
        Directory on the remote server where the missing log files reside.

        :rtype: ``str``
        """
        return self._directory[0]

    @directory.setter
    def directory(self, value):
        self._directory = (value, True)

    @property
    def ssh_verification_strategy(self):
        """
        Mechanism to use for ssh host verification.

        :rtype: :py:class:`v1_11_19.web.vo.SshVerificationStrategy`
        """
        return self._ssh_verification_strategy[0]

    @ssh_verification_strategy.setter
    def ssh_verification_strategy(self, value):
        self._ssh_verification_strategy = (value, True)

