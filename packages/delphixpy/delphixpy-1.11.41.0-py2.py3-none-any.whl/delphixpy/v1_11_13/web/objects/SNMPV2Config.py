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
#     /delphix-snmp-v2-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_13.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_13 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SNMPV2Config(TypedObject):
    """
    *(extends* :py:class:`v1_11_13.web.vo.TypedObject` *)* SNMP configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SNMPV2Config", True)
        self._enabled = (self.__undef__, True)
        self._community = (self.__undef__, True)
        self._authorized_network = (self.__undef__, True)
        self._location = (self.__undef__, True)
        self._severity = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._community = (data.get("community", obj.__undef__), dirty)
        if obj._community[0] is not None and obj._community[0] is not obj.__undef__:
            assert isinstance(obj._community[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._community[0], type(obj._community[0])))
            common.validate_format(obj._community[0], "None", None, None)
        obj._authorized_network = (data.get("authorizedNetwork", obj.__undef__), dirty)
        if obj._authorized_network[0] is not None and obj._authorized_network[0] is not obj.__undef__:
            assert isinstance(obj._authorized_network[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._authorized_network[0], type(obj._authorized_network[0])))
            common.validate_format(obj._authorized_network[0], "cidrAddress", None, None)
        obj._location = (data.get("location", obj.__undef__), dirty)
        if obj._location[0] is not None and obj._location[0] is not obj.__undef__:
            assert isinstance(obj._location[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._location[0], type(obj._location[0])))
            common.validate_format(obj._location[0], "None", None, None)
        obj._severity = (data.get("severity", obj.__undef__), dirty)
        if obj._severity[0] is not None and obj._severity[0] is not obj.__undef__:
            assert isinstance(obj._severity[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._severity[0], type(obj._severity[0])))
            assert obj._severity[0] in ['CRITICAL', 'WARNING', 'INFORMATIONAL'], "Expected enum ['CRITICAL', 'WARNING', 'INFORMATIONAL'] but got %s" % obj._severity[0]
            common.validate_format(obj._severity[0], "None", None, None)
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
        if "enabled" == "type" or (self.enabled is not self.__undef__ and (not (dirty and not self._enabled[1]) or self.is_dirty_list(self.enabled, self._enabled) or belongs_to_parent)):
            dct["enabled"] = dictify(self.enabled)
        elif belongs_to_parent and self.enabled is self.__undef__:
            dct["enabled"] = False
        if "community" == "type" or (self.community is not self.__undef__ and (not (dirty and not self._community[1]) or self.is_dirty_list(self.community, self._community) or belongs_to_parent)):
            dct["community"] = dictify(self.community)
        if "authorized_network" == "type" or (self.authorized_network is not self.__undef__ and (not (dirty and not self._authorized_network[1]) or self.is_dirty_list(self.authorized_network, self._authorized_network) or belongs_to_parent)):
            dct["authorizedNetwork"] = dictify(self.authorized_network)
        elif belongs_to_parent and self.authorized_network is self.__undef__:
            dct["authorizedNetwork"] = "0.0.0.0/0"
        if "location" == "type" or (self.location is not self.__undef__ and (not (dirty and not self._location[1]) or self.is_dirty_list(self.location, self._location) or belongs_to_parent)):
            dct["location"] = dictify(self.location)
        if "severity" == "type" or (self.severity is not self.__undef__ and (not (dirty and not self._severity[1]) or self.is_dirty_list(self.severity, self._severity) or belongs_to_parent)):
            dct["severity"] = dictify(self.severity)
        elif belongs_to_parent and self.severity is self.__undef__:
            dct["severity"] = "WARNING"
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._community = (self._community[0], True)
        self._authorized_network = (self._authorized_network[0], True)
        self._location = (self._location[0], True)
        self._severity = (self._severity[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._community[1], self._authorized_network[1], self._location[1], self._severity[1]])

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
        if not isinstance(other, SNMPV2Config):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.community == other.community and \
               self.authorized_network == other.authorized_network and \
               self.location == other.location and \
               self.severity == other.severity

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        True if the SNMP service is enabled.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def community(self):
        """
        The community string that clients must provide when querying this
        server.

        :rtype: ``str``
        """
        return self._community[0]

    @community.setter
    def community(self, value):
        self._community = (value, True)

    @property
    def authorized_network(self):
        """
        *(default value: 0.0.0.0/0)* The network which is authorized to query
        this SNMP server, in CIDR notation. Toallow any client, then leave
        unset or set to 0.0.0.0/0. To block all clients, set to 127.0.0.1/8.

        :rtype: ``str``
        """
        return self._authorized_network[0]

    @authorized_network.setter
    def authorized_network(self, value):
        self._authorized_network = (value, True)

    @property
    def location(self):
        """
        The physical location of this Delphix Engine (OID 1.3.6.1.2.1.1.6 -
        sysLocation).

        :rtype: ``str``
        """
        return self._location[0]

    @location.setter
    def location(self, value):
        self._location = (value, True)

    @property
    def severity(self):
        """
        *(default value: WARNING)* SNMP trap severity. SNMP managers are only
        notified of events at or above this level. *(permitted values:
        CRITICAL, WARNING, INFORMATIONAL)*

        :rtype: ``str``
        """
        return self._severity[0]

    @severity.setter
    def severity(self, value):
        self._severity = (value, True)

