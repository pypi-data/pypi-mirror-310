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
#     /delphix-capacity-base-consumer-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_5.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_5 import factory
from delphixpy.v1_11_5 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class BaseConsumerCapacityData(TypedObject):
    """
    *(extends* :py:class:`v1_11_5.web.vo.TypedObject` *)* Data about a
    particular capacity consumer.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("BaseConsumerCapacityData", True)
        self._container = (self.__undef__, True)
        self._group = (self.__undef__, True)
        self._timestamp = (self.__undef__, True)
        self._breakdown = (self.__undef__, True)
        self._name = (self.__undef__, True)
        self._parent = (self.__undef__, True)
        self._group_name = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "objectReference", None, None)
        obj._group = (data.get("group", obj.__undef__), dirty)
        if obj._group[0] is not None and obj._group[0] is not obj.__undef__:
            assert isinstance(obj._group[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._group[0], type(obj._group[0])))
            common.validate_format(obj._group[0], "objectReference", None, None)
        obj._timestamp = (data.get("timestamp", obj.__undef__), dirty)
        if obj._timestamp[0] is not None and obj._timestamp[0] is not obj.__undef__:
            assert isinstance(obj._timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._timestamp[0], type(obj._timestamp[0])))
            common.validate_format(obj._timestamp[0], "date", None, None)
        if "breakdown" in data and data["breakdown"] is not None:
            obj._breakdown = (factory.create_object(data["breakdown"], "CapacityBreakdown"), dirty)
            factory.validate_type(obj._breakdown[0], "CapacityBreakdown")
        else:
            obj._breakdown = (obj.__undef__, dirty)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, None)
        obj._parent = (data.get("parent", obj.__undef__), dirty)
        if obj._parent[0] is not None and obj._parent[0] is not obj.__undef__:
            assert isinstance(obj._parent[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent[0], type(obj._parent[0])))
            common.validate_format(obj._parent[0], "objectReference", None, None)
        obj._group_name = (data.get("groupName", obj.__undef__), dirty)
        if obj._group_name[0] is not None and obj._group_name[0] is not obj.__undef__:
            assert isinstance(obj._group_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._group_name[0], type(obj._group_name[0])))
            common.validate_format(obj._group_name[0], "None", None, None)
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
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]))):
            dct["container"] = dictify(self.container)
        if "group" == "type" or (self.group is not self.__undef__ and (not (dirty and not self._group[1]))):
            dct["group"] = dictify(self.group)
        if "timestamp" == "type" or (self.timestamp is not self.__undef__ and (not (dirty and not self._timestamp[1]))):
            dct["timestamp"] = dictify(self.timestamp)
        if "breakdown" == "type" or (self.breakdown is not self.__undef__ and (not (dirty and not self._breakdown[1]))):
            dct["breakdown"] = dictify(self.breakdown)
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]))):
            dct["name"] = dictify(self.name)
        if "parent" == "type" or (self.parent is not self.__undef__ and (not (dirty and not self._parent[1]))):
            dct["parent"] = dictify(self.parent)
        if "group_name" == "type" or (self.group_name is not self.__undef__ and (not (dirty and not self._group_name[1]))):
            dct["groupName"] = dictify(self.group_name)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._container = (self._container[0], True)
        self._group = (self._group[0], True)
        self._timestamp = (self._timestamp[0], True)
        self._breakdown = (self._breakdown[0], True)
        self._name = (self._name[0], True)
        self._parent = (self._parent[0], True)
        self._group_name = (self._group_name[0], True)

    def is_dirty(self):
        return any([self._container[1], self._group[1], self._timestamp[1], self._breakdown[1], self._name[1], self._parent[1], self._group_name[1]])

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
        if not isinstance(other, BaseConsumerCapacityData):
            return False
        return super().__eq__(other) and \
               self.container == other.container and \
               self.group == other.group and \
               self.timestamp == other.timestamp and \
               self.breakdown == other.breakdown and \
               self.name == other.name and \
               self.parent == other.parent and \
               self.group_name == other.group_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

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

    @property
    def group(self):
        """
        Reference to this container's group.

        :rtype: ``str``
        """
        return self._group[0]

    @group.setter
    def group(self, value):
        self._group = (value, True)

    @property
    def timestamp(self):
        """
        Time at which this information was sampled.

        :rtype: ``str``
        """
        return self._timestamp[0]

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = (value, True)

    @property
    def breakdown(self):
        """
        Statistics for this consumer.

        :rtype: :py:class:`v1_11_5.web.vo.CapacityBreakdown`
        """
        return self._breakdown[0]

    @breakdown.setter
    def breakdown(self, value):
        self._breakdown = (value, True)

    @property
    def name(self):
        """
        Name of the container.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def parent(self):
        """
        Container from which this TimeFlow was provisioned.

        :rtype: ``str``
        """
        return self._parent[0]

    @parent.setter
    def parent(self, value):
        self._parent = (value, True)

    @property
    def group_name(self):
        """
        Name of this container's group.

        :rtype: ``str``
        """
        return self._group_name[0]

    @group_name.setter
    def group_name(self, value):
        self._group_name = (value, True)

