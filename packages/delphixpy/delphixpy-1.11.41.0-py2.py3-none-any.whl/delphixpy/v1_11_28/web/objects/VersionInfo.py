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
#     /delphix-version-info.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_28.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_28 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class VersionInfo(TypedObject):
    """
    *(extends* :py:class:`v1_11_28.web.vo.TypedObject` *)* Representation of a
    Delphix software revision.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("VersionInfo", True)
        self._major = (self.__undef__, True)
        self._minor = (self.__undef__, True)
        self._micro = (self.__undef__, True)
        self._patch = (self.__undef__, True)
        self._pre_release = (self.__undef__, True)
        self._build_metadata = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._major = (data.get("major", obj.__undef__), dirty)
        if obj._major[0] is not None and obj._major[0] is not obj.__undef__:
            assert isinstance(obj._major[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._major[0], type(obj._major[0])))
            common.validate_format(obj._major[0], "None", None, None)
        obj._minor = (data.get("minor", obj.__undef__), dirty)
        if obj._minor[0] is not None and obj._minor[0] is not obj.__undef__:
            assert isinstance(obj._minor[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._minor[0], type(obj._minor[0])))
            common.validate_format(obj._minor[0], "None", None, None)
        obj._micro = (data.get("micro", obj.__undef__), dirty)
        if obj._micro[0] is not None and obj._micro[0] is not obj.__undef__:
            assert isinstance(obj._micro[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._micro[0], type(obj._micro[0])))
            common.validate_format(obj._micro[0], "None", None, None)
        obj._patch = (data.get("patch", obj.__undef__), dirty)
        if obj._patch[0] is not None and obj._patch[0] is not obj.__undef__:
            assert isinstance(obj._patch[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._patch[0], type(obj._patch[0])))
            common.validate_format(obj._patch[0], "None", None, None)
        obj._pre_release = []
        for item in data.get("preRelease") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._pre_release.append(item)
        obj._pre_release = (obj._pre_release, dirty)
        obj._build_metadata = []
        for item in data.get("buildMetadata") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._build_metadata.append(item)
        obj._build_metadata = (obj._build_metadata, dirty)
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
        if "major" == "type" or (self.major is not self.__undef__ and (not (dirty and not self._major[1]))):
            dct["major"] = dictify(self.major)
        if "minor" == "type" or (self.minor is not self.__undef__ and (not (dirty and not self._minor[1]))):
            dct["minor"] = dictify(self.minor)
        if "micro" == "type" or (self.micro is not self.__undef__ and (not (dirty and not self._micro[1]))):
            dct["micro"] = dictify(self.micro)
        if "patch" == "type" or (self.patch is not self.__undef__ and (not (dirty and not self._patch[1]))):
            dct["patch"] = dictify(self.patch)
        if "pre_release" == "type" or (self.pre_release is not self.__undef__ and (not (dirty and not self._pre_release[1]))):
            dct["preRelease"] = dictify(self.pre_release)
        if "build_metadata" == "type" or (self.build_metadata is not self.__undef__ and (not (dirty and not self._build_metadata[1]))):
            dct["buildMetadata"] = dictify(self.build_metadata)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._major = (self._major[0], True)
        self._minor = (self._minor[0], True)
        self._micro = (self._micro[0], True)
        self._patch = (self._patch[0], True)
        self._pre_release = (self._pre_release[0], True)
        self._build_metadata = (self._build_metadata[0], True)

    def is_dirty(self):
        return any([self._major[1], self._minor[1], self._micro[1], self._patch[1], self._pre_release[1], self._build_metadata[1]])

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
        if not isinstance(other, VersionInfo):
            return False
        return super().__eq__(other) and \
               self.major == other.major and \
               self.minor == other.minor and \
               self.micro == other.micro and \
               self.patch == other.patch and \
               self.pre_release == other.pre_release and \
               self.build_metadata == other.build_metadata

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def major(self):
        """
        Major version number.

        :rtype: ``int``
        """
        return self._major[0]

    @major.setter
    def major(self, value):
        self._major = (value, True)

    @property
    def minor(self):
        """
        Minor version number.

        :rtype: ``int``
        """
        return self._minor[0]

    @minor.setter
    def minor(self, value):
        self._minor = (value, True)

    @property
    def micro(self):
        """
        Micro version number.

        :rtype: ``int``
        """
        return self._micro[0]

    @micro.setter
    def micro(self, value):
        self._micro = (value, True)

    @property
    def patch(self):
        """
        Patch version number.

        :rtype: ``int``
        """
        return self._patch[0]

    @patch.setter
    def patch(self, value):
        self._patch = (value, True)

    @property
    def pre_release(self):
        """
        Pre-release version.

        :rtype: ``list`` of ``str``
        """
        return self._pre_release[0]

    @pre_release.setter
    def pre_release(self, value):
        self._pre_release = (value, True)

    @property
    def build_metadata(self):
        """
        Build metadata.

        :rtype: ``list`` of ``str``
        """
        return self._build_metadata[0]

    @build_metadata.setter
    def build_metadata(self, value):
        self._build_metadata = (value, True)

