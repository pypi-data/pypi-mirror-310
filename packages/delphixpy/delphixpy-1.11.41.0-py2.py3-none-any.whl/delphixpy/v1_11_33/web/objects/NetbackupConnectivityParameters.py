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
#     /delphix-netbackup-connectivity-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_33.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_33 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class NetbackupConnectivityParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_33.web.vo.TypedObject` *)* Parameters needed to
    test NetBackup connectivity on an environment.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("NetbackupConnectivityParameters", True)
        self._environment = (self.__undef__, True)
        self._environment_user = (self.__undef__, True)
        self._master_server_name = (self.__undef__, True)
        self._source_client_name = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "environment" not in data:
            raise ValueError("Missing required property \"environment\".")
        obj._environment = (data.get("environment", obj.__undef__), dirty)
        if obj._environment[0] is not None and obj._environment[0] is not obj.__undef__:
            assert isinstance(obj._environment[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._environment[0], type(obj._environment[0])))
            common.validate_format(obj._environment[0], "objectReference", None, None)
        if "environmentUser" not in data:
            raise ValueError("Missing required property \"environmentUser\".")
        obj._environment_user = (data.get("environmentUser", obj.__undef__), dirty)
        if obj._environment_user[0] is not None and obj._environment_user[0] is not obj.__undef__:
            assert isinstance(obj._environment_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._environment_user[0], type(obj._environment_user[0])))
            common.validate_format(obj._environment_user[0], "objectReference", None, None)
        if "masterServerName" not in data:
            raise ValueError("Missing required property \"masterServerName\".")
        obj._master_server_name = (data.get("masterServerName", obj.__undef__), dirty)
        if obj._master_server_name[0] is not None and obj._master_server_name[0] is not obj.__undef__:
            assert isinstance(obj._master_server_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._master_server_name[0], type(obj._master_server_name[0])))
            common.validate_format(obj._master_server_name[0], "None", None, None)
        if "sourceClientName" not in data:
            raise ValueError("Missing required property \"sourceClientName\".")
        obj._source_client_name = (data.get("sourceClientName", obj.__undef__), dirty)
        if obj._source_client_name[0] is not None and obj._source_client_name[0] is not obj.__undef__:
            assert isinstance(obj._source_client_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source_client_name[0], type(obj._source_client_name[0])))
            common.validate_format(obj._source_client_name[0], "None", None, None)
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
        if "environment" == "type" or (self.environment is not self.__undef__ and (not (dirty and not self._environment[1]) or self.is_dirty_list(self.environment, self._environment) or belongs_to_parent)):
            dct["environment"] = dictify(self.environment)
        if "environment_user" == "type" or (self.environment_user is not self.__undef__ and (not (dirty and not self._environment_user[1]) or self.is_dirty_list(self.environment_user, self._environment_user) or belongs_to_parent)):
            dct["environmentUser"] = dictify(self.environment_user)
        if "master_server_name" == "type" or (self.master_server_name is not self.__undef__ and (not (dirty and not self._master_server_name[1]) or self.is_dirty_list(self.master_server_name, self._master_server_name) or belongs_to_parent)):
            dct["masterServerName"] = dictify(self.master_server_name)
        if "source_client_name" == "type" or (self.source_client_name is not self.__undef__ and (not (dirty and not self._source_client_name[1]) or self.is_dirty_list(self.source_client_name, self._source_client_name) or belongs_to_parent)):
            dct["sourceClientName"] = dictify(self.source_client_name)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._environment = (self._environment[0], True)
        self._environment_user = (self._environment_user[0], True)
        self._master_server_name = (self._master_server_name[0], True)
        self._source_client_name = (self._source_client_name[0], True)

    def is_dirty(self):
        return any([self._environment[1], self._environment_user[1], self._master_server_name[1], self._source_client_name[1]])

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
        if not isinstance(other, NetbackupConnectivityParameters):
            return False
        return super().__eq__(other) and \
               self.environment == other.environment and \
               self.environment_user == other.environment_user and \
               self.master_server_name == other.master_server_name and \
               self.source_client_name == other.source_client_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def environment(self):
        """
        Target environment to test NetBackup connectivity from.

        :rtype: ``str``
        """
        return self._environment[0]

    @environment.setter
    def environment(self, value):
        self._environment = (value, True)

    @property
    def environment_user(self):
        """
        The environment user to use to connect to the environment.

        :rtype: ``str``
        """
        return self._environment_user[0]

    @environment_user.setter
    def environment_user(self, value):
        self._environment_user = (value, True)

    @property
    def master_server_name(self):
        """
        The name of the NetBackup master server to attempt to connect to.

        :rtype: ``str``
        """
        return self._master_server_name[0]

    @master_server_name.setter
    def master_server_name(self, value):
        self._master_server_name = (value, True)

    @property
    def source_client_name(self):
        """
        The name of the NetBackup client to attempt to connect with.

        :rtype: ``str``
        """
        return self._source_client_name[0]

    @source_client_name.setter
    def source_client_name(self, value):
        self._source_client_name = (value, True)

