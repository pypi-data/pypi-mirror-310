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
#     /delphix-theme.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_12.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_12 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Theme(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_12.web.vo.NamedUserObject` *)* Custom user
    themes.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Theme", True)
        self._name = (self.__undef__, True)
        self._values = (self.__undef__, True)
        self._active = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, None)
        if "values" in data and data["values"] is not None:
            obj._values = (data["values"], dirty)
        else:
            obj._values = (obj.__undef__, dirty)
        obj._active = (data.get("active", obj.__undef__), dirty)
        if obj._active[0] is not None and obj._active[0] is not obj.__undef__:
            assert isinstance(obj._active[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._active[0], type(obj._active[0])))
            common.validate_format(obj._active[0], "None", None, None)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "values" == "type" or (self.values is not self.__undef__ and (not (dirty and not self._values[1]) or self.is_dirty_list(self.values, self._values) or belongs_to_parent)):
            dct["values"] = dictify(self.values, prop_is_list_or_vo=True)
        if "active" == "type" or (self.active is not self.__undef__ and (not (dirty and not self._active[1]))):
            dct["active"] = dictify(self.active)
        if dirty and "active" in dct:
            del dct["active"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._values = (self._values[0], True)
        self._active = (self._active[0], True)

    def is_dirty(self):
        return any([self._name[1], self._values[1], self._active[1]])

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
        if not isinstance(other, Theme):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.values == other.values and \
               self.active == other.active

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        Theme name.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def values(self):
        """
        An object consisting UI styling rules.

        :rtype: :py:class:`v1_11_12.web.vo.SchemaDraftV4`
        """
        return self._values[0]

    @values.setter
    def values(self, value):
        self._values = (value, True)

    @property
    def active(self):
        """
        States whether is set as default by sysadmin.

        :rtype: ``bool``
        """
        return self._active[0]

