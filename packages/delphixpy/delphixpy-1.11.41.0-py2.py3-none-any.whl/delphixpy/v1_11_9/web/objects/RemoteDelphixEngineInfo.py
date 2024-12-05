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
#     /delphix-network-throughput-test-engine-login.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_9.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_9 import factory
from delphixpy.v1_11_9 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RemoteDelphixEngineInfo(TypedObject):
    """
    *(extends* :py:class:`v1_11_9.web.vo.TypedObject` *)* Parameters for
    logging into another Delphix Engine when running a network throughput test.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RemoteDelphixEngineInfo", True)
        self._address = (self.__undef__, True)
        self._principal = (self.__undef__, True)
        self._credential = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._address = (data.get("address", obj.__undef__), dirty)
        if obj._address[0] is not None and obj._address[0] is not obj.__undef__:
            assert isinstance(obj._address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._address[0], type(obj._address[0])))
            common.validate_format(obj._address[0], "host", None, None)
        obj._principal = (data.get("principal", obj.__undef__), dirty)
        if obj._principal[0] is not None and obj._principal[0] is not obj.__undef__:
            assert isinstance(obj._principal[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._principal[0], type(obj._principal[0])))
            common.validate_format(obj._principal[0], "None", None, None)
        if "credential" in data and data["credential"] is not None:
            obj._credential = (factory.create_object(data["credential"], "PasswordCredential"), dirty)
            factory.validate_type(obj._credential[0], "PasswordCredential")
        else:
            obj._credential = (obj.__undef__, dirty)
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
        if "address" == "type" or (self.address is not self.__undef__ and (not (dirty and not self._address[1]) or self.is_dirty_list(self.address, self._address) or belongs_to_parent)):
            dct["address"] = dictify(self.address)
        if "principal" == "type" or (self.principal is not self.__undef__ and (not (dirty and not self._principal[1]) or self.is_dirty_list(self.principal, self._principal) or belongs_to_parent)):
            dct["principal"] = dictify(self.principal)
        if "credential" == "type" or (self.credential is not self.__undef__ and (not (dirty and not self._credential[1]) or self.is_dirty_list(self.credential, self._credential) or belongs_to_parent)):
            dct["credential"] = dictify(self.credential, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._address = (self._address[0], True)
        self._principal = (self._principal[0], True)
        self._credential = (self._credential[0], True)

    def is_dirty(self):
        return any([self._address[1], self._principal[1], self._credential[1]])

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
        if not isinstance(other, RemoteDelphixEngineInfo):
            return False
        return super().__eq__(other) and \
               self.address == other.address and \
               self.principal == other.principal and \
               self.credential == other.credential

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def address(self):
        """
        Address of other Delphix Engine.

        :rtype: ``str``
        """
        return self._address[0]

    @address.setter
    def address(self, value):
        self._address = (value, True)

    @property
    def principal(self):
        """
        Username for the other Delphix Engine.

        :rtype: ``str``
        """
        return self._principal[0]

    @principal.setter
    def principal(self, value):
        self._principal = (value, True)

    @property
    def credential(self):
        """
        Password for the other Delphix Engine.

        :rtype: :py:class:`v1_11_9.web.vo.PasswordCredential`
        """
        return self._credential[0]

    @credential.setter
    def credential(self, value):
        self._credential = (value, True)

