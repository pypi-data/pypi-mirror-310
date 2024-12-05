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
#     /delphix-cloud-enable-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_24.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_24 import factory
from delphixpy.v1_11_24 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CloudEnableParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_24.web.vo.TypedObject` *)* Parameters to the
    Cloud Enable operation.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CloudEnableParameters", True)
        self._proxy_mode = (self.__undef__, True)
        self._proxy_configuration = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._proxy_mode = (data.get("proxyMode", obj.__undef__), dirty)
        if obj._proxy_mode[0] is not None and obj._proxy_mode[0] is not obj.__undef__:
            assert isinstance(obj._proxy_mode[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._proxy_mode[0], type(obj._proxy_mode[0])))
            assert obj._proxy_mode[0] in ['SYSTEM_WIDE_SETTING', 'CLOUD_SPECIFIC_SETTING', 'NO_PROXY'], "Expected enum ['SYSTEM_WIDE_SETTING', 'CLOUD_SPECIFIC_SETTING', 'NO_PROXY'] but got %s" % obj._proxy_mode[0]
            common.validate_format(obj._proxy_mode[0], "None", None, None)
        if "proxyConfiguration" in data and data["proxyConfiguration"] is not None:
            obj._proxy_configuration = (factory.create_object(data["proxyConfiguration"], "ProxyConfiguration"), dirty)
            factory.validate_type(obj._proxy_configuration[0], "ProxyConfiguration")
        else:
            obj._proxy_configuration = (obj.__undef__, dirty)
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
        if "proxy_mode" == "type" or (self.proxy_mode is not self.__undef__ and (not (dirty and not self._proxy_mode[1]))):
            dct["proxyMode"] = dictify(self.proxy_mode)
        if "proxy_configuration" == "type" or (self.proxy_configuration is not self.__undef__ and (not (dirty and not self._proxy_configuration[1]))):
            dct["proxyConfiguration"] = dictify(self.proxy_configuration)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._proxy_mode = (self._proxy_mode[0], True)
        self._proxy_configuration = (self._proxy_configuration[0], True)

    def is_dirty(self):
        return any([self._proxy_mode[1], self._proxy_configuration[1]])

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
        if not isinstance(other, CloudEnableParameters):
            return False
        return super().__eq__(other) and \
               self.proxy_mode == other.proxy_mode and \
               self.proxy_configuration == other.proxy_configuration

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def proxy_mode(self):
        """
        Whether an HTTP proxy must be used to connect to Central Management.
        *(permitted values: SYSTEM_WIDE_SETTING, CLOUD_SPECIFIC_SETTING,
        NO_PROXY)*

        :rtype: ``str``
        """
        return self._proxy_mode[0]

    @proxy_mode.setter
    def proxy_mode(self, value):
        self._proxy_mode = (value, True)

    @property
    def proxy_configuration(self):
        """
        Proxy configuration for communication with Delphix Central Management.
        This property is ignored unless the 'proxyMode' property is set to
        CLOUD_SPECIFIC_SETTING.

        :rtype: :py:class:`v1_11_24.web.vo.ProxyConfiguration`
        """
        return self._proxy_configuration[0]

    @proxy_configuration.setter
    def proxy_configuration(self, value):
        self._proxy_configuration = (value, True)

