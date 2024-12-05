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
#     /delphix-host-privilege-elevation-settings.json
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

class HostPrivilegeElevationSettings(TypedObject):
    """
    *(extends* :py:class:`v1_11_21.web.vo.TypedObject` *)* Settings for
    elevating user privileges on a host.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HostPrivilegeElevationSettings", True)
        self._default_profile = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._default_profile = (data.get("defaultProfile", obj.__undef__), dirty)
        if obj._default_profile[0] is not None and obj._default_profile[0] is not obj.__undef__:
            assert isinstance(obj._default_profile[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._default_profile[0], type(obj._default_profile[0])))
            common.validate_format(obj._default_profile[0], "objectReference", None, None)
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
        if "default_profile" == "type" or (self.default_profile is not self.__undef__ and (not (dirty and not self._default_profile[1]) or self.is_dirty_list(self.default_profile, self._default_profile) or belongs_to_parent)):
            dct["defaultProfile"] = dictify(self.default_profile)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._default_profile = (self._default_profile[0], True)

    def is_dirty(self):
        return any([self._default_profile[1]])

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
        if not isinstance(other, HostPrivilegeElevationSettings):
            return False
        return super().__eq__(other) and \
               self.default_profile == other.default_profile

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def default_profile(self):
        """
        The default privilege elevation profile for new environments.

        :rtype: ``str``
        """
        return self._default_profile[0]

    @default_profile.setter
    def default_profile(self, value):
        self._default_profile = (value, True)

