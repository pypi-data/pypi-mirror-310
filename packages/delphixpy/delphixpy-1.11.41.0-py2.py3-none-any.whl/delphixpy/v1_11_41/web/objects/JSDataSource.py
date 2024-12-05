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
#     /delphix-js-data-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_41.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_41 import factory
from delphixpy.v1_11_41 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSDataSource(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_41.web.vo.NamedUserObject` *)* The data source
    used for Self-Service data layouts.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSDataSource", True)
        self._description = (self.__undef__, True)
        self._properties = (self.__undef__, True)
        self._data_layout = (self.__undef__, True)
        self._container = (self.__undef__, True)
        self._masked = (self.__undef__, True)
        self._enabled = (self.__undef__, True)
        self._runtime = (self.__undef__, True)
        self._priority = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, 4096)
        obj._properties = (data.get("properties", obj.__undef__), dirty)
        if obj._properties[0] is not None and obj._properties[0] is not obj.__undef__:
            assert isinstance(obj._properties[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._properties[0], type(obj._properties[0])))
            common.validate_format(obj._properties[0], "None", None, None)
        obj._data_layout = (data.get("dataLayout", obj.__undef__), dirty)
        if obj._data_layout[0] is not None and obj._data_layout[0] is not obj.__undef__:
            assert isinstance(obj._data_layout[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._data_layout[0], type(obj._data_layout[0])))
            common.validate_format(obj._data_layout[0], "objectReference", None, None)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "objectReference", None, None)
        obj._masked = (data.get("masked", obj.__undef__), dirty)
        if obj._masked[0] is not None and obj._masked[0] is not obj.__undef__:
            assert isinstance(obj._masked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._masked[0], type(obj._masked[0])))
            common.validate_format(obj._masked[0], "None", None, None)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "SourceConnectionInfo"), dirty)
            factory.validate_type(obj._runtime[0], "SourceConnectionInfo")
        else:
            obj._runtime = (obj.__undef__, dirty)
        obj._priority = (data.get("priority", obj.__undef__), dirty)
        if obj._priority[0] is not None and obj._priority[0] is not obj.__undef__:
            assert isinstance(obj._priority[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._priority[0], type(obj._priority[0])))
            common.validate_format(obj._priority[0], "None", None, None)
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
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]) or self.is_dirty_list(self.description, self._description) or belongs_to_parent)):
            dct["description"] = dictify(self.description)
        if "properties" == "type" or (self.properties is not self.__undef__ and (not (dirty and not self._properties[1]) or self.is_dirty_list(self.properties, self._properties) or belongs_to_parent)):
            dct["properties"] = dictify(self.properties, prop_is_list_or_vo=True)
        if "data_layout" == "type" or (self.data_layout is not self.__undef__ and (not (dirty and not self._data_layout[1]))):
            dct["dataLayout"] = dictify(self.data_layout)
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]))):
            dct["container"] = dictify(self.container)
        if "masked" == "type" or (self.masked is not self.__undef__ and (not (dirty and not self._masked[1]))):
            dct["masked"] = dictify(self.masked)
        if "enabled" == "type" or (self.enabled is not self.__undef__ and (not (dirty and not self._enabled[1]))):
            dct["enabled"] = dictify(self.enabled)
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        if "priority" == "type" or (self.priority is not self.__undef__ and (not (dirty and not self._priority[1]) or self.is_dirty_list(self.priority, self._priority) or belongs_to_parent)):
            dct["priority"] = dictify(self.priority)
        elif belongs_to_parent and self.priority is self.__undef__:
            dct["priority"] = 1
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._description = (self._description[0], True)
        self._properties = (self._properties[0], True)
        self._data_layout = (self._data_layout[0], True)
        self._container = (self._container[0], True)
        self._masked = (self._masked[0], True)
        self._enabled = (self._enabled[0], True)
        self._runtime = (self._runtime[0], True)
        self._priority = (self._priority[0], True)

    def is_dirty(self):
        return any([self._description[1], self._properties[1], self._data_layout[1], self._container[1], self._masked[1], self._enabled[1], self._runtime[1], self._priority[1]])

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
        if not isinstance(other, JSDataSource):
            return False
        return super().__eq__(other) and \
               self.description == other.description and \
               self.properties == other.properties and \
               self.data_layout == other.data_layout and \
               self.container == other.container and \
               self.masked == other.masked and \
               self.enabled == other.enabled and \
               self.runtime == other.runtime and \
               self.priority == other.priority

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def description(self):
        """
        A description of this data source.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def properties(self):
        """
        Key/value pairs used to specify attributes for this data source.

        :rtype: ``dict``
        """
        return self._properties[0]

    @properties.setter
    def properties(self, value):
        self._properties = (value, True)

    @property
    def data_layout(self):
        """
        A reference to the Self-Service data layout to which this source
        belongs.

        :rtype: ``str``
        """
        return self._data_layout[0]

    @data_layout.setter
    def data_layout(self, value):
        self._data_layout = (value, True)

    @property
    def container(self):
        """
        A reference to the underlying container.

        :rtype: ``str``
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def masked(self):
        """
        Flag indicating whether the source is masked.

        :rtype: ``bool``
        """
        return self._masked[0]

    @masked.setter
    def masked(self, value):
        self._masked = (value, True)

    @property
    def enabled(self):
        """
        Flag indicating whether the source is enabled.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def runtime(self):
        """
        Runtime properties of this data source.

        :rtype: :py:class:`v1_11_41.web.vo.SourceConnectionInfo`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

    @property
    def priority(self):
        """
        *(default value: 1)* Dictates order of operations on data sources.
        Operations can be performed in parallel for all sources or
        sequentially. Below are possible valid and invalid orderings given an
        example data template with 3 sources (A, B, and C).<br>Valid:<br>A B
        C<br>1 1 1 (parallel)<br>1 2 3 (sequential)<br>Invalid:<br>A B C<br>2 2
        2<br>0 1 2<br>2 3 4<br>1 2 2<br>In the sequential case the data source
        with priority 1 is the first to be started and the last to be stopped.
        This value is set on creation of the template's data sources and copied
        to the data container's data sources.

        :rtype: ``int``
        """
        return self._priority[0]

    @priority.setter
    def priority(self, value):
        self._priority = (value, True)

