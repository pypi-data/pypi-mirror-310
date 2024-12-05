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
#     /delphix-link-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_36 import factory
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class LinkParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TypedObject` *)* Represents the
    parameters of a link request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("LinkParameters", True)
        self._name = (self.__undef__, True)
        self._group = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._link_data = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "name" not in data:
            raise ValueError("Missing required property \"name\".")
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "objectName", None, 256)
        if "group" not in data:
            raise ValueError("Missing required property \"group\".")
        obj._group = (data.get("group", obj.__undef__), dirty)
        if obj._group[0] is not None and obj._group[0] is not obj.__undef__:
            assert isinstance(obj._group[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._group[0], type(obj._group[0])))
            common.validate_format(obj._group[0], "objectReference", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, 1024)
        if "linkData" not in data:
            raise ValueError("Missing required property \"linkData\".")
        if "linkData" in data and data["linkData"] is not None:
            obj._link_data = (factory.create_object(data["linkData"], "LinkData"), dirty)
            factory.validate_type(obj._link_data[0], "LinkData")
        else:
            obj._link_data = (obj.__undef__, dirty)
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
        if "group" == "type" or (self.group is not self.__undef__ and (not (dirty and not self._group[1]) or self.is_dirty_list(self.group, self._group) or belongs_to_parent)):
            dct["group"] = dictify(self.group)
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]) or self.is_dirty_list(self.description, self._description) or belongs_to_parent)):
            dct["description"] = dictify(self.description)
        if "link_data" == "type" or (self.link_data is not self.__undef__ and (not (dirty and not self._link_data[1]) or self.is_dirty_list(self.link_data, self._link_data) or belongs_to_parent)):
            dct["linkData"] = dictify(self.link_data, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._group = (self._group[0], True)
        self._description = (self._description[0], True)
        self._link_data = (self._link_data[0], True)

    def is_dirty(self):
        return any([self._name[1], self._group[1], self._description[1], self._link_data[1]])

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
        if not isinstance(other, LinkParameters):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.group == other.group and \
               self.description == other.description and \
               self.link_data == other.link_data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        DSource name.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def group(self):
        """
        A reference to the group containing this container.

        :rtype: ``str``
        """
        return self._group[0]

    @group.setter
    def group(self, value):
        self._group = (value, True)

    @property
    def description(self):
        """
        Optional user-provided description for the container.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def link_data(self):
        """
        Database specific data required for linking.

        :rtype: :py:class:`v1_11_36.web.vo.LinkData`
        """
        return self._link_data[0]

    @link_data.setter
    def link_data(self, value):
        self._link_data = (value, True)

