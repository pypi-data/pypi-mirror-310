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
#     /delphix-hashicorp-approle-authentication.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.HashiCorpAuthentication import HashiCorpAuthentication
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HashiCorpAppRoleAuthentication(HashiCorpAuthentication):
    """
    *(extends* :py:class:`v1_11_32.web.vo.HashiCorpAuthentication` *)* AppRole
    credentials for authenticating to a HashiCorp vault.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HashiCorpAppRoleAuthentication", True)
        self._role_id = (self.__undef__, True)
        self._secret_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._role_id = (data.get("roleId", obj.__undef__), dirty)
        if obj._role_id[0] is not None and obj._role_id[0] is not obj.__undef__:
            assert isinstance(obj._role_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._role_id[0], type(obj._role_id[0])))
            common.validate_format(obj._role_id[0], "None", None, None)
        obj._secret_id = (data.get("secretId", obj.__undef__), dirty)
        if obj._secret_id[0] is not None and obj._secret_id[0] is not obj.__undef__:
            assert isinstance(obj._secret_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._secret_id[0], type(obj._secret_id[0])))
            common.validate_format(obj._secret_id[0], "password", None, None)
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
        if "role_id" == "type" or (self.role_id is not self.__undef__ and (not (dirty and not self._role_id[1]) or self.is_dirty_list(self.role_id, self._role_id) or belongs_to_parent)):
            dct["roleId"] = dictify(self.role_id)
        if "secret_id" == "type" or (self.secret_id is not self.__undef__ and (not (dirty and not self._secret_id[1]) or self.is_dirty_list(self.secret_id, self._secret_id) or belongs_to_parent)):
            dct["secretId"] = dictify(self.secret_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._role_id = (self._role_id[0], True)
        self._secret_id = (self._secret_id[0], True)

    def is_dirty(self):
        return any([self._role_id[1], self._secret_id[1]])

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
        if not isinstance(other, HashiCorpAppRoleAuthentication):
            return False
        return super().__eq__(other) and \
               self.role_id == other.role_id and \
               self.secret_id == other.secret_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def role_id(self):
        """
        Role id for authenticating to the vault.

        :rtype: ``str``
        """
        return self._role_id[0]

    @role_id.setter
    def role_id(self, value):
        self._role_id = (value, True)

    @property
    def secret_id(self):
        """
        Secret id for authenticating to the vault.

        :rtype: ``str``
        """
        return self._secret_id[0]

    @secret_id.setter
    def secret_id(self, value):
        self._secret_id = (value, True)

