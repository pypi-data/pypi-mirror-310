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
#     /delphix-repave-dns-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RepaveDNSConfig(TypedObject):
    """
    *(extends* :py:class:`v1_11_21.web.vo.TypedObject` *)* DNS Client
    Configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RepaveDNSConfig", True)
        self._source = (self.__undef__, True)
        self._domain = (self.__undef__, True)
        self._servers = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._source = (data.get("source", obj.__undef__), dirty)
        if obj._source[0] is not None and obj._source[0] is not obj.__undef__:
            assert isinstance(obj._source[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source[0], type(obj._source[0])))
            assert obj._source[0] in ['STATIC', 'DHCP'], "Expected enum ['STATIC', 'DHCP'] but got %s" % obj._source[0]
            common.validate_format(obj._source[0], "None", None, None)
        obj._domain = []
        for item in data.get("domain") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._domain.append(item)
        obj._domain = (obj._domain, dirty)
        obj._servers = []
        for item in data.get("servers") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "ipAddress", None, None)
            obj._servers.append(item)
        obj._servers = (obj._servers, dirty)
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
        if "source" == "type" or (self.source is not self.__undef__ and (not (dirty and not self._source[1]))):
            dct["source"] = dictify(self.source)
        if dirty and "source" in dct:
            del dct["source"]
        if "domain" == "type" or (self.domain is not self.__undef__ and (not (dirty and not self._domain[1]))):
            dct["domain"] = dictify(self.domain)
        if dirty and "domain" in dct:
            del dct["domain"]
        if "servers" == "type" or (self.servers is not self.__undef__ and (not (dirty and not self._servers[1]))):
            dct["servers"] = dictify(self.servers)
        if dirty and "servers" in dct:
            del dct["servers"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._source = (self._source[0], True)
        self._domain = (self._domain[0], True)
        self._servers = (self._servers[0], True)

    def is_dirty(self):
        return any([self._source[1], self._domain[1], self._servers[1]])

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
        if not isinstance(other, RepaveDNSConfig):
            return False
        return super().__eq__(other) and \
               self.source == other.source and \
               self.domain == other.domain and \
               self.servers == other.servers

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.source,
            self.domain,
            self.servers,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def source(self):
        """
        The source of the DNS configuration (STATIC or DHCP). *(permitted
        values: STATIC, DHCP)*

        :rtype: ``str``
        """
        return self._source[0]

    @property
    def domain(self):
        """
        One of more DNS domain names.

        :rtype: ``list`` of ``str``
        """
        return self._domain[0]

    @property
    def servers(self):
        """
        List of DNS servers.

        :rtype: ``list`` of ``str``
        """
        return self._servers[0]

