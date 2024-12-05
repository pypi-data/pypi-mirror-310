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
#     /delphix-cyberark-vault-credential.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.AbstractVaultCredential import AbstractVaultCredential
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CyberArkVaultCredential(AbstractVaultCredential):
    """
    *(extends* :py:class:`v1_11_16.web.vo.AbstractVaultCredential` *)* The
    CyberArk vault based security credential.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CyberArkVaultCredential", True)
        self._vault = (self.__undef__, True)
        self._query_string = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._vault = (data.get("vault", obj.__undef__), dirty)
        if obj._vault[0] is not None and obj._vault[0] is not obj.__undef__:
            assert isinstance(obj._vault[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._vault[0], type(obj._vault[0])))
            common.validate_format(obj._vault[0], "objectReference", None, None)
        obj._query_string = (data.get("queryString", obj.__undef__), dirty)
        if obj._query_string[0] is not None and obj._query_string[0] is not obj.__undef__:
            assert isinstance(obj._query_string[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._query_string[0], type(obj._query_string[0])))
            common.validate_format(obj._query_string[0], "None", None, None)
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
        if "vault" == "type" or (self.vault is not self.__undef__ and (not (dirty and not self._vault[1]) or self.is_dirty_list(self.vault, self._vault) or belongs_to_parent)):
            dct["vault"] = dictify(self.vault)
        if "query_string" == "type" or (self.query_string is not self.__undef__ and (not (dirty and not self._query_string[1]) or self.is_dirty_list(self.query_string, self._query_string) or belongs_to_parent)):
            dct["queryString"] = dictify(self.query_string)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._vault = (self._vault[0], True)
        self._query_string = (self._query_string[0], True)

    def is_dirty(self):
        return any([self._vault[1], self._query_string[1]])

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
        if not isinstance(other, CyberArkVaultCredential):
            return False
        return super().__eq__(other) and \
               self.vault == other.vault and \
               self.query_string == other.query_string

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def vault(self):
        """
        Reference to the CyberArk vault to use.

        :rtype: ``str``
        """
        return self._vault[0]

    @vault.setter
    def vault(self, value):
        self._vault = (value, True)

    @property
    def query_string(self):
        """
        Query to find a credential in the CyberArk vault.

        :rtype: ``str``
        """
        return self._query_string[0]

    @query_string.setter
    def query_string(self, value):
        self._query_string = (value, True)

