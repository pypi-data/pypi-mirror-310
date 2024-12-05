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
#     /delphix-pem-client-certificate.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.ClientCertificate import ClientCertificate
from delphixpy.v1_11_21 import factory
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PemClientCertificate(ClientCertificate):
    """
    *(extends* :py:class:`v1_11_21.web.vo.ClientCertificate` *)* Client
    certificate.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PemClientCertificate", True)
        self._private_key = (self.__undef__, True)
        self._client_certificate_chain = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._private_key = (data.get("privateKey", obj.__undef__), dirty)
        if obj._private_key[0] is not None and obj._private_key[0] is not obj.__undef__:
            assert isinstance(obj._private_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._private_key[0], type(obj._private_key[0])))
            common.validate_format(obj._private_key[0], "password", None, None)
        if "clientCertificateChain" in data and data["clientCertificateChain"] is not None:
            obj._client_certificate_chain = (factory.create_object(data["clientCertificateChain"], "PemCertificateChain"), dirty)
            factory.validate_type(obj._client_certificate_chain[0], "PemCertificateChain")
        else:
            obj._client_certificate_chain = (obj.__undef__, dirty)
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
        if "private_key" == "type" or (self.private_key is not self.__undef__ and (not (dirty and not self._private_key[1]) or self.is_dirty_list(self.private_key, self._private_key) or belongs_to_parent)):
            dct["privateKey"] = dictify(self.private_key)
        if "client_certificate_chain" == "type" or (self.client_certificate_chain is not self.__undef__ and (not (dirty and not self._client_certificate_chain[1]) or self.is_dirty_list(self.client_certificate_chain, self._client_certificate_chain) or belongs_to_parent)):
            dct["clientCertificateChain"] = dictify(self.client_certificate_chain, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._private_key = (self._private_key[0], True)
        self._client_certificate_chain = (self._client_certificate_chain[0], True)

    def is_dirty(self):
        return any([self._private_key[1], self._client_certificate_chain[1]])

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
        if not isinstance(other, PemClientCertificate):
            return False
        return super().__eq__(other) and \
               self.private_key == other.private_key and \
               self.client_certificate_chain == other.client_certificate_chain

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def private_key(self):
        """
        Private key in PEM format for authentication to the vault.

        :rtype: ``str``
        """
        return self._private_key[0]

    @private_key.setter
    def private_key(self, value):
        self._private_key = (value, True)

    @property
    def client_certificate_chain(self):
        """
        Client certificate chain in PEM format for authentication to the vault.

        :rtype: :py:class:`v1_11_21.web.vo.PemCertificateChain`
        """
        return self._client_certificate_chain[0]

    @client_certificate_chain.setter
    def client_certificate_chain(self, value):
        self._client_certificate_chain = (value, True)

