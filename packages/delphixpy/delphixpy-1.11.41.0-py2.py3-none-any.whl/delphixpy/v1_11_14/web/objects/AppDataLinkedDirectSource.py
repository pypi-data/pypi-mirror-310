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
#     /delphix-appdata-linked-direct-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.AppDataLinkedSource import AppDataLinkedSource
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AppDataLinkedDirectSource(AppDataLinkedSource):
    """
    *(extends* :py:class:`v1_11_14.web.vo.AppDataLinkedSource` *)* An AppData
    linked source directly replicated into the Delphix Engine.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AppDataLinkedDirectSource", True)
        self._excludes = (self.__undef__, True)
        self._follow_symlinks = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._excludes = []
        for item in data.get("excludes") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._excludes.append(item)
        obj._excludes = (obj._excludes, dirty)
        obj._follow_symlinks = []
        for item in data.get("followSymlinks") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._follow_symlinks.append(item)
        obj._follow_symlinks = (obj._follow_symlinks, dirty)
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
        if "excludes" == "type" or (self.excludes is not self.__undef__ and (not (dirty and not self._excludes[1]) or self.is_dirty_list(self.excludes, self._excludes) or belongs_to_parent)):
            dct["excludes"] = dictify(self.excludes, prop_is_list_or_vo=True)
        if "follow_symlinks" == "type" or (self.follow_symlinks is not self.__undef__ and (not (dirty and not self._follow_symlinks[1]) or self.is_dirty_list(self.follow_symlinks, self._follow_symlinks) or belongs_to_parent)):
            dct["followSymlinks"] = dictify(self.follow_symlinks, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._excludes = (self._excludes[0], True)
        self._follow_symlinks = (self._follow_symlinks[0], True)

    def is_dirty(self):
        return any([self._excludes[1], self._follow_symlinks[1]])

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
        if not isinstance(other, AppDataLinkedDirectSource):
            return False
        return super().__eq__(other) and \
               self.excludes == other.excludes and \
               self.follow_symlinks == other.follow_symlinks

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def excludes(self):
        """
        List of subdirectories in the source to exclude when syncing data.
        These paths are relative to the root of the source directory.

        :rtype: ``list`` of ``str``
        """
        return self._excludes[0]

    @excludes.setter
    def excludes(self, value):
        self._excludes = (value, True)

    @property
    def follow_symlinks(self):
        """
        List of symlinks in the source to follow when syncing data. These paths
        are relative to the root of the source directory. All other symlinks
        are preserved.

        :rtype: ``list`` of ``str``
        """
        return self._follow_symlinks[0]

    @follow_symlinks.setter
    def follow_symlinks(self, value):
        self._follow_symlinks = (value, True)

