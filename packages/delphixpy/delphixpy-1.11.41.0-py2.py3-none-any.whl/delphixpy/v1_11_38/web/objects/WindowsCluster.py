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
#     /delphix-windows-cluster.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.SourceEnvironment import SourceEnvironment
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class WindowsCluster(SourceEnvironment):
    """
    *(extends* :py:class:`v1_11_38.web.vo.SourceEnvironment` *)* A Windows
    cluster environment.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("WindowsCluster", True)
        self._proxy = (self.__undef__, True)
        self._target_proxy = (self.__undef__, True)
        self._address = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._proxy = (data.get("proxy", obj.__undef__), dirty)
        if obj._proxy[0] is not None and obj._proxy[0] is not obj.__undef__:
            assert isinstance(obj._proxy[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._proxy[0], type(obj._proxy[0])))
            common.validate_format(obj._proxy[0], "objectReference", None, None)
        obj._target_proxy = (data.get("targetProxy", obj.__undef__), dirty)
        if obj._target_proxy[0] is not None and obj._target_proxy[0] is not obj.__undef__:
            assert isinstance(obj._target_proxy[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_proxy[0], type(obj._target_proxy[0])))
            common.validate_format(obj._target_proxy[0], "objectReference", None, None)
        obj._address = (data.get("address", obj.__undef__), dirty)
        if obj._address[0] is not None and obj._address[0] is not obj.__undef__:
            assert isinstance(obj._address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._address[0], type(obj._address[0])))
            common.validate_format(obj._address[0], "None", None, None)
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
        if "proxy" == "type" or (self.proxy is not self.__undef__ and (not (dirty and not self._proxy[1]) or self.is_dirty_list(self.proxy, self._proxy) or belongs_to_parent)):
            dct["proxy"] = dictify(self.proxy)
        if "target_proxy" == "type" or (self.target_proxy is not self.__undef__ and (not (dirty and not self._target_proxy[1]) or self.is_dirty_list(self.target_proxy, self._target_proxy) or belongs_to_parent)):
            dct["targetProxy"] = dictify(self.target_proxy)
        if "address" == "type" or (self.address is not self.__undef__ and (not (dirty and not self._address[1]) or self.is_dirty_list(self.address, self._address) or belongs_to_parent)):
            dct["address"] = dictify(self.address)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._proxy = (self._proxy[0], True)
        self._target_proxy = (self._target_proxy[0], True)
        self._address = (self._address[0], True)

    def is_dirty(self):
        return any([self._proxy[1], self._target_proxy[1], self._address[1]])

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
        if not isinstance(other, WindowsCluster):
            return False
        return super().__eq__(other) and \
               self.proxy == other.proxy and \
               self.target_proxy == other.target_proxy and \
               self.address == other.address

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def proxy(self):
        """
        A reference to the proxy that will be used to discover the cluster.

        :rtype: ``str``
        """
        return self._proxy[0]

    @proxy.setter
    def proxy(self, value):
        self._proxy = (value, True)

    @property
    def target_proxy(self):
        """
        A reference to the proxy host that will be used for cluster support
        operations.

        :rtype: ``str``
        """
        return self._target_proxy[0]

    @target_proxy.setter
    def target_proxy(self, value):
        self._target_proxy = (value, True)

    @property
    def address(self):
        """
        The address that will be used to perform discovery on the cluster.

        :rtype: ``str``
        """
        return self._address[0]

    @address.setter
    def address(self, value):
        self._address = (value, True)

