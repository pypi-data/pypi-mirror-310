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
#     /delphix-js-bookmark-create-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_23 import factory
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSBookmarkCreateParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_23.web.vo.TypedObject` *)* The parameters used
    to create a Self-Service bookmark.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSBookmarkCreateParameters", True)
        self._bookmark = (self.__undef__, True)
        self._timeline_point_parameters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "bookmark" not in data:
            raise ValueError("Missing required property \"bookmark\".")
        if "bookmark" in data and data["bookmark"] is not None:
            obj._bookmark = (factory.create_object(data["bookmark"], "JSBookmark"), dirty)
            factory.validate_type(obj._bookmark[0], "JSBookmark")
        else:
            obj._bookmark = (obj.__undef__, dirty)
        if "timelinePointParameters" not in data:
            raise ValueError("Missing required property \"timelinePointParameters\".")
        if "timelinePointParameters" in data and data["timelinePointParameters"] is not None:
            obj._timeline_point_parameters = (factory.create_object(data["timelinePointParameters"], "JSTimelinePointTimeParameters"), dirty)
            factory.validate_type(obj._timeline_point_parameters[0], "JSTimelinePointTimeParameters")
        else:
            obj._timeline_point_parameters = (obj.__undef__, dirty)
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
        if "bookmark" == "type" or (self.bookmark is not self.__undef__ and (not (dirty and not self._bookmark[1]) or self.is_dirty_list(self.bookmark, self._bookmark) or belongs_to_parent)):
            dct["bookmark"] = dictify(self.bookmark, prop_is_list_or_vo=True)
        if "timeline_point_parameters" == "type" or (self.timeline_point_parameters is not self.__undef__ and (not (dirty and not self._timeline_point_parameters[1]) or self.is_dirty_list(self.timeline_point_parameters, self._timeline_point_parameters) or belongs_to_parent)):
            dct["timelinePointParameters"] = dictify(self.timeline_point_parameters, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._bookmark = (self._bookmark[0], True)
        self._timeline_point_parameters = (self._timeline_point_parameters[0], True)

    def is_dirty(self):
        return any([self._bookmark[1], self._timeline_point_parameters[1]])

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
        if not isinstance(other, JSBookmarkCreateParameters):
            return False
        return super().__eq__(other) and \
               self.bookmark == other.bookmark and \
               self.timeline_point_parameters == other.timeline_point_parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def bookmark(self):
        """
        The Self-Service bookmark object.

        :rtype: :py:class:`v1_11_23.web.vo.JSBookmark`
        """
        return self._bookmark[0]

    @bookmark.setter
    def bookmark(self, value):
        self._bookmark = (value, True)

    @property
    def timeline_point_parameters(self):
        """
        The Self-Service data timeline point at which the bookmark will be
        created.

        :rtype: :py:class:`v1_11_23.web.vo.JSTimelinePointTimeParameters`
        """
        return self._timeline_point_parameters[0]

    @timeline_point_parameters.setter
    def timeline_point_parameters(self, value):
        self._timeline_point_parameters = (value, True)

