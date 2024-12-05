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
#     /delphix-user-path-storage.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UserPathStorage(PersistentObject):
    """
    *(extends* :py:class:`v1_11_27.web.vo.PersistentObject` *)* Store
    configuration paths.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UserPathStorage", True)
        self._path = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._pathtype = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._path = (data.get("path", obj.__undef__), dirty)
        if obj._path[0] is not None and obj._path[0] is not obj.__undef__:
            assert isinstance(obj._path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._path[0], type(obj._path[0])))
            common.validate_format(obj._path[0], "None", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        obj._pathtype = (data.get("pathtype", obj.__undef__), dirty)
        if obj._pathtype[0] is not None and obj._pathtype[0] is not obj.__undef__:
            assert isinstance(obj._pathtype[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pathtype[0], type(obj._pathtype[0])))
            assert obj._pathtype[0] in ['UPGRADE_STAGING_LOC'], "Expected enum ['UPGRADE_STAGING_LOC'] but got %s" % obj._pathtype[0]
            common.validate_format(obj._pathtype[0], "None", None, None)
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
        if "path" == "type" or (self.path is not self.__undef__ and (not (dirty and not self._path[1]) or self.is_dirty_list(self.path, self._path) or belongs_to_parent)):
            dct["path"] = dictify(self.path)
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]) or self.is_dirty_list(self.description, self._description) or belongs_to_parent)):
            dct["description"] = dictify(self.description)
        if "pathtype" == "type" or (self.pathtype is not self.__undef__ and (not (dirty and not self._pathtype[1]) or self.is_dirty_list(self.pathtype, self._pathtype) or belongs_to_parent)):
            dct["pathtype"] = dictify(self.pathtype)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._path = (self._path[0], True)
        self._description = (self._description[0], True)
        self._pathtype = (self._pathtype[0], True)

    def is_dirty(self):
        return any([self._path[1], self._description[1], self._pathtype[1]])

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
        if not isinstance(other, UserPathStorage):
            return False
        return super().__eq__(other) and \
               self.path == other.path and \
               self.description == other.description and \
               self.pathtype == other.pathtype

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def path(self):
        """
        String field storing the path.

        :rtype: ``str``
        """
        return self._path[0]

    @path.setter
    def path(self, value):
        self._path = (value, True)

    @property
    def description(self):
        """
        Optional textual description.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def pathtype(self):
        """
        Type of path stored. *(permitted values: UPGRADE_STAGING_LOC)*

        :rtype: ``str``
        """
        return self._pathtype[0]

    @pathtype.setter
    def pathtype(self, value):
        self._pathtype = (value, True)

