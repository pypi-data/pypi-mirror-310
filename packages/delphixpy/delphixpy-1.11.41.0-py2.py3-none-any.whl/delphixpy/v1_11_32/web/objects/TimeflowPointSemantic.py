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
#     /delphix-timeflow-point-semantic.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.TimeflowPointParameters import TimeflowPointParameters
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TimeflowPointSemantic(TimeflowPointParameters):
    """
    *(extends* :py:class:`v1_11_32.web.vo.TimeflowPointParameters` *)* TimeFlow
    point based on a semantic reference.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TimeflowPointSemantic", True)
        self._location = (self.__undef__, True)
        self._container = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._location = (data.get("location", obj.__undef__), dirty)
        if obj._location[0] is not None and obj._location[0] is not obj.__undef__:
            assert isinstance(obj._location[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._location[0], type(obj._location[0])))
            assert obj._location[0] in ['LATEST_POINT', 'LATEST_SNAPSHOT', 'OLDEST_SNAPSHOT'], "Expected enum ['LATEST_POINT', 'LATEST_SNAPSHOT', 'OLDEST_SNAPSHOT'] but got %s" % obj._location[0]
            common.validate_format(obj._location[0], "None", None, None)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "objectReference", None, None)
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
        if "location" == "type" or (self.location is not self.__undef__ and (not (dirty and not self._location[1]) or self.is_dirty_list(self.location, self._location) or belongs_to_parent)):
            dct["location"] = dictify(self.location)
        elif belongs_to_parent and self.location is self.__undef__:
            dct["location"] = "LATEST_POINT"
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]) or self.is_dirty_list(self.container, self._container) or belongs_to_parent)):
            dct["container"] = dictify(self.container)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._location = (self._location[0], True)
        self._container = (self._container[0], True)

    def is_dirty(self):
        return any([self._location[1], self._container[1]])

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
        if not isinstance(other, TimeflowPointSemantic):
            return False
        return super().__eq__(other) and \
               self.location == other.location and \
               self.container == other.container

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def location(self):
        """
        *(default value: LATEST_POINT)* A semantic description of a TimeFlow
        location. *(permitted values: LATEST_POINT, LATEST_SNAPSHOT,
        OLDEST_SNAPSHOT)*

        :rtype: ``str``
        """
        return self._location[0]

    @location.setter
    def location(self, value):
        self._location = (value, True)

    @property
    def container(self):
        """
        Reference to the container.

        :rtype: ``str``
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

