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
#     /delphix-js-bookmark-data-parent.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.JSDataParent import JSDataParent
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSBookmarkDataParent(JSDataParent):
    """
    *(extends* :py:class:`v1_11_18.web.vo.JSDataParent` *)* The bookmark data
    parent of a RESTORE or CREATE_BRANCH operation.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSBookmarkDataParent", True)
        self._bookmark = (self.__undef__, True)
        self._bookmark_name = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._bookmark = (data.get("bookmark", obj.__undef__), dirty)
        if obj._bookmark[0] is not None and obj._bookmark[0] is not obj.__undef__:
            assert isinstance(obj._bookmark[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bookmark[0], type(obj._bookmark[0])))
            common.validate_format(obj._bookmark[0], "objectReference", None, None)
        obj._bookmark_name = (data.get("bookmarkName", obj.__undef__), dirty)
        if obj._bookmark_name[0] is not None and obj._bookmark_name[0] is not obj.__undef__:
            assert isinstance(obj._bookmark_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bookmark_name[0], type(obj._bookmark_name[0])))
            common.validate_format(obj._bookmark_name[0], "None", None, 256)
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
        if "bookmark" == "type" or (self.bookmark is not self.__undef__ and (not (dirty and not self._bookmark[1]))):
            dct["bookmark"] = dictify(self.bookmark)
        if "bookmark_name" == "type" or (self.bookmark_name is not self.__undef__ and (not (dirty and not self._bookmark_name[1]))):
            dct["bookmarkName"] = dictify(self.bookmark_name)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._bookmark = (self._bookmark[0], True)
        self._bookmark_name = (self._bookmark_name[0], True)

    def is_dirty(self):
        return any([self._bookmark[1], self._bookmark_name[1]])

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
        if not isinstance(other, JSBookmarkDataParent):
            return False
        return super().__eq__(other) and \
               self.bookmark == other.bookmark and \
               self.bookmark_name == other.bookmark_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def bookmark(self):
        """
        The bookmark that this operation's data came from. This will be null if
        the bookmark has been deleted.

        :rtype: ``str``
        """
        return self._bookmark[0]

    @bookmark.setter
    def bookmark(self, value):
        self._bookmark = (value, True)

    @property
    def bookmark_name(self):
        """
        This will always contain the name of the bookmark, even if it has been
        deleted.

        :rtype: ``str``
        """
        return self._bookmark_name[0]

    @bookmark_name.setter
    def bookmark_name(self, value):
        self._bookmark_name = (value, True)

