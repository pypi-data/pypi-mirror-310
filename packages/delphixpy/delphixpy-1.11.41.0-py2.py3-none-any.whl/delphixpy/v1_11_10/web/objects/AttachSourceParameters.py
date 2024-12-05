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
#     /delphix-attach-source-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_10.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_10 import factory
from delphixpy.v1_11_10 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AttachSourceParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_10.web.vo.TypedObject` *)* Represents the
    parameters of an attach request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AttachSourceParameters", True)
        self._attach_data = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "attachData" not in data:
            raise ValueError("Missing required property \"attachData\".")
        if "attachData" in data and data["attachData"] is not None:
            obj._attach_data = (factory.create_object(data["attachData"], "AttachData"), dirty)
            factory.validate_type(obj._attach_data[0], "AttachData")
        else:
            obj._attach_data = (obj.__undef__, dirty)
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
        if "attach_data" == "type" or (self.attach_data is not self.__undef__ and (not (dirty and not self._attach_data[1]) or self.is_dirty_list(self.attach_data, self._attach_data) or belongs_to_parent)):
            dct["attachData"] = dictify(self.attach_data, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._attach_data = (self._attach_data[0], True)

    def is_dirty(self):
        return any([self._attach_data[1]])

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
        if not isinstance(other, AttachSourceParameters):
            return False
        return super().__eq__(other) and \
               self.attach_data == other.attach_data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def attach_data(self):
        """
        The database-specific parameters of an attach request.

        :rtype: :py:class:`v1_11_10.web.vo.AttachData`
        """
        return self._attach_data[0]

    @attach_data.setter
    def attach_data(self, value):
        self._attach_data = (value, True)

