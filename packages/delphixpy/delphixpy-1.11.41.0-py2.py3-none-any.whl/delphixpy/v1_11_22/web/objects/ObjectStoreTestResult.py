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
#     /delphix-object-store-test-result.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_22.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_22 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ObjectStoreTestResult(TypedObject):
    """
    *(extends* :py:class:`v1_11_22.web.vo.TypedObject` *)* An object store
    connectivity test result.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ObjectStoreTestResult", True)
        self._result = (self.__undef__, True)
        self._error_message = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._result = (data.get("result", obj.__undef__), dirty)
        if obj._result[0] is not None and obj._result[0] is not obj.__undef__:
            assert isinstance(obj._result[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._result[0], type(obj._result[0])))
            common.validate_format(obj._result[0], "None", None, None)
        obj._error_message = (data.get("errorMessage", obj.__undef__), dirty)
        if obj._error_message[0] is not None and obj._error_message[0] is not obj.__undef__:
            assert isinstance(obj._error_message[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._error_message[0], type(obj._error_message[0])))
            common.validate_format(obj._error_message[0], "None", None, None)
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
        if "result" == "type" or (self.result is not self.__undef__ and (not (dirty and not self._result[1]))):
            dct["result"] = dictify(self.result)
        if "error_message" == "type" or (self.error_message is not self.__undef__ and (not (dirty and not self._error_message[1]))):
            dct["errorMessage"] = dictify(self.error_message)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._result = (self._result[0], True)
        self._error_message = (self._error_message[0], True)

    def is_dirty(self):
        return any([self._result[1], self._error_message[1]])

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
        if not isinstance(other, ObjectStoreTestResult):
            return False
        return super().__eq__(other) and \
               self.result == other.result and \
               self.error_message == other.error_message

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def result(self):
        """
        The result of the connectivity test.

        :rtype: ``bool``
        """
        return self._result[0]

    @result.setter
    def result(self, value):
        self._result = (value, True)

    @property
    def error_message(self):
        """
        Error message from connectivity test.

        :rtype: ``str``
        """
        return self._error_message[0]

    @error_message.setter
    def error_message(self, value):
        self._error_message = (value, True)

