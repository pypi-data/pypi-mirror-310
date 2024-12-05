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
#     /delphix-js-bookmark-checkout-count.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSBookmarkCheckoutCount(PersistentObject):
    """
    *(extends* :py:class:`v1_11_23.web.vo.PersistentObject` *)* The number of
    times a bookmark has been checked out. This means it was used as input to a
    RESTORE, CREATE_BRANCH, or RESET operation. The bookmark checkout count is
    kept separately on replicated templates.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSBookmarkCheckoutCount", True)
        self._bookmark = (self.__undef__, True)
        self._checkout_count = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._bookmark = (data.get("bookmark", obj.__undef__), dirty)
        if obj._bookmark[0] is not None and obj._bookmark[0] is not obj.__undef__:
            assert isinstance(obj._bookmark[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bookmark[0], type(obj._bookmark[0])))
            common.validate_format(obj._bookmark[0], "objectReference", None, None)
        obj._checkout_count = (data.get("checkoutCount", obj.__undef__), dirty)
        if obj._checkout_count[0] is not None and obj._checkout_count[0] is not obj.__undef__:
            assert isinstance(obj._checkout_count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._checkout_count[0], type(obj._checkout_count[0])))
            common.validate_format(obj._checkout_count[0], "None", None, None)
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
        if "checkout_count" == "type" or (self.checkout_count is not self.__undef__ and (not (dirty and not self._checkout_count[1]))):
            dct["checkoutCount"] = dictify(self.checkout_count)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._bookmark = (self._bookmark[0], True)
        self._checkout_count = (self._checkout_count[0], True)

    def is_dirty(self):
        return any([self._bookmark[1], self._checkout_count[1]])

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
        if not isinstance(other, JSBookmarkCheckoutCount):
            return False
        return super().__eq__(other) and \
               self.bookmark == other.bookmark and \
               self.checkout_count == other.checkout_count

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def bookmark(self):
        """
        The bookmark that this checkout count is associated with.

        :rtype: ``str``
        """
        return self._bookmark[0]

    @bookmark.setter
    def bookmark(self, value):
        self._bookmark = (value, True)

    @property
    def checkout_count(self):
        """
        The number of times the bookmark has been checked out. This means it
        was used as input to a RESTORE, CREATE_BRANCH, or RESET operation. This
        should not be replicated.

        :rtype: ``int``
        """
        return self._checkout_count[0]

    @checkout_count.setter
    def checkout_count(self, value):
        self._checkout_count = (value, True)

