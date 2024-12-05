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
#     /delphix-cyberark-vault-test-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.HostedVaultTestParameters import HostedVaultTestParameters
from delphixpy.v1_11_27 import factory
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CyberArkPasswordVaultTestParameters(HostedVaultTestParameters):
    """
    *(extends* :py:class:`v1_11_27.web.vo.HostedVaultTestParameters` *)*
    CyberArk password vault test configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CyberArkPasswordVaultTestParameters", True)
        self._application_id = (self.__undef__, True)
        self._client_certificate = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "applicationId" not in data:
            raise ValueError("Missing required property \"applicationId\".")
        obj._application_id = (data.get("applicationId", obj.__undef__), dirty)
        if obj._application_id[0] is not None and obj._application_id[0] is not obj.__undef__:
            assert isinstance(obj._application_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._application_id[0], type(obj._application_id[0])))
            common.validate_format(obj._application_id[0], "None", None, None)
        if "clientCertificate" not in data:
            raise ValueError("Missing required property \"clientCertificate\".")
        if "clientCertificate" in data and data["clientCertificate"] is not None:
            obj._client_certificate = (factory.create_object(data["clientCertificate"], "ClientCertificate"), dirty)
            factory.validate_type(obj._client_certificate[0], "ClientCertificate")
        else:
            obj._client_certificate = (obj.__undef__, dirty)
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
        if "application_id" == "type" or (self.application_id is not self.__undef__ and (not (dirty and not self._application_id[1]) or self.is_dirty_list(self.application_id, self._application_id) or belongs_to_parent)):
            dct["applicationId"] = dictify(self.application_id)
        if "client_certificate" == "type" or (self.client_certificate is not self.__undef__ and (not (dirty and not self._client_certificate[1]) or self.is_dirty_list(self.client_certificate, self._client_certificate) or belongs_to_parent)):
            dct["clientCertificate"] = dictify(self.client_certificate, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._application_id = (self._application_id[0], True)
        self._client_certificate = (self._client_certificate[0], True)

    def is_dirty(self):
        return any([self._application_id[1], self._client_certificate[1]])

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
        if not isinstance(other, CyberArkPasswordVaultTestParameters):
            return False
        return super().__eq__(other) and \
               self.application_id == other.application_id and \
               self.client_certificate == other.client_certificate

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def application_id(self):
        """
        Application identifier in the vault.

        :rtype: ``str``
        """
        return self._application_id[0]

    @application_id.setter
    def application_id(self, value):
        self._application_id = (value, True)

    @property
    def client_certificate(self):
        """
        Client certificate for authentication to the vault.

        :rtype: :py:class:`v1_11_27.web.vo.ClientCertificate`
        """
        return self._client_certificate[0]

    @client_certificate.setter
    def client_certificate(self, value):
        self._client_certificate = (value, True)

