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
#     /delphix-identifiable-array-element.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_41.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_41 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class IdentifiableArrayElement(TypedObject):
    """
    *(extends* :py:class:`v1_11_41.web.vo.TypedObject` *)* Object that can be
    uniquely identified within an array.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("IdentifiableArrayElement", True)
        self._element_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._element_id = (data.get("elementId", obj.__undef__), dirty)
        if obj._element_id[0] is not None and obj._element_id[0] is not obj.__undef__:
            assert isinstance(obj._element_id[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._element_id[0], type(obj._element_id[0])))
            common.validate_format(obj._element_id[0], "None", None, None)
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
        if "element_id" == "type" or (self.element_id is not self.__undef__ and (not (dirty and not self._element_id[1]) or self.is_dirty_list(self.element_id, self._element_id) or belongs_to_parent)):
            dct["elementId"] = dictify(self.element_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._element_id = (self._element_id[0], True)

    def is_dirty(self):
        return any([self._element_id[1]])

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
        if not isinstance(other, IdentifiableArrayElement):
            return False
        return super().__eq__(other) and \
               self.element_id == other.element_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def element_id(self):
        """
        Unique identifier generated by the engine when this object is in an
        array. If this value is set and this object is in an update request,
        this id identifies the element to update in the existing array. In that
        case, this object can be "sparse" (only the changed properties need to
        be included). The resulting position of the element in the array is its
        position in the update. If an element with this id does not exist, this
        object is ignored. If the id is not set, a new object is added to the
        array and a new id is assigned to it by the engine. If an existing
        element id is omitted from an update, the corresponding element is
        deleted. To preserve an existing array element unchanged, the API
        client must include an element in the update with just this id.

        :rtype: ``str`` *or* ``null``
        """
        return self._element_id[0]

    @element_id.setter
    def element_id(self, value):
        self._element_id = (value, True)

