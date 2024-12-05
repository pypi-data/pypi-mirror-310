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
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UserManagement(TypedObject):
    """
    *(extends* :py:class:`v1_11_18.web.vo.TypedObject` *)* Configuration of
    user management capabilities.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UserManagement", True)
        self._user_and_roles_lock_down = (self.__undef__, True)
        self._api_user_lock_down = (self.__undef__, True)
        self._locked_authorization_targets = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "userAndRolesLockDown" not in data:
            raise ValueError("Missing required property \"userAndRolesLockDown\".")
        obj._user_and_roles_lock_down = (data.get("userAndRolesLockDown", obj.__undef__), dirty)
        if obj._user_and_roles_lock_down[0] is not None and obj._user_and_roles_lock_down[0] is not obj.__undef__:
            assert isinstance(obj._user_and_roles_lock_down[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._user_and_roles_lock_down[0], type(obj._user_and_roles_lock_down[0])))
            common.validate_format(obj._user_and_roles_lock_down[0], "None", None, None)
        if "apiUserLockDown" not in data:
            raise ValueError("Missing required property \"apiUserLockDown\".")
        obj._api_user_lock_down = (data.get("apiUserLockDown", obj.__undef__), dirty)
        if obj._api_user_lock_down[0] is not None and obj._api_user_lock_down[0] is not obj.__undef__:
            assert isinstance(obj._api_user_lock_down[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._api_user_lock_down[0], type(obj._api_user_lock_down[0])))
            common.validate_format(obj._api_user_lock_down[0], "None", None, None)
        obj._locked_authorization_targets = []
        for item in data.get("lockedAuthorizationTargets") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "type", None, None)
            obj._locked_authorization_targets.append(item)
        obj._locked_authorization_targets = (obj._locked_authorization_targets, dirty)
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
        if "user_and_roles_lock_down" == "type" or (self.user_and_roles_lock_down is not self.__undef__ and (not (dirty and not self._user_and_roles_lock_down[1]) or self.is_dirty_list(self.user_and_roles_lock_down, self._user_and_roles_lock_down) or belongs_to_parent)):
            dct["userAndRolesLockDown"] = dictify(self.user_and_roles_lock_down)
        if "api_user_lock_down" == "type" or (self.api_user_lock_down is not self.__undef__ and (not (dirty and not self._api_user_lock_down[1]) or self.is_dirty_list(self.api_user_lock_down, self._api_user_lock_down) or belongs_to_parent)):
            dct["apiUserLockDown"] = dictify(self.api_user_lock_down)
        if "locked_authorization_targets" == "type" or (self.locked_authorization_targets is not self.__undef__ and (not (dirty and not self._locked_authorization_targets[1]))):
            dct["lockedAuthorizationTargets"] = dictify(self.locked_authorization_targets)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._user_and_roles_lock_down = (self._user_and_roles_lock_down[0], True)
        self._api_user_lock_down = (self._api_user_lock_down[0], True)
        self._locked_authorization_targets = (self._locked_authorization_targets[0], True)

    def is_dirty(self):
        return any([self._user_and_roles_lock_down[1], self._api_user_lock_down[1], self._locked_authorization_targets[1]])

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
        if not isinstance(other, UserManagement):
            return False
        return super().__eq__(other) and \
               self.user_and_roles_lock_down == other.user_and_roles_lock_down and \
               self.api_user_lock_down == other.api_user_lock_down and \
               self.locked_authorization_targets == other.locked_authorization_targets

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def user_and_roles_lock_down(self):
        """
        Whether the creation and delete of users is restricted to the Central
        Management agent.

        :rtype: ``bool``
        """
        return self._user_and_roles_lock_down[0]

    @user_and_roles_lock_down.setter
    def user_and_roles_lock_down(self, value):
        self._user_and_roles_lock_down = (value, True)

    @property
    def api_user_lock_down(self):
        """
        Whether updating users to API user is restricted to the Central
        Management agent.

        :rtype: ``bool``
        """
        return self._api_user_lock_down[0]

    @api_user_lock_down.setter
    def api_user_lock_down(self, value):
        self._api_user_lock_down = (value, True)

    @property
    def locked_authorization_targets(self):
        """
        The list of object types for which authorizations management is
        restricted to the Central management agent.

        :rtype: ``list`` of ``str``
        """
        return self._locked_authorization_targets[0]

    @locked_authorization_targets.setter
    def locked_authorization_targets(self, value):
        self._locked_authorization_targets = (value, True)

