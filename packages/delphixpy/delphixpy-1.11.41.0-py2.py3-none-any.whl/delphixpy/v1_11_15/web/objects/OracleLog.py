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
#     /delphix-oracle-log.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_15.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_15 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleLog(TypedObject):
    """
    *(extends* :py:class:`v1_11_15.web.vo.TypedObject` *)* Oracle log file.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleLog", True)
        self._instance_num = (self.__undef__, True)
        self._sequence = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._instance_num = (data.get("instanceNum", obj.__undef__), dirty)
        if obj._instance_num[0] is not None and obj._instance_num[0] is not obj.__undef__:
            assert isinstance(obj._instance_num[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._instance_num[0], type(obj._instance_num[0])))
            common.validate_format(obj._instance_num[0], "None", None, None)
        obj._sequence = (data.get("sequence", obj.__undef__), dirty)
        if obj._sequence[0] is not None and obj._sequence[0] is not obj.__undef__:
            assert isinstance(obj._sequence[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._sequence[0], type(obj._sequence[0])))
            common.validate_format(obj._sequence[0], "None", None, None)
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
        if "instance_num" == "type" or (self.instance_num is not self.__undef__ and (not (dirty and not self._instance_num[1]))):
            dct["instanceNum"] = dictify(self.instance_num)
        if "sequence" == "type" or (self.sequence is not self.__undef__ and (not (dirty and not self._sequence[1]))):
            dct["sequence"] = dictify(self.sequence)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._instance_num = (self._instance_num[0], True)
        self._sequence = (self._sequence[0], True)

    def is_dirty(self):
        return any([self._instance_num[1], self._sequence[1]])

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
        if not isinstance(other, OracleLog):
            return False
        return super().__eq__(other) and \
               self.instance_num == other.instance_num and \
               self.sequence == other.sequence

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def instance_num(self):
        """
        Instance number associated with the log file.

        :rtype: ``int``
        """
        return self._instance_num[0]

    @instance_num.setter
    def instance_num(self, value):
        self._instance_num = (value, True)

    @property
    def sequence(self):
        """
        Sequence number for the log file.

        :rtype: ``int``
        """
        return self._sequence[0]

    @sequence.setter
    def sequence(self, value):
        self._sequence = (value, True)

