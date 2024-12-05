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
#     /delphix-oracle-base-db-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_28.web.objects.SourceConfig import SourceConfig
from delphixpy.v1_11_28 import factory
from delphixpy.v1_11_28 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleBaseDBConfig(SourceConfig):
    """
    *(extends* :py:class:`v1_11_28.web.vo.SourceConfig` *)* The source config
    represents the dynamically discovered attributes of a base Oracle source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleBaseDBConfig", True)
        self._user = (self.__undef__, True)
        self._credentials = (self.__undef__, True)
        self._services = (self.__undef__, True)
        self._non_sys_user = (self.__undef__, True)
        self._non_sys_credentials = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._user = (data.get("user", obj.__undef__), dirty)
        if obj._user[0] is not None and obj._user[0] is not obj.__undef__:
            assert isinstance(obj._user[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._user[0], type(obj._user[0])))
            common.validate_format(obj._user[0], "None", None, 30)
        if "credentials" in data and data["credentials"] is not None:
            obj._credentials = (factory.create_object(data["credentials"], "Credential"), dirty)
            factory.validate_type(obj._credentials[0], "Credential")
        else:
            obj._credentials = (obj.__undef__, dirty)
        obj._services = []
        for item in data.get("services") or []:
            obj._services.append(factory.create_object(item))
            factory.validate_type(obj._services[-1], "OracleService")
        obj._services = (obj._services, dirty)
        obj._non_sys_user = (data.get("nonSysUser", obj.__undef__), dirty)
        if obj._non_sys_user[0] is not None and obj._non_sys_user[0] is not obj.__undef__:
            assert isinstance(obj._non_sys_user[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._non_sys_user[0], type(obj._non_sys_user[0])))
            common.validate_format(obj._non_sys_user[0], "None", None, 30)
        if "nonSysCredentials" in data and data["nonSysCredentials"] is not None:
            obj._non_sys_credentials = (factory.create_object(data["nonSysCredentials"], "Credential"), dirty)
            factory.validate_type(obj._non_sys_credentials[0], "Credential")
        else:
            obj._non_sys_credentials = (obj.__undef__, dirty)
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
        if "user" == "type" or (self.user is not self.__undef__ and (not (dirty and not self._user[1]) or self.is_dirty_list(self.user, self._user) or belongs_to_parent)):
            dct["user"] = dictify(self.user)
        if "credentials" == "type" or (self.credentials is not self.__undef__ and (not (dirty and not self._credentials[1]) or self.is_dirty_list(self.credentials, self._credentials) or belongs_to_parent)):
            dct["credentials"] = dictify(self.credentials)
        if "services" == "type" or (self.services is not self.__undef__ and (not (dirty and not self._services[1]) or self.is_dirty_list(self.services, self._services) or belongs_to_parent)):
            dct["services"] = dictify(self.services, prop_is_list_or_vo=True)
        if "non_sys_user" == "type" or (self.non_sys_user is not self.__undef__ and (not (dirty and not self._non_sys_user[1]) or self.is_dirty_list(self.non_sys_user, self._non_sys_user) or belongs_to_parent)):
            dct["nonSysUser"] = dictify(self.non_sys_user)
        if "non_sys_credentials" == "type" or (self.non_sys_credentials is not self.__undef__ and (not (dirty and not self._non_sys_credentials[1]) or self.is_dirty_list(self.non_sys_credentials, self._non_sys_credentials) or belongs_to_parent)):
            dct["nonSysCredentials"] = dictify(self.non_sys_credentials)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._user = (self._user[0], True)
        self._credentials = (self._credentials[0], True)
        self._services = (self._services[0], True)
        self._non_sys_user = (self._non_sys_user[0], True)
        self._non_sys_credentials = (self._non_sys_credentials[0], True)

    def is_dirty(self):
        return any([self._user[1], self._credentials[1], self._services[1], self._non_sys_user[1], self._non_sys_credentials[1]])

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
        if not isinstance(other, OracleBaseDBConfig):
            return False
        return super().__eq__(other) and \
               self.user == other.user and \
               self.credentials == other.credentials and \
               self.services == other.services and \
               self.non_sys_user == other.non_sys_user and \
               self.non_sys_credentials == other.non_sys_credentials

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def user(self):
        """
        The username of the database user.

        :rtype: ``str`` *or* ``null``
        """
        return self._user[0]

    @user.setter
    def user(self, value):
        self._user = (value, True)

    @property
    def credentials(self):
        """
        The password of the database user. This must be a Credential instance.

        :rtype: :py:class:`v1_11_28.web.vo.Credential`
        """
        return self._credentials[0]

    @credentials.setter
    def credentials(self, value):
        self._credentials = (value, True)

    @property
    def services(self):
        """
        The list of database services.

        :rtype: ``list`` of :py:class:`v1_11_28.web.vo.OracleService`
        """
        return self._services[0]

    @services.setter
    def services(self, value):
        self._services = (value, True)

    @property
    def non_sys_user(self):
        """
        The username of a database user that does not have administrative
        privileges.

        :rtype: ``str`` *or* ``null``
        """
        return self._non_sys_user[0]

    @non_sys_user.setter
    def non_sys_user(self, value):
        self._non_sys_user = (value, True)

    @property
    def non_sys_credentials(self):
        """
        The credentials of a database user that does not have administrative
        privileges.

        :rtype: :py:class:`v1_11_28.web.vo.Credential`
        """
        return self._non_sys_credentials[0]

    @non_sys_credentials.setter
    def non_sys_credentials(self, value):
        self._non_sys_credentials = (value, True)

