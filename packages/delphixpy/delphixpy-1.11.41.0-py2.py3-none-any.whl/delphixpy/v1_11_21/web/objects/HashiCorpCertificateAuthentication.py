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
#     /delphix-hashicorp-certificate-authentication.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.HashiCorpAuthentication import HashiCorpAuthentication
from delphixpy.v1_11_21 import factory
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HashiCorpCertificateAuthentication(HashiCorpAuthentication):
    """
    *(extends* :py:class:`v1_11_21.web.vo.HashiCorpAuthentication` *)* Client
    certificate for authenticating to a HashiCorp vault.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HashiCorpCertificateAuthentication", True)
        self._client_certificate = (self.__undef__, True)
        self._role_name = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "clientCertificate" in data and data["clientCertificate"] is not None:
            obj._client_certificate = (factory.create_object(data["clientCertificate"], "ClientCertificate"), dirty)
            factory.validate_type(obj._client_certificate[0], "ClientCertificate")
        else:
            obj._client_certificate = (obj.__undef__, dirty)
        obj._role_name = (data.get("roleName", obj.__undef__), dirty)
        if obj._role_name[0] is not None and obj._role_name[0] is not obj.__undef__:
            assert isinstance(obj._role_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._role_name[0], type(obj._role_name[0])))
            common.validate_format(obj._role_name[0], "None", None, None)
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
        if "client_certificate" == "type" or (self.client_certificate is not self.__undef__ and (not (dirty and not self._client_certificate[1]) or self.is_dirty_list(self.client_certificate, self._client_certificate) or belongs_to_parent)):
            dct["clientCertificate"] = dictify(self.client_certificate, prop_is_list_or_vo=True)
        if "role_name" == "type" or (self.role_name is not self.__undef__ and (not (dirty and not self._role_name[1]) or self.is_dirty_list(self.role_name, self._role_name) or belongs_to_parent)):
            dct["roleName"] = dictify(self.role_name)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._client_certificate = (self._client_certificate[0], True)
        self._role_name = (self._role_name[0], True)

    def is_dirty(self):
        return any([self._client_certificate[1], self._role_name[1]])

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
        if not isinstance(other, HashiCorpCertificateAuthentication):
            return False
        return super().__eq__(other) and \
               self.client_certificate == other.client_certificate and \
               self.role_name == other.role_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def client_certificate(self):
        """
        Client certificate for authenticating to the vault.

        :rtype: :py:class:`v1_11_21.web.vo.ClientCertificate`
        """
        return self._client_certificate[0]

    @client_certificate.setter
    def client_certificate(self, value):
        self._client_certificate = (value, True)

    @property
    def role_name(self):
        """
        Role name for authenticating to the vault.

        :rtype: ``str``
        """
        return self._role_name[0]

    @role_name.setter
    def role_name(self, value):
        self._role_name = (value, True)

