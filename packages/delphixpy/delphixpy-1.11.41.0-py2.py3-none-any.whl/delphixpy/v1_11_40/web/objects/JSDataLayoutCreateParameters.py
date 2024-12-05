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
#     /delphix-js-data-layout-create-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_40 import factory
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSDataLayoutCreateParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_40.web.vo.TypedObject` *)* The parameters used
    to create a data layout.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSDataLayoutCreateParameters", True)
        self._name = (self.__undef__, True)
        self._notes = (self.__undef__, True)
        self._data_sources = (self.__undef__, True)
        self._properties = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "name" not in data:
            raise ValueError("Missing required property \"name\".")
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, 256)
        obj._notes = (data.get("notes", obj.__undef__), dirty)
        if obj._notes[0] is not None and obj._notes[0] is not obj.__undef__:
            assert isinstance(obj._notes[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._notes[0], type(obj._notes[0])))
            common.validate_format(obj._notes[0], "None", None, 4096)
        if "dataSources" not in data:
            raise ValueError("Missing required property \"dataSources\".")
        obj._data_sources = []
        for item in data.get("dataSources") or []:
            obj._data_sources.append(factory.create_object(item))
            factory.validate_type(obj._data_sources[-1], "JSDataSourceCreateParameters")
        obj._data_sources = (obj._data_sources, dirty)
        obj._properties = (data.get("properties", obj.__undef__), dirty)
        if obj._properties[0] is not None and obj._properties[0] is not obj.__undef__:
            assert isinstance(obj._properties[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._properties[0], type(obj._properties[0])))
            common.validate_format(obj._properties[0], "None", None, None)
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
        if "notes" == "type" or (self.notes is not self.__undef__ and (not (dirty and not self._notes[1]) or self.is_dirty_list(self.notes, self._notes) or belongs_to_parent)):
            dct["notes"] = dictify(self.notes)
        if "data_sources" == "type" or (self.data_sources is not self.__undef__ and (not (dirty and not self._data_sources[1]) or self.is_dirty_list(self.data_sources, self._data_sources) or belongs_to_parent)):
            dct["dataSources"] = dictify(self.data_sources, prop_is_list_or_vo=True)
        if "properties" == "type" or (self.properties is not self.__undef__ and (not (dirty and not self._properties[1]) or self.is_dirty_list(self.properties, self._properties) or belongs_to_parent)):
            dct["properties"] = dictify(self.properties, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._notes = (self._notes[0], True)
        self._data_sources = (self._data_sources[0], True)
        self._properties = (self._properties[0], True)

    def is_dirty(self):
        return any([self._name[1], self._notes[1], self._data_sources[1], self._properties[1]])

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
        if not isinstance(other, JSDataLayoutCreateParameters):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.notes == other.notes and \
               self.data_sources == other.data_sources and \
               self.properties == other.properties

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        The name of the data layout.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def notes(self):
        """
        A description of this data layout to define what it is used for.

        :rtype: ``str``
        """
        return self._notes[0]

    @notes.setter
    def notes(self, value):
        self._notes = (value, True)

    @property
    def data_sources(self):
        """
        The set of data sources that belong to this data layout.

        :rtype: ``list`` of
            :py:class:`v1_11_40.web.vo.JSDataSourceCreateParameters`
        """
        return self._data_sources[0]

    @data_sources.setter
    def data_sources(self, value):
        self._data_sources = (value, True)

    @property
    def properties(self):
        """
        Key/value pairs used to specify attributes for this data layout.

        :rtype: ``dict``
        """
        return self._properties[0]

    @properties.setter
    def properties(self, value):
        self._properties = (value, True)

