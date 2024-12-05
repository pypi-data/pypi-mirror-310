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
#
# Do not edit this file manually!
#

from delphixpy.v1_11_17.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_17 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class GetLogParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_17.web.vo.TypedObject` *)* The parameters to
    use as input to Log.get.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("GetLogParameters", True)
        self._log_number = (self.__undef__, True)
        self._log_type = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._log_number = (data.get("logNumber", obj.__undef__), dirty)
        if obj._log_number[0] is not None and obj._log_number[0] is not obj.__undef__:
            assert isinstance(obj._log_number[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._log_number[0], type(obj._log_number[0])))
            common.validate_format(obj._log_number[0], "None", None, None)
        obj._log_type = (data.get("logType", obj.__undef__), dirty)
        if obj._log_type[0] is not None and obj._log_type[0] is not obj.__undef__:
            assert isinstance(obj._log_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._log_type[0], type(obj._log_type[0])))
            assert obj._log_type[0] in ['info', 'debug', 'error', 'trace'], "Expected enum ['info', 'debug', 'error', 'trace'] but got %s" % obj._log_type[0]
            common.validate_format(obj._log_type[0], "None", None, None)
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
        if "log_number" == "type" or (self.log_number is not self.__undef__ and (not (dirty and not self._log_number[1]) or self.is_dirty_list(self.log_number, self._log_number) or belongs_to_parent)):
            dct["logNumber"] = dictify(self.log_number)
        elif belongs_to_parent and self.log_number is self.__undef__:
            dct["logNumber"] = 0
        if "log_type" == "type" or (self.log_type is not self.__undef__ and (not (dirty and not self._log_type[1]) or self.is_dirty_list(self.log_type, self._log_type) or belongs_to_parent)):
            dct["logType"] = dictify(self.log_type)
        elif belongs_to_parent and self.log_type is self.__undef__:
            dct["logType"] = "debug"
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._log_number = (self._log_number[0], True)
        self._log_type = (self._log_type[0], True)

    def is_dirty(self):
        return any([self._log_number[1], self._log_type[1]])

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
        if not isinstance(other, GetLogParameters):
            return False
        return super().__eq__(other) and \
               self.log_number == other.log_number and \
               self.log_type == other.log_type

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def log_number(self):
        """
        Log number to return.

        :rtype: ``int``
        """
        return self._log_number[0]

    @log_number.setter
    def log_number(self, value):
        self._log_number = (value, True)

    @property
    def log_type(self):
        """
        *(default value: debug)* Type of log to retrieve. *(permitted values:
        info, debug, error, trace)*

        :rtype: ``str``
        """
        return self._log_type[0]

    @log_type.setter
    def log_type(self, value):
        self._log_type = (value, True)

