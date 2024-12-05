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
#     /delphix-source-environment-user.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_19.web.objects.UserObject import UserObject
from delphixpy.v1_11_19 import factory
from delphixpy.v1_11_19 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class EnvironmentUser(UserObject):
    """
    *(extends* :py:class:`v1_11_19.web.vo.UserObject` *)* The representation of
    an environment user object.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("EnvironmentUser", True)
        self._credential = (self.__undef__, True)
        self._environment = (self.__undef__, True)
        self._group_id = (self.__undef__, True)
        self._user_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "credential" in data and data["credential"] is not None:
            obj._credential = (factory.create_object(data["credential"], "Credential"), dirty)
            factory.validate_type(obj._credential[0], "Credential")
        else:
            obj._credential = (obj.__undef__, dirty)
        obj._environment = (data.get("environment", obj.__undef__), dirty)
        if obj._environment[0] is not None and obj._environment[0] is not obj.__undef__:
            assert isinstance(obj._environment[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._environment[0], type(obj._environment[0])))
            common.validate_format(obj._environment[0], "objectReference", None, None)
        obj._group_id = (data.get("groupId", obj.__undef__), dirty)
        if obj._group_id[0] is not None and obj._group_id[0] is not obj.__undef__:
            assert isinstance(obj._group_id[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._group_id[0], type(obj._group_id[0])))
            common.validate_format(obj._group_id[0], "None", None, None)
        obj._user_id = (data.get("userId", obj.__undef__), dirty)
        if obj._user_id[0] is not None and obj._user_id[0] is not obj.__undef__:
            assert isinstance(obj._user_id[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._user_id[0], type(obj._user_id[0])))
            common.validate_format(obj._user_id[0], "None", None, None)
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
        if "credential" == "type" or (self.credential is not self.__undef__ and (not (dirty and not self._credential[1]) or self.is_dirty_list(self.credential, self._credential) or belongs_to_parent)):
            dct["credential"] = dictify(self.credential, prop_is_list_or_vo=True)
        if "environment" == "type" or (self.environment is not self.__undef__ and (not (dirty and not self._environment[1]) or self.is_dirty_list(self.environment, self._environment) or belongs_to_parent)):
            dct["environment"] = dictify(self.environment)
        if "group_id" == "type" or (self.group_id is not self.__undef__ and (not (dirty and not self._group_id[1]) or self.is_dirty_list(self.group_id, self._group_id) or belongs_to_parent)):
            dct["groupId"] = dictify(self.group_id)
        if "user_id" == "type" or (self.user_id is not self.__undef__ and (not (dirty and not self._user_id[1]) or self.is_dirty_list(self.user_id, self._user_id) or belongs_to_parent)):
            dct["userId"] = dictify(self.user_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._credential = (self._credential[0], True)
        self._environment = (self._environment[0], True)
        self._group_id = (self._group_id[0], True)
        self._user_id = (self._user_id[0], True)

    def is_dirty(self):
        return any([self._credential[1], self._environment[1], self._group_id[1], self._user_id[1]])

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
        if not isinstance(other, EnvironmentUser):
            return False
        return super().__eq__(other) and \
               self.credential == other.credential and \
               self.environment == other.environment and \
               self.group_id == other.group_id and \
               self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def credential(self):
        """
        The credential for the environment user.

        :rtype: :py:class:`v1_11_19.web.vo.Credential`
        """
        return self._credential[0]

    @credential.setter
    def credential(self, value):
        self._credential = (value, True)

    @property
    def environment(self):
        """
        A reference to the associated environment.

        :rtype: ``str``
        """
        return self._environment[0]

    @environment.setter
    def environment(self, value):
        self._environment = (value, True)

    @property
    def group_id(self):
        """
        Group ID of the user.

        :rtype: ``int``
        """
        return self._group_id[0]

    @group_id.setter
    def group_id(self, value):
        self._group_id = (value, True)

    @property
    def user_id(self):
        """
        User ID of the user.

        :rtype: ``int``
        """
        return self._user_id[0]

    @user_id.setter
    def user_id(self, value):
        self._user_id = (value, True)

