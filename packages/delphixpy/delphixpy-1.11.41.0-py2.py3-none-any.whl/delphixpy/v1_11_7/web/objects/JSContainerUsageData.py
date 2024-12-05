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
#     /delphix-js-container-usage-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_7.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_7 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSContainerUsageData(TypedObject):
    """
    *(extends* :py:class:`v1_11_7.web.vo.TypedObject` *)* The space usage
    information for a data container.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSContainerUsageData", True)
        self._data_container = (self.__undef__, True)
        self._unique = (self.__undef__, True)
        self._shared_others = (self.__undef__, True)
        self._shared_self = (self.__undef__, True)
        self._unvirtualized = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._data_container = (data.get("dataContainer", obj.__undef__), dirty)
        if obj._data_container[0] is not None and obj._data_container[0] is not obj.__undef__:
            assert isinstance(obj._data_container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._data_container[0], type(obj._data_container[0])))
            common.validate_format(obj._data_container[0], "objectReference", None, None)
        obj._unique = (data.get("unique", obj.__undef__), dirty)
        if obj._unique[0] is not None and obj._unique[0] is not obj.__undef__:
            assert isinstance(obj._unique[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._unique[0], type(obj._unique[0])))
            common.validate_format(obj._unique[0], "None", None, None)
        obj._shared_others = (data.get("sharedOthers", obj.__undef__), dirty)
        if obj._shared_others[0] is not None and obj._shared_others[0] is not obj.__undef__:
            assert isinstance(obj._shared_others[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._shared_others[0], type(obj._shared_others[0])))
            common.validate_format(obj._shared_others[0], "None", None, None)
        obj._shared_self = (data.get("sharedSelf", obj.__undef__), dirty)
        if obj._shared_self[0] is not None and obj._shared_self[0] is not obj.__undef__:
            assert isinstance(obj._shared_self[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._shared_self[0], type(obj._shared_self[0])))
            common.validate_format(obj._shared_self[0], "None", None, None)
        obj._unvirtualized = (data.get("unvirtualized", obj.__undef__), dirty)
        if obj._unvirtualized[0] is not None and obj._unvirtualized[0] is not obj.__undef__:
            assert isinstance(obj._unvirtualized[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._unvirtualized[0], type(obj._unvirtualized[0])))
            common.validate_format(obj._unvirtualized[0], "None", None, None)
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
        if "data_container" == "type" or (self.data_container is not self.__undef__ and (not (dirty and not self._data_container[1]))):
            dct["dataContainer"] = dictify(self.data_container)
        if "unique" == "type" or (self.unique is not self.__undef__ and (not (dirty and not self._unique[1]))):
            dct["unique"] = dictify(self.unique)
        if "shared_others" == "type" or (self.shared_others is not self.__undef__ and (not (dirty and not self._shared_others[1]))):
            dct["sharedOthers"] = dictify(self.shared_others)
        if "shared_self" == "type" or (self.shared_self is not self.__undef__ and (not (dirty and not self._shared_self[1]))):
            dct["sharedSelf"] = dictify(self.shared_self)
        if "unvirtualized" == "type" or (self.unvirtualized is not self.__undef__ and (not (dirty and not self._unvirtualized[1]))):
            dct["unvirtualized"] = dictify(self.unvirtualized)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._data_container = (self._data_container[0], True)
        self._unique = (self._unique[0], True)
        self._shared_others = (self._shared_others[0], True)
        self._shared_self = (self._shared_self[0], True)
        self._unvirtualized = (self._unvirtualized[0], True)

    def is_dirty(self):
        return any([self._data_container[1], self._unique[1], self._shared_others[1], self._shared_self[1], self._unvirtualized[1]])

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
        if not isinstance(other, JSContainerUsageData):
            return False
        return super().__eq__(other) and \
               self.data_container == other.data_container and \
               self.unique == other.unique and \
               self.shared_others == other.shared_others and \
               self.shared_self == other.shared_self and \
               self.unvirtualized == other.unvirtualized

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def data_container(self):
        """
        The data container that this usage information is for.

        :rtype: ``str``
        """
        return self._data_container[0]

    @data_container.setter
    def data_container(self, value):
        self._data_container = (value, True)

    @property
    def unique(self):
        """
        The amount of space that will be freed if this data container is
        deleted or purged. This assumes that the data container is deleted
        along with underlying data sources.

        :rtype: ``float``
        """
        return self._unique[0]

    @unique.setter
    def unique(self, value):
        self._unique = (value, True)

    @property
    def shared_others(self):
        """
        The amount of space that cannot be freed on the parent data template
        (or sibling data containers) because it is also being referenced by
        this data container due to restore or create branch operations.

        :rtype: ``float``
        """
        return self._shared_others[0]

    @shared_others.setter
    def shared_others(self, value):
        self._shared_others = (value, True)

    @property
    def shared_self(self):
        """
        The amount of space that cannot be freed on this data container because
        it is also being referenced by sibling data containers due to restore
        or create branch operations.

        :rtype: ``float``
        """
        return self._shared_self[0]

    @shared_self.setter
    def shared_self(self, value):
        self._shared_self = (value, True)

    @property
    def unvirtualized(self):
        """
        The amount of space that would be consumed by the data in this
        container without Delphix.

        :rtype: ``float``
        """
        return self._unvirtualized[0]

    @unvirtualized.setter
    def unvirtualized(self, value):
        self._unvirtualized = (value, True)

