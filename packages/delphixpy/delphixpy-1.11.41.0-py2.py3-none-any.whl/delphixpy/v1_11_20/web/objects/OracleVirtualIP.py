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
#     /delphix-oracle-virtual-ip.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleVirtualIP(TypedObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.TypedObject` *)* The parameters used
    for virtual IP operations.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleVirtualIP", True)
        self._ip = (self.__undef__, True)
        self._domain_name = (self.__undef__, True)
        self._discovered = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "ip" not in data:
            raise ValueError("Missing required property \"ip\".")
        obj._ip = (data.get("ip", obj.__undef__), dirty)
        if obj._ip[0] is not None and obj._ip[0] is not obj.__undef__:
            assert isinstance(obj._ip[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ip[0], type(obj._ip[0])))
            common.validate_format(obj._ip[0], "ipv4Address", None, None)
        if "domainName" not in data:
            raise ValueError("Missing required property \"domainName\".")
        obj._domain_name = (data.get("domainName", obj.__undef__), dirty)
        if obj._domain_name[0] is not None and obj._domain_name[0] is not obj.__undef__:
            assert isinstance(obj._domain_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._domain_name[0], type(obj._domain_name[0])))
            common.validate_format(obj._domain_name[0], "None", None, None)
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
        if "ip" == "type" or (self.ip is not self.__undef__ and (not (dirty and not self._ip[1]) or self.is_dirty_list(self.ip, self._ip) or belongs_to_parent)):
            dct["ip"] = dictify(self.ip)
        if "domain_name" == "type" or (self.domain_name is not self.__undef__ and (not (dirty and not self._domain_name[1]) or self.is_dirty_list(self.domain_name, self._domain_name) or belongs_to_parent)):
            dct["domainName"] = dictify(self.domain_name)
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._ip = (self._ip[0], True)
        self._domain_name = (self._domain_name[0], True)
        self._discovered = (self._discovered[0], True)

    def is_dirty(self):
        return any([self._ip[1], self._domain_name[1], self._discovered[1]])

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
        if not isinstance(other, OracleVirtualIP):
            return False
        return super().__eq__(other) and \
               self.ip == other.ip and \
               self.domain_name == other.domain_name and \
               self.discovered == other.discovered

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def ip(self):
        """
        The virtual IP address.

        :rtype: ``str``
        """
        return self._ip[0]

    @ip.setter
    def ip(self, value):
        self._ip = (value, True)

    @property
    def domain_name(self):
        """
        The name of the domain where the cluster is residing.

        :rtype: ``str``
        """
        return self._domain_name[0]

    @domain_name.setter
    def domain_name(self, value):
        self._domain_name = (value, True)

    @property
    def discovered(self):
        """
        A boolean indicating whether this VIP was automatically discovered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

