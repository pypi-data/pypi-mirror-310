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
#     /delphix-js-source-data-timestamp.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_3.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_3 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSSourceDataTimestamp(TypedObject):
    """
    *(extends* :py:class:`v1_11_3.web.vo.TypedObject` *)* The association
    between a Self-Service data source and a point in time that's
    provisionable.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSSourceDataTimestamp", True)
        self._source = (self.__undef__, True)
        self._name = (self.__undef__, True)
        self._priority = (self.__undef__, True)
        self._timestamp = (self.__undef__, True)
        self._branch = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._source = (data.get("source", obj.__undef__), dirty)
        if obj._source[0] is not None and obj._source[0] is not obj.__undef__:
            assert isinstance(obj._source[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source[0], type(obj._source[0])))
            common.validate_format(obj._source[0], "objectReference", None, None)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, None)
        obj._priority = (data.get("priority", obj.__undef__), dirty)
        if obj._priority[0] is not None and obj._priority[0] is not obj.__undef__:
            assert isinstance(obj._priority[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._priority[0], type(obj._priority[0])))
            common.validate_format(obj._priority[0], "None", None, None)
        obj._timestamp = (data.get("timestamp", obj.__undef__), dirty)
        if obj._timestamp[0] is not None and obj._timestamp[0] is not obj.__undef__:
            assert isinstance(obj._timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._timestamp[0], type(obj._timestamp[0])))
            common.validate_format(obj._timestamp[0], "date", None, None)
        obj._branch = (data.get("branch", obj.__undef__), dirty)
        if obj._branch[0] is not None and obj._branch[0] is not obj.__undef__:
            assert isinstance(obj._branch[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._branch[0], type(obj._branch[0])))
            common.validate_format(obj._branch[0], "objectReference", None, None)
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
        if "source" == "type" or (self.source is not self.__undef__ and (not (dirty and not self._source[1]))):
            dct["source"] = dictify(self.source)
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]))):
            dct["name"] = dictify(self.name)
        if "priority" == "type" or (self.priority is not self.__undef__ and (not (dirty and not self._priority[1]))):
            dct["priority"] = dictify(self.priority)
        if "timestamp" == "type" or (self.timestamp is not self.__undef__ and (not (dirty and not self._timestamp[1]))):
            dct["timestamp"] = dictify(self.timestamp)
        if "branch" == "type" or (self.branch is not self.__undef__ and (not (dirty and not self._branch[1]))):
            dct["branch"] = dictify(self.branch)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._source = (self._source[0], True)
        self._name = (self._name[0], True)
        self._priority = (self._priority[0], True)
        self._timestamp = (self._timestamp[0], True)
        self._branch = (self._branch[0], True)

    def is_dirty(self):
        return any([self._source[1], self._name[1], self._priority[1], self._timestamp[1], self._branch[1]])

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
        if not isinstance(other, JSSourceDataTimestamp):
            return False
        return super().__eq__(other) and \
               self.source == other.source and \
               self.name == other.name and \
               self.priority == other.priority and \
               self.timestamp == other.timestamp and \
               self.branch == other.branch

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def source(self):
        """
        A reference to the Self-Service data source.

        :rtype: ``str``
        """
        return self._source[0]

    @source.setter
    def source(self, value):
        self._source = (value, True)

    @property
    def name(self):
        """
        The name of the Self-Service data source.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def priority(self):
        """
        The priority of the Self-Service data source.

        :rtype: ``int``
        """
        return self._priority[0]

    @priority.setter
    def priority(self, value):
        self._priority = (value, True)

    @property
    def timestamp(self):
        """
        The point in the source's dataset time which is provisionable.

        :rtype: ``str``
        """
        return self._timestamp[0]

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = (value, True)

    @property
    def branch(self):
        """
        A reference to the Self-Service branch.

        :rtype: ``str``
        """
        return self._branch[0]

    @branch.setter
    def branch(self, value):
        self._branch = (value, True)

