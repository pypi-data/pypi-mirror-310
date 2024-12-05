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
#     /delphix-password-reset-validation-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_24.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_24 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PasswordResetValidationParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_24.web.vo.TypedObject` *)* Self-service
    password Reset validation parameters.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PasswordResetValidationParameters", True)
        self._token_uuid = (self.__undef__, True)
        self._new_password = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "tokenUUID" not in data:
            raise ValueError("Missing required property \"tokenUUID\".")
        obj._token_uuid = (data.get("tokenUUID", obj.__undef__), dirty)
        if obj._token_uuid[0] is not None and obj._token_uuid[0] is not obj.__undef__:
            assert isinstance(obj._token_uuid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._token_uuid[0], type(obj._token_uuid[0])))
            common.validate_format(obj._token_uuid[0], "None", None, None)
        obj._new_password = (data.get("newPassword", obj.__undef__), dirty)
        if obj._new_password[0] is not None and obj._new_password[0] is not obj.__undef__:
            assert isinstance(obj._new_password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._new_password[0], type(obj._new_password[0])))
            common.validate_format(obj._new_password[0], "password", None, None)
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
        if "token_uuid" == "type" or (self.token_uuid is not self.__undef__ and (not (dirty and not self._token_uuid[1]) or self.is_dirty_list(self.token_uuid, self._token_uuid) or belongs_to_parent)):
            dct["tokenUUID"] = dictify(self.token_uuid)
        if "new_password" == "type" or (self.new_password is not self.__undef__ and (not (dirty and not self._new_password[1]) or self.is_dirty_list(self.new_password, self._new_password) or belongs_to_parent)):
            dct["newPassword"] = dictify(self.new_password)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._token_uuid = (self._token_uuid[0], True)
        self._new_password = (self._new_password[0], True)

    def is_dirty(self):
        return any([self._token_uuid[1], self._new_password[1]])

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
        if not isinstance(other, PasswordResetValidationParameters):
            return False
        return super().__eq__(other) and \
               self.token_uuid == other.token_uuid and \
               self.new_password == other.new_password

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def token_uuid(self):
        """
        A user's token UUID (unique identifier).

        :rtype: ``str``
        """
        return self._token_uuid[0]

    @token_uuid.setter
    def token_uuid(self, value):
        self._token_uuid = (value, True)

    @property
    def new_password(self):
        """
        New password provided for self-service reset.

        :rtype: ``str``
        """
        return self._new_password[0]

    @new_password.setter
    def new_password(self, value):
        self._new_password = (value, True)

