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
#     /delphix-fluentd-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_30.web.objects.UserObject import UserObject
from delphixpy.v1_11_30 import factory
from delphixpy.v1_11_30 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class FluentdConfig(UserObject):
    """
    *(extends* :py:class:`v1_11_30.web.vo.UserObject` *)* Fluentd configuration
    information.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("FluentdConfig", True)
        self._enabled = (self.__undef__, True)
        self._plugin = (self.__undef__, True)
        self._attributes = (self.__undef__, True)
        self._performance_metrics_resolution = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._plugin = (data.get("plugin", obj.__undef__), dirty)
        if obj._plugin[0] is not None and obj._plugin[0] is not obj.__undef__:
            assert isinstance(obj._plugin[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._plugin[0], type(obj._plugin[0])))
            common.validate_format(obj._plugin[0], "None", None, None)
        obj._attributes = []
        for item in data.get("attributes") or []:
            obj._attributes.append(factory.create_object(item))
            factory.validate_type(obj._attributes[-1], "FluentdAttribute")
        obj._attributes = (obj._attributes, dirty)
        obj._performance_metrics_resolution = (data.get("performanceMetricsResolution", obj.__undef__), dirty)
        if obj._performance_metrics_resolution[0] is not None and obj._performance_metrics_resolution[0] is not obj.__undef__:
            assert isinstance(obj._performance_metrics_resolution[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._performance_metrics_resolution[0], type(obj._performance_metrics_resolution[0])))
            assert obj._performance_metrics_resolution[0] in ['SECOND', 'MINUTE'], "Expected enum ['SECOND', 'MINUTE'] but got %s" % obj._performance_metrics_resolution[0]
            common.validate_format(obj._performance_metrics_resolution[0], "None", None, None)
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
        if "plugin" == "type" or (self.plugin is not self.__undef__ and (not (dirty and not self._plugin[1]) or self.is_dirty_list(self.plugin, self._plugin) or belongs_to_parent)):
            dct["plugin"] = dictify(self.plugin)
        if "attributes" == "type" or (self.attributes is not self.__undef__ and (not (dirty and not self._attributes[1]) or self.is_dirty_list(self.attributes, self._attributes) or belongs_to_parent)):
            dct["attributes"] = dictify(self.attributes, prop_is_list_or_vo=True)
        if "performance_metrics_resolution" == "type" or (self.performance_metrics_resolution is not self.__undef__ and (not (dirty and not self._performance_metrics_resolution[1]) or self.is_dirty_list(self.performance_metrics_resolution, self._performance_metrics_resolution) or belongs_to_parent)):
            dct["performanceMetricsResolution"] = dictify(self.performance_metrics_resolution)
        elif belongs_to_parent and self.performance_metrics_resolution is self.__undef__:
            dct["performanceMetricsResolution"] = "MINUTE"
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._plugin = (self._plugin[0], True)
        self._attributes = (self._attributes[0], True)
        self._performance_metrics_resolution = (self._performance_metrics_resolution[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._plugin[1], self._attributes[1], self._performance_metrics_resolution[1]])

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
        if not isinstance(other, FluentdConfig):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.plugin == other.plugin and \
               self.attributes == other.attributes and \
               self.performance_metrics_resolution == other.performance_metrics_resolution

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        Whether we should send Delphix Insight data using this configuration.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def plugin(self):
        """
        Name of the fluentd plugin.

        :rtype: ``str``
        """
        return self._plugin[0]

    @plugin.setter
    def plugin(self, value):
        self._plugin = (value, True)

    @property
    def attributes(self):
        """
        List of attributes to configure fluentd.

        :rtype: ``list`` of :py:class:`v1_11_30.web.vo.FluentdAttribute`
        """
        return self._attributes[0]

    @attributes.setter
    def attributes(self, value):
        self._attributes = (value, True)

    @property
    def performance_metrics_resolution(self):
        """
        *(default value: MINUTE)* Performance metrics resolution. *(permitted
        values: SECOND, MINUTE)*

        :rtype: ``str``
        """
        return self._performance_metrics_resolution[0]

    @performance_metrics_resolution.setter
    def performance_metrics_resolution(self, value):
        self._performance_metrics_resolution = (value, True)

