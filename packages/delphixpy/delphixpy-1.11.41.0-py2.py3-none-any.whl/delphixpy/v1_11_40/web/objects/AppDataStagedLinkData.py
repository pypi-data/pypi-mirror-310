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
#     /delphix-appdata-staged-link-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.AppDataLinkData import AppDataLinkData
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AppDataStagedLinkData(AppDataLinkData):
    """
    *(extends* :py:class:`v1_11_40.web.vo.AppDataLinkData` *)* Represents the
    AppData specific parameters of a link request for a source with a staging
    source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AppDataStagedLinkData", True)
        self._config = (self.__undef__, True)
        self._staging_mount_base = (self.__undef__, True)
        self._staging_environment = (self.__undef__, True)
        self._staging_environment_user = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "config" not in data:
            raise ValueError("Missing required property \"config\".")
        obj._config = (data.get("config", obj.__undef__), dirty)
        if obj._config[0] is not None and obj._config[0] is not obj.__undef__:
            assert isinstance(obj._config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config[0], type(obj._config[0])))
            common.validate_format(obj._config[0], "objectReference", None, None)
        obj._staging_mount_base = (data.get("stagingMountBase", obj.__undef__), dirty)
        if obj._staging_mount_base[0] is not None and obj._staging_mount_base[0] is not obj.__undef__:
            assert isinstance(obj._staging_mount_base[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_mount_base[0], type(obj._staging_mount_base[0])))
            common.validate_format(obj._staging_mount_base[0], "None", None, 256)
        if "stagingEnvironment" not in data:
            raise ValueError("Missing required property \"stagingEnvironment\".")
        obj._staging_environment = (data.get("stagingEnvironment", obj.__undef__), dirty)
        if obj._staging_environment[0] is not None and obj._staging_environment[0] is not obj.__undef__:
            assert isinstance(obj._staging_environment[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_environment[0], type(obj._staging_environment[0])))
            common.validate_format(obj._staging_environment[0], "objectReference", None, None)
        if "stagingEnvironmentUser" not in data:
            raise ValueError("Missing required property \"stagingEnvironmentUser\".")
        obj._staging_environment_user = (data.get("stagingEnvironmentUser", obj.__undef__), dirty)
        if obj._staging_environment_user[0] is not None and obj._staging_environment_user[0] is not obj.__undef__:
            assert isinstance(obj._staging_environment_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_environment_user[0], type(obj._staging_environment_user[0])))
            common.validate_format(obj._staging_environment_user[0], "objectReference", None, None)
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
        if "config" == "type" or (self.config is not self.__undef__ and (not (dirty and not self._config[1]) or self.is_dirty_list(self.config, self._config) or belongs_to_parent)):
            dct["config"] = dictify(self.config)
        if "staging_mount_base" == "type" or (self.staging_mount_base is not self.__undef__ and (not (dirty and not self._staging_mount_base[1]) or self.is_dirty_list(self.staging_mount_base, self._staging_mount_base) or belongs_to_parent)):
            dct["stagingMountBase"] = dictify(self.staging_mount_base)
        if "staging_environment" == "type" or (self.staging_environment is not self.__undef__ and (not (dirty and not self._staging_environment[1]) or self.is_dirty_list(self.staging_environment, self._staging_environment) or belongs_to_parent)):
            dct["stagingEnvironment"] = dictify(self.staging_environment)
        if "staging_environment_user" == "type" or (self.staging_environment_user is not self.__undef__ and (not (dirty and not self._staging_environment_user[1]) or self.is_dirty_list(self.staging_environment_user, self._staging_environment_user) or belongs_to_parent)):
            dct["stagingEnvironmentUser"] = dictify(self.staging_environment_user)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._config = (self._config[0], True)
        self._staging_mount_base = (self._staging_mount_base[0], True)
        self._staging_environment = (self._staging_environment[0], True)
        self._staging_environment_user = (self._staging_environment_user[0], True)

    def is_dirty(self):
        return any([self._config[1], self._staging_mount_base[1], self._staging_environment[1], self._staging_environment_user[1]])

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
        if not isinstance(other, AppDataStagedLinkData):
            return False
        return super().__eq__(other) and \
               self.config == other.config and \
               self.staging_mount_base == other.staging_mount_base and \
               self.staging_environment == other.staging_environment and \
               self.staging_environment_user == other.staging_environment_user

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def config(self):
        """
        Reference to the configuration for the source.

        :rtype: ``str``
        """
        return self._config[0]

    @config.setter
    def config(self, value):
        self._config = (value, True)

    @property
    def staging_mount_base(self):
        """
        The base mount point for the NFS mount on the staging environment.

        :rtype: ``str``
        """
        return self._staging_mount_base[0]

    @staging_mount_base.setter
    def staging_mount_base(self, value):
        self._staging_mount_base = (value, True)

    @property
    def staging_environment(self):
        """
        The environment used as an intermediate stage to pull data into
        Delphix.

        :rtype: ``str``
        """
        return self._staging_environment[0]

    @staging_environment.setter
    def staging_environment(self, value):
        self._staging_environment = (value, True)

    @property
    def staging_environment_user(self):
        """
        The environment user used to access the staging environment.

        :rtype: ``str``
        """
        return self._staging_environment_user[0]

    @staging_environment_user.setter
    def staging_environment_user(self, value):
        self._staging_environment_user = (value, True)

