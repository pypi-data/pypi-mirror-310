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
#     /delphix-appdata-platform-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.BasePlatformParameters import BasePlatformParameters
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AppDataPlatformParameters(BasePlatformParameters):
    """
    *(extends* :py:class:`v1_11_34.web.vo.BasePlatformParameters` *)* AppData
    platform-specific parameters that are stored on a transformation.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AppDataPlatformParameters", True)
        self._payload = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "payload" in data and data["payload"] is not None:
            obj._payload = (data["payload"], dirty)
        else:
            obj._payload = (obj.__undef__, dirty)
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
        if "payload" == "type" or (self.payload is not self.__undef__ and (not (dirty and not self._payload[1]) or self.is_dirty_list(self.payload, self._payload) or belongs_to_parent)):
            dct["payload"] = dictify(self.payload, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._payload = (self._payload[0], True)

    def is_dirty(self):
        return any([self._payload[1]])

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
        if not isinstance(other, AppDataPlatformParameters):
            return False
        return super().__eq__(other) and \
               self.payload == other.payload

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def payload(self):
        """
        The JSON payload conforming to the DraftV4 schema based on the type of
        application data being manipulated.

        :rtype: :py:class:`v1_11_34.web.vo.Json`
        """
        return self._payload[0]

    @payload.setter
    def payload(self, value):
        self._payload = (value, True)

