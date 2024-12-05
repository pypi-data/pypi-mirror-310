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
#     /delphix-hashicorp-vault.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.PasswordVault import PasswordVault
from delphixpy.v1_11_18 import factory
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HashiCorpVault(PasswordVault):
    """
    *(extends* :py:class:`v1_11_18.web.vo.PasswordVault` *)* HashiCorpVault
    password vault configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HashiCorpVault", True)
        self._authentication = (self.__undef__, True)
        self._vault_namespace = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "authentication" in data and data["authentication"] is not None:
            obj._authentication = (factory.create_object(data["authentication"], "HashiCorpAuthentication"), dirty)
            factory.validate_type(obj._authentication[0], "HashiCorpAuthentication")
        else:
            obj._authentication = (obj.__undef__, dirty)
        obj._vault_namespace = (data.get("vaultNamespace", obj.__undef__), dirty)
        if obj._vault_namespace[0] is not None and obj._vault_namespace[0] is not obj.__undef__:
            assert isinstance(obj._vault_namespace[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._vault_namespace[0], type(obj._vault_namespace[0])))
            common.validate_format(obj._vault_namespace[0], "noLinebreaks", None, None)
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
        if "authentication" == "type" or (self.authentication is not self.__undef__ and (not (dirty and not self._authentication[1]) or self.is_dirty_list(self.authentication, self._authentication) or belongs_to_parent)):
            dct["authentication"] = dictify(self.authentication, prop_is_list_or_vo=True)
        if "vault_namespace" == "type" or (self.vault_namespace is not self.__undef__ and (not (dirty and not self._vault_namespace[1]) or self.is_dirty_list(self.vault_namespace, self._vault_namespace) or belongs_to_parent)):
            dct["vaultNamespace"] = dictify(self.vault_namespace)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._authentication = (self._authentication[0], True)
        self._vault_namespace = (self._vault_namespace[0], True)

    def is_dirty(self):
        return any([self._authentication[1], self._vault_namespace[1]])

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
        if not isinstance(other, HashiCorpVault):
            return False
        return super().__eq__(other) and \
               self.authentication == other.authentication and \
               self.vault_namespace == other.vault_namespace

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def authentication(self):
        """
        Parameters for authenticating to a HashiCorp vault.

        :rtype: :py:class:`v1_11_18.web.vo.HashiCorpAuthentication`
        """
        return self._authentication[0]

    @authentication.setter
    def authentication(self, value):
        self._authentication = (value, True)

    @property
    def vault_namespace(self):
        """
        Namespace within the vault.

        :rtype: ``str`` *or* ``null``
        """
        return self._vault_namespace[0]

    @vault_namespace.setter
    def vault_namespace(self, value):
        self._vault_namespace = (value, True)

