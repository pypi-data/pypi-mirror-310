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
#     /delphix-hashicorp-vault-credential.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.AbstractVaultCredential import AbstractVaultCredential
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HashiCorpVaultCredential(AbstractVaultCredential):
    """
    *(extends* :py:class:`v1_11_18.web.vo.AbstractVaultCredential` *)* The
    HashiCorp vault based security credential.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HashiCorpVaultCredential", True)
        self._vault = (self.__undef__, True)
        self._engine = (self.__undef__, True)
        self._path = (self.__undef__, True)
        self._username_key = (self.__undef__, True)
        self._secret_key = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._vault = (data.get("vault", obj.__undef__), dirty)
        if obj._vault[0] is not None and obj._vault[0] is not obj.__undef__:
            assert isinstance(obj._vault[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._vault[0], type(obj._vault[0])))
            common.validate_format(obj._vault[0], "objectReference", None, None)
        obj._engine = (data.get("engine", obj.__undef__), dirty)
        if obj._engine[0] is not None and obj._engine[0] is not obj.__undef__:
            assert isinstance(obj._engine[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine[0], type(obj._engine[0])))
            common.validate_format(obj._engine[0], "None", None, None)
        obj._path = (data.get("path", obj.__undef__), dirty)
        if obj._path[0] is not None and obj._path[0] is not obj.__undef__:
            assert isinstance(obj._path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._path[0], type(obj._path[0])))
            common.validate_format(obj._path[0], "None", None, None)
        obj._username_key = (data.get("usernameKey", obj.__undef__), dirty)
        if obj._username_key[0] is not None and obj._username_key[0] is not obj.__undef__:
            assert isinstance(obj._username_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username_key[0], type(obj._username_key[0])))
            common.validate_format(obj._username_key[0], "None", None, None)
        obj._secret_key = (data.get("secretKey", obj.__undef__), dirty)
        if obj._secret_key[0] is not None and obj._secret_key[0] is not obj.__undef__:
            assert isinstance(obj._secret_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._secret_key[0], type(obj._secret_key[0])))
            common.validate_format(obj._secret_key[0], "None", None, None)
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
        if "engine" == "type" or (self.engine is not self.__undef__ and (not (dirty and not self._engine[1]) or self.is_dirty_list(self.engine, self._engine) or belongs_to_parent)):
            dct["engine"] = dictify(self.engine)
        if "path" == "type" or (self.path is not self.__undef__ and (not (dirty and not self._path[1]) or self.is_dirty_list(self.path, self._path) or belongs_to_parent)):
            dct["path"] = dictify(self.path)
        if "username_key" == "type" or (self.username_key is not self.__undef__ and (not (dirty and not self._username_key[1]) or self.is_dirty_list(self.username_key, self._username_key) or belongs_to_parent)):
            dct["usernameKey"] = dictify(self.username_key)
        if "secret_key" == "type" or (self.secret_key is not self.__undef__ and (not (dirty and not self._secret_key[1]) or self.is_dirty_list(self.secret_key, self._secret_key) or belongs_to_parent)):
            dct["secretKey"] = dictify(self.secret_key)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._vault = (self._vault[0], True)
        self._engine = (self._engine[0], True)
        self._path = (self._path[0], True)
        self._username_key = (self._username_key[0], True)
        self._secret_key = (self._secret_key[0], True)

    def is_dirty(self):
        return any([self._vault[1], self._engine[1], self._path[1], self._username_key[1], self._secret_key[1]])

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
        if not isinstance(other, HashiCorpVaultCredential):
            return False
        return super().__eq__(other) and \
               self.vault == other.vault and \
               self.engine == other.engine and \
               self.path == other.path and \
               self.username_key == other.username_key and \
               self.secret_key == other.secret_key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def vault(self):
        """
        Reference to the HashiCorp vault to use.

        :rtype: ``str``
        """
        return self._vault[0]

    @vault.setter
    def vault(self, value):
        self._vault = (value, True)

    @property
    def engine(self):
        """
        Vault engine where the credential is stored.

        :rtype: ``str``
        """
        return self._engine[0]

    @engine.setter
    def engine(self, value):
        self._engine = (value, True)

    @property
    def path(self):
        """
        Path in the vault engine where the credential is stored.

        :rtype: ``str``
        """
        return self._path[0]

    @path.setter
    def path(self, value):
        self._path = (value, True)

    @property
    def username_key(self):
        """
        Key for the username in the key-value store.

        :rtype: ``str``
        """
        return self._username_key[0]

    @username_key.setter
    def username_key(self, value):
        self._username_key = (value, True)

    @property
    def secret_key(self):
        """
        Key for the secret (password or SSH key) in the key-value store.

        :rtype: ``str``
        """
        return self._secret_key[0]

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = (value, True)

