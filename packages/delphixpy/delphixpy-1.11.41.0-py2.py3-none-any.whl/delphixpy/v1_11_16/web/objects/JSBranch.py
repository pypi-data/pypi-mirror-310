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
#     /delphix-js-branch.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSBranch(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_16.web.vo.NamedUserObject` *)* A branch
    represents a distinct timeline for data sources in a data layout.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSBranch", True)
        self._data_layout = (self.__undef__, True)
        self._first_operation = (self.__undef__, True)
        self._last_operation = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._data_layout = (data.get("dataLayout", obj.__undef__), dirty)
        if obj._data_layout[0] is not None and obj._data_layout[0] is not obj.__undef__:
            assert isinstance(obj._data_layout[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._data_layout[0], type(obj._data_layout[0])))
            common.validate_format(obj._data_layout[0], "objectReference", None, None)
        obj._first_operation = (data.get("firstOperation", obj.__undef__), dirty)
        if obj._first_operation[0] is not None and obj._first_operation[0] is not obj.__undef__:
            assert isinstance(obj._first_operation[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._first_operation[0], type(obj._first_operation[0])))
            common.validate_format(obj._first_operation[0], "objectReference", None, None)
        obj._last_operation = (data.get("lastOperation", obj.__undef__), dirty)
        if obj._last_operation[0] is not None and obj._last_operation[0] is not obj.__undef__:
            assert isinstance(obj._last_operation[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_operation[0], type(obj._last_operation[0])))
            common.validate_format(obj._last_operation[0], "objectReference", None, None)
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
        if "data_layout" == "type" or (self.data_layout is not self.__undef__ and (not (dirty and not self._data_layout[1]))):
            dct["dataLayout"] = dictify(self.data_layout)
        if "first_operation" == "type" or (self.first_operation is not self.__undef__ and (not (dirty and not self._first_operation[1]))):
            dct["firstOperation"] = dictify(self.first_operation)
        if "last_operation" == "type" or (self.last_operation is not self.__undef__ and (not (dirty and not self._last_operation[1]))):
            dct["lastOperation"] = dictify(self.last_operation)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._data_layout = (self._data_layout[0], True)
        self._first_operation = (self._first_operation[0], True)
        self._last_operation = (self._last_operation[0], True)

    def is_dirty(self):
        return any([self._data_layout[1], self._first_operation[1], self._last_operation[1]])

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
        if not isinstance(other, JSBranch):
            return False
        return super().__eq__(other) and \
               self.data_layout == other.data_layout and \
               self.first_operation == other.first_operation and \
               self.last_operation == other.last_operation

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def data_layout(self):
        """
        A reference to the data layout this branch was created on.

        :rtype: ``str``
        """
        return self._data_layout[0]

    @data_layout.setter
    def data_layout(self, value):
        self._data_layout = (value, True)

    @property
    def first_operation(self):
        """
        The first JSOperation on this branch by data time.

        :rtype: ``str``
        """
        return self._first_operation[0]

    @first_operation.setter
    def first_operation(self, value):
        self._first_operation = (value, True)

    @property
    def last_operation(self):
        """
        The last JSOperation on this branch by data time.

        :rtype: ``str``
        """
        return self._last_operation[0]

    @last_operation.setter
    def last_operation(self, value):
        self._last_operation = (value, True)

