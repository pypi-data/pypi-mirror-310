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
#     /delphix-password-policy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PasswordPolicy(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_39.web.vo.NamedUserObject` *)* Password
    policies for Delphix users.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PasswordPolicy", True)
        self._name = (self.__undef__, True)
        self._min_length = (self.__undef__, True)
        self._reuse_disallow_limit = (self.__undef__, True)
        self._uppercase_letter = (self.__undef__, True)
        self._lowercase_letter = (self.__undef__, True)
        self._digit = (self.__undef__, True)
        self._symbol = (self.__undef__, True)
        self._disallow_username_as_password = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", 1, 64)
        obj._min_length = (data.get("minLength", obj.__undef__), dirty)
        if obj._min_length[0] is not None and obj._min_length[0] is not obj.__undef__:
            assert isinstance(obj._min_length[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._min_length[0], type(obj._min_length[0])))
            common.validate_format(obj._min_length[0], "None", None, None)
        obj._reuse_disallow_limit = (data.get("reuseDisallowLimit", obj.__undef__), dirty)
        if obj._reuse_disallow_limit[0] is not None and obj._reuse_disallow_limit[0] is not obj.__undef__:
            assert isinstance(obj._reuse_disallow_limit[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._reuse_disallow_limit[0], type(obj._reuse_disallow_limit[0])))
            common.validate_format(obj._reuse_disallow_limit[0], "None", None, None)
        obj._uppercase_letter = (data.get("uppercaseLetter", obj.__undef__), dirty)
        if obj._uppercase_letter[0] is not None and obj._uppercase_letter[0] is not obj.__undef__:
            assert isinstance(obj._uppercase_letter[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._uppercase_letter[0], type(obj._uppercase_letter[0])))
            common.validate_format(obj._uppercase_letter[0], "None", None, None)
        obj._lowercase_letter = (data.get("lowercaseLetter", obj.__undef__), dirty)
        if obj._lowercase_letter[0] is not None and obj._lowercase_letter[0] is not obj.__undef__:
            assert isinstance(obj._lowercase_letter[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._lowercase_letter[0], type(obj._lowercase_letter[0])))
            common.validate_format(obj._lowercase_letter[0], "None", None, None)
        obj._digit = (data.get("digit", obj.__undef__), dirty)
        if obj._digit[0] is not None and obj._digit[0] is not obj.__undef__:
            assert isinstance(obj._digit[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._digit[0], type(obj._digit[0])))
            common.validate_format(obj._digit[0], "None", None, None)
        obj._symbol = (data.get("symbol", obj.__undef__), dirty)
        if obj._symbol[0] is not None and obj._symbol[0] is not obj.__undef__:
            assert isinstance(obj._symbol[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._symbol[0], type(obj._symbol[0])))
            common.validate_format(obj._symbol[0], "None", None, None)
        obj._disallow_username_as_password = (data.get("disallowUsernameAsPassword", obj.__undef__), dirty)
        if obj._disallow_username_as_password[0] is not None and obj._disallow_username_as_password[0] is not obj.__undef__:
            assert isinstance(obj._disallow_username_as_password[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._disallow_username_as_password[0], type(obj._disallow_username_as_password[0])))
            common.validate_format(obj._disallow_username_as_password[0], "None", None, None)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "min_length" == "type" or (self.min_length is not self.__undef__ and (not (dirty and not self._min_length[1]) or self.is_dirty_list(self.min_length, self._min_length) or belongs_to_parent)):
            dct["minLength"] = dictify(self.min_length)
        if "reuse_disallow_limit" == "type" or (self.reuse_disallow_limit is not self.__undef__ and (not (dirty and not self._reuse_disallow_limit[1]) or self.is_dirty_list(self.reuse_disallow_limit, self._reuse_disallow_limit) or belongs_to_parent)):
            dct["reuseDisallowLimit"] = dictify(self.reuse_disallow_limit)
        if "uppercase_letter" == "type" or (self.uppercase_letter is not self.__undef__ and (not (dirty and not self._uppercase_letter[1]) or self.is_dirty_list(self.uppercase_letter, self._uppercase_letter) or belongs_to_parent)):
            dct["uppercaseLetter"] = dictify(self.uppercase_letter)
        if "lowercase_letter" == "type" or (self.lowercase_letter is not self.__undef__ and (not (dirty and not self._lowercase_letter[1]) or self.is_dirty_list(self.lowercase_letter, self._lowercase_letter) or belongs_to_parent)):
            dct["lowercaseLetter"] = dictify(self.lowercase_letter)
        if "digit" == "type" or (self.digit is not self.__undef__ and (not (dirty and not self._digit[1]) or self.is_dirty_list(self.digit, self._digit) or belongs_to_parent)):
            dct["digit"] = dictify(self.digit)
        if "symbol" == "type" or (self.symbol is not self.__undef__ and (not (dirty and not self._symbol[1]) or self.is_dirty_list(self.symbol, self._symbol) or belongs_to_parent)):
            dct["symbol"] = dictify(self.symbol)
        if "disallow_username_as_password" == "type" or (self.disallow_username_as_password is not self.__undef__ and (not (dirty and not self._disallow_username_as_password[1]) or self.is_dirty_list(self.disallow_username_as_password, self._disallow_username_as_password) or belongs_to_parent)):
            dct["disallowUsernameAsPassword"] = dictify(self.disallow_username_as_password)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._min_length = (self._min_length[0], True)
        self._reuse_disallow_limit = (self._reuse_disallow_limit[0], True)
        self._uppercase_letter = (self._uppercase_letter[0], True)
        self._lowercase_letter = (self._lowercase_letter[0], True)
        self._digit = (self._digit[0], True)
        self._symbol = (self._symbol[0], True)
        self._disallow_username_as_password = (self._disallow_username_as_password[0], True)

    def is_dirty(self):
        return any([self._name[1], self._min_length[1], self._reuse_disallow_limit[1], self._uppercase_letter[1], self._lowercase_letter[1], self._digit[1], self._symbol[1], self._disallow_username_as_password[1]])

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
        if not isinstance(other, PasswordPolicy):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.min_length == other.min_length and \
               self.reuse_disallow_limit == other.reuse_disallow_limit and \
               self.uppercase_letter == other.uppercase_letter and \
               self.lowercase_letter == other.lowercase_letter and \
               self.digit == other.digit and \
               self.symbol == other.symbol and \
               self.disallow_username_as_password == other.disallow_username_as_password

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        Name of password policy.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def min_length(self):
        """
        Minimum length for the password.

        :rtype: ``int``
        """
        return self._min_length[0]

    @min_length.setter
    def min_length(self, value):
        self._min_length = (value, True)

    @property
    def reuse_disallow_limit(self):
        """
        The password may not be the same as any of previous n passwords.

        :rtype: ``int``
        """
        return self._reuse_disallow_limit[0]

    @reuse_disallow_limit.setter
    def reuse_disallow_limit(self, value):
        self._reuse_disallow_limit = (value, True)

    @property
    def uppercase_letter(self):
        """
        True if password must contain at least one uppercase letter.

        :rtype: ``bool``
        """
        return self._uppercase_letter[0]

    @uppercase_letter.setter
    def uppercase_letter(self, value):
        self._uppercase_letter = (value, True)

    @property
    def lowercase_letter(self):
        """
        True if password must contain at least one lowercase letter.

        :rtype: ``bool``
        """
        return self._lowercase_letter[0]

    @lowercase_letter.setter
    def lowercase_letter(self, value):
        self._lowercase_letter = (value, True)

    @property
    def digit(self):
        """
        True if password must contain at least one digit.

        :rtype: ``bool``
        """
        return self._digit[0]

    @digit.setter
    def digit(self, value):
        self._digit = (value, True)

    @property
    def symbol(self):
        """
        True if password must contain at least one symbol.

        :rtype: ``bool``
        """
        return self._symbol[0]

    @symbol.setter
    def symbol(self, value):
        self._symbol = (value, True)

    @property
    def disallow_username_as_password(self):
        """
        True to disallow password containing username.

        :rtype: ``bool``
        """
        return self._disallow_username_as_password[0]

    @disallow_username_as_password.setter
    def disallow_username_as_password(self, value):
        self._disallow_username_as_password = (value, True)

