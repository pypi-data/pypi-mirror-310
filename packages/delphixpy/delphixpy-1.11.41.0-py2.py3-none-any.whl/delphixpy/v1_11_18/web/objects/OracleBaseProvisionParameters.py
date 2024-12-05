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
#     /delphix-oracle-base-provision-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.ProvisionParameters import ProvisionParameters
from delphixpy.v1_11_18 import factory
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleBaseProvisionParameters(ProvisionParameters):
    """
    *(extends* :py:class:`v1_11_18.web.vo.ProvisionParameters` *)* Parameters
    applicable when provisioning all Oracle databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleBaseProvisionParameters", True)
        self._container = (self.__undef__, True)
        self._source = (self.__undef__, True)
        self._source_config = (self.__undef__, True)
        self._username = (self.__undef__, True)
        self._credential = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "container" not in data:
            raise ValueError("Missing required property \"container\".")
        if "container" in data and data["container"] is not None:
            obj._container = (factory.create_object(data["container"], "OracleDatabaseContainer"), dirty)
            factory.validate_type(obj._container[0], "OracleDatabaseContainer")
        else:
            obj._container = (obj.__undef__, dirty)
        if "source" not in data:
            raise ValueError("Missing required property \"source\".")
        if "source" in data and data["source"] is not None:
            obj._source = (factory.create_object(data["source"], "OracleVirtualSource"), dirty)
            factory.validate_type(obj._source[0], "OracleVirtualSource")
        else:
            obj._source = (obj.__undef__, dirty)
        if "sourceConfig" not in data:
            raise ValueError("Missing required property \"sourceConfig\".")
        if "sourceConfig" in data and data["sourceConfig"] is not None:
            obj._source_config = (factory.create_object(data["sourceConfig"], "OracleBaseDBConfig"), dirty)
            factory.validate_type(obj._source_config[0], "OracleBaseDBConfig")
        else:
            obj._source_config = (obj.__undef__, dirty)
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        if "credential" in data and data["credential"] is not None:
            obj._credential = (factory.create_object(data["credential"], "Credential"), dirty)
            factory.validate_type(obj._credential[0], "Credential")
        else:
            obj._credential = (obj.__undef__, dirty)
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
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]) or self.is_dirty_list(self.container, self._container) or belongs_to_parent)):
            dct["container"] = dictify(self.container, prop_is_list_or_vo=True)
        if "source" == "type" or (self.source is not self.__undef__ and (not (dirty and not self._source[1]) or self.is_dirty_list(self.source, self._source) or belongs_to_parent)):
            dct["source"] = dictify(self.source, prop_is_list_or_vo=True)
        if "source_config" == "type" or (self.source_config is not self.__undef__ and (not (dirty and not self._source_config[1]) or self.is_dirty_list(self.source_config, self._source_config) or belongs_to_parent)):
            dct["sourceConfig"] = dictify(self.source_config, prop_is_list_or_vo=True)
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]) or self.is_dirty_list(self.username, self._username) or belongs_to_parent)):
            dct["username"] = dictify(self.username)
        if "credential" == "type" or (self.credential is not self.__undef__ and (not (dirty and not self._credential[1]) or self.is_dirty_list(self.credential, self._credential) or belongs_to_parent)):
            dct["credential"] = dictify(self.credential, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._container = (self._container[0], True)
        self._source = (self._source[0], True)
        self._source_config = (self._source_config[0], True)
        self._username = (self._username[0], True)
        self._credential = (self._credential[0], True)

    def is_dirty(self):
        return any([self._container[1], self._source[1], self._source_config[1], self._username[1], self._credential[1]])

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
        if not isinstance(other, OracleBaseProvisionParameters):
            return False
        return super().__eq__(other) and \
               self.container == other.container and \
               self.source == other.source and \
               self.source_config == other.source_config and \
               self.username == other.username and \
               self.credential == other.credential

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def container(self):
        """
        The new container for the provisioned database.

        :rtype: :py:class:`v1_11_18.web.vo.OracleDatabaseContainer`
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def source(self):
        """
        The source that describes an external database instance.

        :rtype: :py:class:`v1_11_18.web.vo.OracleVirtualSource`
        """
        return self._source[0]

    @source.setter
    def source(self, value):
        self._source = (value, True)

    @property
    def source_config(self):
        """
        The source config including dynamically discovered attributes of the
        source.

        :rtype: :py:class:`v1_11_18.web.vo.OracleBaseDBConfig`
        """
        return self._source_config[0]

    @source_config.setter
    def source_config(self, value):
        self._source_config = (value, True)

    @property
    def username(self):
        """
        The name of the privileged user to run the provision operation as.

        :rtype: ``str``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def credential(self):
        """
        The security credential of the privileged user to run the provision
        operation as.

        :rtype: :py:class:`v1_11_18.web.vo.Credential`
        """
        return self._credential[0]

    @credential.setter
    def credential(self, value):
        self._credential = (value, True)

