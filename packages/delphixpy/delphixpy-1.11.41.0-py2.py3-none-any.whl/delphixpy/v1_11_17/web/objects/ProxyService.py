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
#     /delphix-proxy-service.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_17.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_17 import factory
from delphixpy.v1_11_17 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ProxyService(TypedObject):
    """
    *(extends* :py:class:`v1_11_17.web.vo.TypedObject` *)* Proxy service
    configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ProxyService", True)
        self._https = (self.__undef__, True)
        self._socks = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "https" in data and data["https"] is not None:
            obj._https = (factory.create_object(data["https"], "ProxyConfiguration"), dirty)
            factory.validate_type(obj._https[0], "ProxyConfiguration")
        else:
            obj._https = (obj.__undef__, dirty)
        if "socks" in data and data["socks"] is not None:
            obj._socks = (factory.create_object(data["socks"], "ProxyConfiguration"), dirty)
            factory.validate_type(obj._socks[0], "ProxyConfiguration")
        else:
            obj._socks = (obj.__undef__, dirty)
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
        if "https" == "type" or (self.https is not self.__undef__ and (not (dirty and not self._https[1]) or self.is_dirty_list(self.https, self._https) or belongs_to_parent)):
            dct["https"] = dictify(self.https, prop_is_list_or_vo=True)
        if "socks" == "type" or (self.socks is not self.__undef__ and (not (dirty and not self._socks[1]) or self.is_dirty_list(self.socks, self._socks) or belongs_to_parent)):
            dct["socks"] = dictify(self.socks, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._https = (self._https[0], True)
        self._socks = (self._socks[0], True)

    def is_dirty(self):
        return any([self._https[1], self._socks[1]])

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
        if not isinstance(other, ProxyService):
            return False
        return super().__eq__(other) and \
               self.https == other.https and \
               self.socks == other.socks

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def https(self):
        """
        HTTPS proxy configuration.

        :rtype: :py:class:`v1_11_17.web.vo.ProxyConfiguration`
        """
        return self._https[0]

    @https.setter
    def https(self, value):
        self._https = (value, True)

    @property
    def socks(self):
        """
        SOCKS proxy configuration.

        :rtype: :py:class:`v1_11_17.web.vo.ProxyConfiguration`
        """
        return self._socks[0]

    @socks.setter
    def socks(self, value):
        self._socks = (value, True)

