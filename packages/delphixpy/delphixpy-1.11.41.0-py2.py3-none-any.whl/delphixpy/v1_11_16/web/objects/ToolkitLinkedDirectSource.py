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
#     /delphix-toolkit-linked-direct-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.ToolkitLinkedSource import ToolkitLinkedSource
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ToolkitLinkedDirectSource(ToolkitLinkedSource):
    """
    *(extends* :py:class:`v1_11_16.web.vo.ToolkitLinkedSource` *)* A linked
    source definition for Lua toolkits that perform linking using direct file
    sync.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ToolkitLinkedDirectSource", True)
        self._uses_grandfathered_app_data_properties = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._uses_grandfathered_app_data_properties = (data.get("usesGrandfatheredAppDataProperties", obj.__undef__), dirty)
        if obj._uses_grandfathered_app_data_properties[0] is not None and obj._uses_grandfathered_app_data_properties[0] is not obj.__undef__:
            assert isinstance(obj._uses_grandfathered_app_data_properties[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._uses_grandfathered_app_data_properties[0], type(obj._uses_grandfathered_app_data_properties[0])))
            common.validate_format(obj._uses_grandfathered_app_data_properties[0], "None", None, None)
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
        if "uses_grandfathered_app_data_properties" == "type" or (self.uses_grandfathered_app_data_properties is not self.__undef__ and (not (dirty and not self._uses_grandfathered_app_data_properties[1]) or self.is_dirty_list(self.uses_grandfathered_app_data_properties, self._uses_grandfathered_app_data_properties) or belongs_to_parent)):
            dct["usesGrandfatheredAppDataProperties"] = dictify(self.uses_grandfathered_app_data_properties)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._uses_grandfathered_app_data_properties = (self._uses_grandfathered_app_data_properties[0], True)

    def is_dirty(self):
        return any([self._uses_grandfathered_app_data_properties[1]])

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
        if not isinstance(other, ToolkitLinkedDirectSource):
            return False
        return super().__eq__(other) and \
               self.uses_grandfathered_app_data_properties == other.uses_grandfathered_app_data_properties

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def uses_grandfathered_app_data_properties(self):
        """
        True if this toolkit requires old-style AppData-defined properties.

        :rtype: ``bool``
        """
        return self._uses_grandfathered_app_data_properties[0]

    @uses_grandfathered_app_data_properties.setter
    def uses_grandfathered_app_data_properties(self, value):
        self._uses_grandfathered_app_data_properties = (value, True)

