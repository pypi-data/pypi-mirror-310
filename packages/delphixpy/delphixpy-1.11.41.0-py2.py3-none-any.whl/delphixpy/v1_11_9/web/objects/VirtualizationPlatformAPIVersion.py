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
#     /delphix-virtualization-platform-api-version.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_9.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_9 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class VirtualizationPlatformAPIVersion(TypedObject):
    """
    *(extends* :py:class:`v1_11_9.web.vo.TypedObject` *)* A version of the
    Virtualization Platform API.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("VirtualizationPlatformAPIVersion", True)
        self._major = (self.__undef__, True)
        self._minor = (self.__undef__, True)
        self._micro = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "major" not in data:
            raise ValueError("Missing required property \"major\".")
        obj._major = (data.get("major", obj.__undef__), dirty)
        if obj._major[0] is not None and obj._major[0] is not obj.__undef__:
            assert isinstance(obj._major[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._major[0], type(obj._major[0])))
            common.validate_format(obj._major[0], "None", None, None)
        if "minor" not in data:
            raise ValueError("Missing required property \"minor\".")
        obj._minor = (data.get("minor", obj.__undef__), dirty)
        if obj._minor[0] is not None and obj._minor[0] is not obj.__undef__:
            assert isinstance(obj._minor[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._minor[0], type(obj._minor[0])))
            common.validate_format(obj._minor[0], "None", None, None)
        if "micro" not in data:
            raise ValueError("Missing required property \"micro\".")
        obj._micro = (data.get("micro", obj.__undef__), dirty)
        if obj._micro[0] is not None and obj._micro[0] is not obj.__undef__:
            assert isinstance(obj._micro[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._micro[0], type(obj._micro[0])))
            common.validate_format(obj._micro[0], "None", None, None)
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
        if "major" == "type" or (self.major is not self.__undef__ and (not (dirty and not self._major[1]) or self.is_dirty_list(self.major, self._major) or belongs_to_parent)):
            dct["major"] = dictify(self.major)
        if "minor" == "type" or (self.minor is not self.__undef__ and (not (dirty and not self._minor[1]) or self.is_dirty_list(self.minor, self._minor) or belongs_to_parent)):
            dct["minor"] = dictify(self.minor)
        if "micro" == "type" or (self.micro is not self.__undef__ and (not (dirty and not self._micro[1]) or self.is_dirty_list(self.micro, self._micro) or belongs_to_parent)):
            dct["micro"] = dictify(self.micro)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._major = (self._major[0], True)
        self._minor = (self._minor[0], True)
        self._micro = (self._micro[0], True)

    def is_dirty(self):
        return any([self._major[1], self._minor[1], self._micro[1]])

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
        if not isinstance(other, VirtualizationPlatformAPIVersion):
            return False
        return super().__eq__(other) and \
               self.major == other.major and \
               self.minor == other.minor and \
               self.micro == other.micro

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def major(self):
        """
        The major version of the API. A change in this number reflects a
        breaking API change.

        :rtype: ``int``
        """
        return self._major[0]

    @major.setter
    def major(self, value):
        self._major = (value, True)

    @property
    def minor(self):
        """
        The minor version of the API. A change in this number reflects a
        backwards compatible API change.

        :rtype: ``int``
        """
        return self._minor[0]

    @minor.setter
    def minor(self, value):
        self._minor = (value, True)

    @property
    def micro(self):
        """
        The micro version of the API. A change in this number reflects a change
        in behavior without an API change.

        :rtype: ``int``
        """
        return self._micro[0]

    @micro.setter
    def micro(self, value):
        self._micro = (value, True)

