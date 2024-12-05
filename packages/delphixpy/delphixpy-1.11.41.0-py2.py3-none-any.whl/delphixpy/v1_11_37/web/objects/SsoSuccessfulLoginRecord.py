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

from delphixpy.v1_11_37.web.objects.LoginRecord import LoginRecord
from delphixpy.v1_11_37 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SsoSuccessfulLoginRecord(LoginRecord):
    """
    *(extends* :py:class:`v1_11_37.web.vo.LoginRecord` *)* Represents a
    successful SAML SSO login.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SsoSuccessfulLoginRecord", True)
        self._email = (self.__undef__, True)
        self._asserting_entity_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "email" not in data:
            raise ValueError("Missing required property \"email\".")
        obj._email = (data.get("email", obj.__undef__), dirty)
        if obj._email[0] is not None and obj._email[0] is not obj.__undef__:
            assert isinstance(obj._email[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._email[0], type(obj._email[0])))
            common.validate_format(obj._email[0], "None", None, None)
        if "assertingEntityId" not in data:
            raise ValueError("Missing required property \"assertingEntityId\".")
        obj._asserting_entity_id = (data.get("assertingEntityId", obj.__undef__), dirty)
        if obj._asserting_entity_id[0] is not None and obj._asserting_entity_id[0] is not obj.__undef__:
            assert isinstance(obj._asserting_entity_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._asserting_entity_id[0], type(obj._asserting_entity_id[0])))
            common.validate_format(obj._asserting_entity_id[0], "None", None, None)
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
        if "email" == "type" or (self.email is not self.__undef__ and (not (dirty and not self._email[1]) or self.is_dirty_list(self.email, self._email) or belongs_to_parent)):
            dct["email"] = dictify(self.email)
        if "asserting_entity_id" == "type" or (self.asserting_entity_id is not self.__undef__ and (not (dirty and not self._asserting_entity_id[1]) or self.is_dirty_list(self.asserting_entity_id, self._asserting_entity_id) or belongs_to_parent)):
            dct["assertingEntityId"] = dictify(self.asserting_entity_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._email = (self._email[0], True)
        self._asserting_entity_id = (self._asserting_entity_id[0], True)

    def is_dirty(self):
        return any([self._email[1], self._asserting_entity_id[1]])

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
        if not isinstance(other, SsoSuccessfulLoginRecord):
            return False
        return super().__eq__(other) and \
               self.email == other.email and \
               self.asserting_entity_id == other.asserting_entity_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def email(self):
        """
        Email address of the user who logged in.

        :rtype: ``str``
        """
        return self._email[0]

    @email.setter
    def email(self, value):
        self._email = (value, True)

    @property
    def asserting_entity_id(self):
        """
        Entity Id of the Identity provider which generated the SAML assertion.

        :rtype: ``str``
        """
        return self._asserting_entity_id[0]

    @asserting_entity_id.setter
    def asserting_entity_id(self, value):
        self._asserting_entity_id = (value, True)

