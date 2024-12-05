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
#     /delphix-file-mapping-result.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class FileMappingResult(TypedObject):
    """
    *(extends* :py:class:`v1_11_32.web.vo.TypedObject` *)* Result of a file
    mapping request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("FileMappingResult", True)
        self._mapped_files = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._mapped_files = (data.get("mappedFiles", obj.__undef__), dirty)
        if obj._mapped_files[0] is not None and obj._mapped_files[0] is not obj.__undef__:
            assert isinstance(obj._mapped_files[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._mapped_files[0], type(obj._mapped_files[0])))
            common.validate_format(obj._mapped_files[0], "None", None, None)
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
        if "mapped_files" == "type" or (self.mapped_files is not self.__undef__ and (not (dirty and not self._mapped_files[1]))):
            dct["mappedFiles"] = dictify(self.mapped_files)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._mapped_files = (self._mapped_files[0], True)

    def is_dirty(self):
        return any([self._mapped_files[1]])

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
        if not isinstance(other, FileMappingResult):
            return False
        return super().__eq__(other) and \
               self.mapped_files == other.mapped_files

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def mapped_files(self):
        """
        Mapped files.

        :rtype: ``dict``
        """
        return self._mapped_files[0]

    @mapped_files.setter
    def mapped_files(self, value):
        self._mapped_files = (value, True)

