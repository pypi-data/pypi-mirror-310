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
#     /delphix-password-reset-validation-result.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.TypedObject import TypedObject
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PasswordResetValidationResult(TypedObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.TypedObject` *)* Self-service
    password Reset validation result.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PasswordResetValidationResult", True)
        self._valid_token = (self.__undef__, True)
        self._valid_password = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "validToken" not in data:
            raise ValueError("Missing required property \"validToken\".")
        obj._valid_token = (data.get("validToken", obj.__undef__), dirty)
        if obj._valid_token[0] is not None and obj._valid_token[0] is not obj.__undef__:
            assert isinstance(obj._valid_token[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._valid_token[0], type(obj._valid_token[0])))
            common.validate_format(obj._valid_token[0], "None", None, None)
        obj._valid_password = (data.get("validPassword", obj.__undef__), dirty)
        if obj._valid_password[0] is not None and obj._valid_password[0] is not obj.__undef__:
            assert isinstance(obj._valid_password[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._valid_password[0], type(obj._valid_password[0])))
            common.validate_format(obj._valid_password[0], "None", None, None)
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
        if "valid_token" == "type" or (self.valid_token is not self.__undef__ and (not (dirty and not self._valid_token[1]) or self.is_dirty_list(self.valid_token, self._valid_token) or belongs_to_parent)):
            dct["validToken"] = dictify(self.valid_token)
        if "valid_password" == "type" or (self.valid_password is not self.__undef__ and (not (dirty and not self._valid_password[1]) or self.is_dirty_list(self.valid_password, self._valid_password) or belongs_to_parent)):
            dct["validPassword"] = dictify(self.valid_password)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._valid_token = (self._valid_token[0], True)
        self._valid_password = (self._valid_password[0], True)

    def is_dirty(self):
        return any([self._valid_token[1], self._valid_password[1]])

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
        if not isinstance(other, PasswordResetValidationResult):
            return False
        return super().__eq__(other) and \
               self.valid_token == other.valid_token and \
               self.valid_password == other.valid_password

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def valid_token(self):
        """
        The identifier string for password reset validation.

        :rtype: ``bool``
        """
        return self._valid_token[0]

    @valid_token.setter
    def valid_token(self, value):
        self._valid_token = (value, True)

    @property
    def valid_password(self):
        """
        New password provided for self-service reset.

        :rtype: ``bool``
        """
        return self._valid_password[0]

    @valid_password.setter
    def valid_password(self, value):
        self._valid_password = (value, True)

