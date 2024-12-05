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
#     /delphix-host-machine.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_24.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_24 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HostMachine(TypedObject):
    """
    *(extends* :py:class:`v1_11_24.web.vo.TypedObject` *)* The representation
    of the host machine.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HostMachine", True)
        self._platform = (self.__undef__, True)
        self._memory_size = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._platform = (data.get("platform", obj.__undef__), dirty)
        if obj._platform[0] is not None and obj._platform[0] is not obj.__undef__:
            assert isinstance(obj._platform[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._platform[0], type(obj._platform[0])))
            common.validate_format(obj._platform[0], "None", None, None)
        obj._memory_size = (data.get("memorySize", obj.__undef__), dirty)
        if obj._memory_size[0] is not None and obj._memory_size[0] is not obj.__undef__:
            assert isinstance(obj._memory_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._memory_size[0], type(obj._memory_size[0])))
            common.validate_format(obj._memory_size[0], "None", None, None)
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
        if "platform" == "type" or (self.platform is not self.__undef__ and (not (dirty and not self._platform[1]))):
            dct["platform"] = dictify(self.platform)
        if "memory_size" == "type" or (self.memory_size is not self.__undef__ and (not (dirty and not self._memory_size[1]))):
            dct["memorySize"] = dictify(self.memory_size)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._platform = (self._platform[0], True)
        self._memory_size = (self._memory_size[0], True)

    def is_dirty(self):
        return any([self._platform[1], self._memory_size[1]])

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
        if not isinstance(other, HostMachine):
            return False
        return super().__eq__(other) and \
               self.platform == other.platform and \
               self.memory_size == other.memory_size

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def platform(self):
        """
        The platform for the host machine.

        :rtype: ``str``
        """
        return self._platform[0]

    @platform.setter
    def platform(self, value):
        self._platform = (value, True)

    @property
    def memory_size(self):
        """
        The amount of RAM on the host machine.

        :rtype: ``float``
        """
        return self._memory_size[0]

    @memory_size.setter
    def memory_size(self, value):
        self._memory_size = (value, True)

