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
#     /delphix-azure-authentication.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_22.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_22 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AzureAuthentication(TypedObject):
    """
    *(extends* :py:class:`v1_11_22.web.vo.TypedObject` *)* Parameters for
    authenticating to an Azure vault.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AzureAuthentication", True)
        self._tenant_id = (self.__undef__, True)
        self._client_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._tenant_id = (data.get("tenantId", obj.__undef__), dirty)
        if obj._tenant_id[0] is not None and obj._tenant_id[0] is not obj.__undef__:
            assert isinstance(obj._tenant_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tenant_id[0], type(obj._tenant_id[0])))
            common.validate_format(obj._tenant_id[0], "None", None, None)
        obj._client_id = (data.get("clientId", obj.__undef__), dirty)
        if obj._client_id[0] is not None and obj._client_id[0] is not obj.__undef__:
            assert isinstance(obj._client_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._client_id[0], type(obj._client_id[0])))
            common.validate_format(obj._client_id[0], "None", None, None)
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
        if "tenant_id" == "type" or (self.tenant_id is not self.__undef__ and (not (dirty and not self._tenant_id[1]) or self.is_dirty_list(self.tenant_id, self._tenant_id) or belongs_to_parent)):
            dct["tenantId"] = dictify(self.tenant_id)
        if "client_id" == "type" or (self.client_id is not self.__undef__ and (not (dirty and not self._client_id[1]) or self.is_dirty_list(self.client_id, self._client_id) or belongs_to_parent)):
            dct["clientId"] = dictify(self.client_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._tenant_id = (self._tenant_id[0], True)
        self._client_id = (self._client_id[0], True)

    def is_dirty(self):
        return any([self._tenant_id[1], self._client_id[1]])

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
        if not isinstance(other, AzureAuthentication):
            return False
        return super().__eq__(other) and \
               self.tenant_id == other.tenant_id and \
               self.client_id == other.client_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def tenant_id(self):
        """
        Tenant identifier in Azure.

        :rtype: ``str``
        """
        return self._tenant_id[0]

    @tenant_id.setter
    def tenant_id(self, value):
        self._tenant_id = (value, True)

    @property
    def client_id(self):
        """
        Client identifier in Azure.

        :rtype: ``str``
        """
        return self._client_id[0]

    @client_id.setter
    def client_id(self, value):
        self._client_id = (value, True)

