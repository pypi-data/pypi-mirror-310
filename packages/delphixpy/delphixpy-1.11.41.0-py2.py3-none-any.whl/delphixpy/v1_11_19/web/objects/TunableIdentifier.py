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
#     /delphix-tunable-identifier.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_19.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_19 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TunableIdentifier(TypedObject):
    """
    *(extends* :py:class:`v1_11_19.web.vo.TypedObject` *)* The subsystem and
    name for a tunable.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TunableIdentifier", True)
        self._subsystem = (self.__undef__, True)
        self._name = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "subsystem" not in data:
            raise ValueError("Missing required property \"subsystem\".")
        obj._subsystem = (data.get("subsystem", obj.__undef__), dirty)
        if obj._subsystem[0] is not None and obj._subsystem[0] is not obj.__undef__:
            assert isinstance(obj._subsystem[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._subsystem[0], type(obj._subsystem[0])))
            assert obj._subsystem[0] in ['virtualization', 'kernel', 'sysctl', 'service'], "Expected enum ['virtualization', 'kernel', 'sysctl', 'service'] but got %s" % obj._subsystem[0]
            common.validate_format(obj._subsystem[0], "None", None, None)
        if "name" not in data:
            raise ValueError("Missing required property \"name\".")
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, None)
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
        if "subsystem" == "type" or (self.subsystem is not self.__undef__ and (not (dirty and not self._subsystem[1]) or self.is_dirty_list(self.subsystem, self._subsystem) or belongs_to_parent)):
            dct["subsystem"] = dictify(self.subsystem)
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._subsystem = (self._subsystem[0], True)
        self._name = (self._name[0], True)

    def is_dirty(self):
        return any([self._subsystem[1], self._name[1]])

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
        if not isinstance(other, TunableIdentifier):
            return False
        return super().__eq__(other) and \
               self.subsystem == other.subsystem and \
               self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def subsystem(self):
        """
        The subsytem of the tunable represented by this object. *(permitted
        values: virtualization, kernel, sysctl, service)*

        :rtype: ``str``
        """
        return self._subsystem[0]

    @subsystem.setter
    def subsystem(self, value):
        self._subsystem = (value, True)

    @property
    def name(self):
        """
        Name of the tunable.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

