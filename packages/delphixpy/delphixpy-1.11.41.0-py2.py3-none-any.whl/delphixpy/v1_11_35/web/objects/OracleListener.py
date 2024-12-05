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
#     /delphix-oracle-listener.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_35.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_35 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleListener(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_35.web.vo.NamedUserObject` *)* An Oracle
    listener.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleListener", True)
        self._environment = (self.__undef__, True)
        self._protocol_addresses = (self.__undef__, True)
        self._client_endpoints = (self.__undef__, True)
        self._discovered = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._environment = (data.get("environment", obj.__undef__), dirty)
        if obj._environment[0] is not None and obj._environment[0] is not obj.__undef__:
            assert isinstance(obj._environment[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._environment[0], type(obj._environment[0])))
            common.validate_format(obj._environment[0], "objectReference", None, None)
        obj._protocol_addresses = []
        for item in data.get("protocolAddresses") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "oracleProtocolAddress", None, None)
            obj._protocol_addresses.append(item)
        obj._protocol_addresses = (obj._protocol_addresses, dirty)
        obj._client_endpoints = []
        for item in data.get("clientEndpoints") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._client_endpoints.append(item)
        obj._client_endpoints = (obj._client_endpoints, dirty)
        obj._discovered = (data.get("discovered", obj.__undef__), dirty)
        if obj._discovered[0] is not None and obj._discovered[0] is not obj.__undef__:
            assert isinstance(obj._discovered[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._discovered[0], type(obj._discovered[0])))
            common.validate_format(obj._discovered[0], "None", None, None)
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
        if "environment" == "type" or (self.environment is not self.__undef__ and (not (dirty and not self._environment[1]) or self.is_dirty_list(self.environment, self._environment) or belongs_to_parent)):
            dct["environment"] = dictify(self.environment)
        if "protocol_addresses" == "type" or (self.protocol_addresses is not self.__undef__ and (not (dirty and not self._protocol_addresses[1]) or self.is_dirty_list(self.protocol_addresses, self._protocol_addresses) or belongs_to_parent)):
            dct["protocolAddresses"] = dictify(self.protocol_addresses, prop_is_list_or_vo=True)
        if "client_endpoints" == "type" or (self.client_endpoints is not self.__undef__ and (not (dirty and not self._client_endpoints[1]))):
            dct["clientEndpoints"] = dictify(self.client_endpoints)
        if dirty and "clientEndpoints" in dct:
            del dct["clientEndpoints"]
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._environment = (self._environment[0], True)
        self._protocol_addresses = (self._protocol_addresses[0], True)
        self._client_endpoints = (self._client_endpoints[0], True)
        self._discovered = (self._discovered[0], True)

    def is_dirty(self):
        return any([self._environment[1], self._protocol_addresses[1], self._client_endpoints[1], self._discovered[1]])

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
        if not isinstance(other, OracleListener):
            return False
        return super().__eq__(other) and \
               self.environment == other.environment and \
               self.protocol_addresses == other.protocol_addresses and \
               self.client_endpoints == other.client_endpoints and \
               self.discovered == other.discovered

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def environment(self):
        """
        Reference to the environment this listener is associated with.

        :rtype: ``str``
        """
        return self._environment[0]

    @environment.setter
    def environment(self, value):
        self._environment = (value, True)

    @property
    def protocol_addresses(self):
        """
        The list of protocol addresses for this listener. These are used for
        the local_listener parameter when provisioning VDBs.

        :rtype: ``list`` of ``str``
        """
        return self._protocol_addresses[0]

    @protocol_addresses.setter
    def protocol_addresses(self, value):
        self._protocol_addresses = (value, True)

    @property
    def client_endpoints(self):
        """
        The list of client endpoints for this listener of the format
        hostname:port. These are used when constructing the JDBC connection
        string.

        :rtype: ``list`` of ``str``
        """
        return self._client_endpoints[0]

    @property
    def discovered(self):
        """
        Whether this listener was automatically discovered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

