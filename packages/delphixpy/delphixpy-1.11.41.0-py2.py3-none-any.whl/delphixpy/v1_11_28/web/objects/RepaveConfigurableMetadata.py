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
#     /delphix-repave-configurable-metadata.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_28.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_28 import factory
from delphixpy.v1_11_28 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RepaveConfigurableMetadata(TypedObject):
    """
    *(extends* :py:class:`v1_11_28.web.vo.TypedObject` *)* Engine configurable
    metadata for Repave.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RepaveConfigurableMetadata", True)
        self._hostname = (self.__undef__, True)
        self._static_host_address = (self.__undef__, True)
        self._kerberos_config = (self.__undef__, True)
        self._ntp_config = (self.__undef__, True)
        self._dns_config = (self.__undef__, True)
        self._api_version = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._hostname = (data.get("hostname", obj.__undef__), dirty)
        if obj._hostname[0] is not None and obj._hostname[0] is not obj.__undef__:
            assert isinstance(obj._hostname[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._hostname[0], type(obj._hostname[0])))
            common.validate_format(obj._hostname[0], "hostname", None, None)
        obj._static_host_address = []
        for item in data.get("staticHostAddress") or []:
            obj._static_host_address.append(factory.create_object(item))
            factory.validate_type(obj._static_host_address[-1], "StaticHostAddress")
        obj._static_host_address = (obj._static_host_address, dirty)
        if "kerberosConfig" in data and data["kerberosConfig"] is not None:
            obj._kerberos_config = (factory.create_object(data["kerberosConfig"], "KerberosConfig"), dirty)
            factory.validate_type(obj._kerberos_config[0], "KerberosConfig")
        else:
            obj._kerberos_config = (obj.__undef__, dirty)
        if "ntpConfig" in data and data["ntpConfig"] is not None:
            obj._ntp_config = (factory.create_object(data["ntpConfig"], "NTPConfig"), dirty)
            factory.validate_type(obj._ntp_config[0], "NTPConfig")
        else:
            obj._ntp_config = (obj.__undef__, dirty)
        if "dnsConfig" in data and data["dnsConfig"] is not None:
            obj._dns_config = (factory.create_object(data["dnsConfig"], "RepaveDNSConfig"), dirty)
            factory.validate_type(obj._dns_config[0], "RepaveDNSConfig")
        else:
            obj._dns_config = (obj.__undef__, dirty)
        if "apiVersion" in data and data["apiVersion"] is not None:
            obj._api_version = (factory.create_object(data["apiVersion"], "APIVersion"), dirty)
            factory.validate_type(obj._api_version[0], "APIVersion")
        else:
            obj._api_version = (obj.__undef__, dirty)
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
        if "hostname" == "type" or (self.hostname is not self.__undef__ and (not (dirty and not self._hostname[1]))):
            dct["hostname"] = dictify(self.hostname)
        if dirty and "hostname" in dct:
            del dct["hostname"]
        if "static_host_address" == "type" or (self.static_host_address is not self.__undef__ and (not (dirty and not self._static_host_address[1]))):
            dct["staticHostAddress"] = dictify(self.static_host_address)
        if dirty and "staticHostAddress" in dct:
            del dct["staticHostAddress"]
        if "kerberos_config" == "type" or (self.kerberos_config is not self.__undef__ and (not (dirty and not self._kerberos_config[1]))):
            dct["kerberosConfig"] = dictify(self.kerberos_config)
        if dirty and "kerberosConfig" in dct:
            del dct["kerberosConfig"]
        if "ntp_config" == "type" or (self.ntp_config is not self.__undef__ and (not (dirty and not self._ntp_config[1]))):
            dct["ntpConfig"] = dictify(self.ntp_config)
        if dirty and "ntpConfig" in dct:
            del dct["ntpConfig"]
        if "dns_config" == "type" or (self.dns_config is not self.__undef__ and (not (dirty and not self._dns_config[1]))):
            dct["dnsConfig"] = dictify(self.dns_config)
        if dirty and "dnsConfig" in dct:
            del dct["dnsConfig"]
        if "api_version" == "type" or (self.api_version is not self.__undef__ and (not (dirty and not self._api_version[1]))):
            dct["apiVersion"] = dictify(self.api_version)
        if dirty and "apiVersion" in dct:
            del dct["apiVersion"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._hostname = (self._hostname[0], True)
        self._static_host_address = (self._static_host_address[0], True)
        self._kerberos_config = (self._kerberos_config[0], True)
        self._ntp_config = (self._ntp_config[0], True)
        self._dns_config = (self._dns_config[0], True)
        self._api_version = (self._api_version[0], True)

    def is_dirty(self):
        return any([self._hostname[1], self._static_host_address[1], self._kerberos_config[1], self._ntp_config[1], self._dns_config[1], self._api_version[1]])

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
        if not isinstance(other, RepaveConfigurableMetadata):
            return False
        return super().__eq__(other) and \
               self.hostname == other.hostname and \
               self.static_host_address == other.static_host_address and \
               self.kerberos_config == other.kerberos_config and \
               self.ntp_config == other.ntp_config and \
               self.dns_config == other.dns_config and \
               self.api_version == other.api_version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.hostname,
            self.static_host_address,
            self.kerberos_config,
            self.ntp_config,
            self.dns_config,
            self.api_version,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def hostname(self):
        """
        System hostname.

        :rtype: ``str``
        """
        return self._hostname[0]

    @property
    def static_host_address(self):
        """
        Static mapping of hostname to IP address.

        :rtype: ``list`` of :py:class:`v1_11_28.web.vo.StaticHostAddress`
        """
        return self._static_host_address[0]

    @property
    def kerberos_config(self):
        """
        Kerberos Client Configuration.

        :rtype: :py:class:`v1_11_28.web.vo.KerberosConfig`
        """
        return self._kerberos_config[0]

    @property
    def ntp_config(self):
        """
        NTP configuration.

        :rtype: :py:class:`v1_11_28.web.vo.NTPConfig`
        """
        return self._ntp_config[0]

    @property
    def dns_config(self):
        """
        DNS Client Configuration.

        :rtype: :py:class:`v1_11_28.web.vo.RepaveDNSConfig`
        """
        return self._dns_config[0]

    @property
    def api_version(self):
        """
        API version.

        :rtype: :py:class:`v1_11_28.web.vo.APIVersion`
        """
        return self._api_version[0]

