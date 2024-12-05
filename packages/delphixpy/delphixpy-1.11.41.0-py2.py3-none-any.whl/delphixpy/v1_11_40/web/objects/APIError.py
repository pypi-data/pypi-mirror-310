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
#     /delphix-api-error.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_40 import factory
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class APIError(TypedObject):
    """
    *(extends* :py:class:`v1_11_40.web.vo.TypedObject` *)* Description of an
    error encountered during an API call.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("APIError", True)
        self._details = (self.__undef__, True)
        self._action = (self.__undef__, True)
        self._id = (self.__undef__, True)
        self._command_output = (self.__undef__, True)
        self._diagnoses = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._details = (data.get("details", obj.__undef__), dirty)
        if obj._details[0] is not None and obj._details[0] is not obj.__undef__:
            assert isinstance(obj._details[0], dict) or isinstance(obj._details[0], str), ("Expected one of ['object', 'string'], but got %s of type %s" % (obj._details[0], type(obj._details[0])))
            common.validate_format(obj._details[0], "None", None, None)
        obj._action = (data.get("action", obj.__undef__), dirty)
        if obj._action[0] is not None and obj._action[0] is not obj.__undef__:
            assert isinstance(obj._action[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._action[0], type(obj._action[0])))
            common.validate_format(obj._action[0], "None", None, None)
        obj._id = (data.get("id", obj.__undef__), dirty)
        if obj._id[0] is not None and obj._id[0] is not obj.__undef__:
            assert isinstance(obj._id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._id[0], type(obj._id[0])))
            common.validate_format(obj._id[0], "None", None, None)
        obj._command_output = (data.get("commandOutput", obj.__undef__), dirty)
        if obj._command_output[0] is not None and obj._command_output[0] is not obj.__undef__:
            assert isinstance(obj._command_output[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._command_output[0], type(obj._command_output[0])))
            common.validate_format(obj._command_output[0], "None", None, None)
        obj._diagnoses = []
        for item in data.get("diagnoses") or []:
            obj._diagnoses.append(factory.create_object(item))
            factory.validate_type(obj._diagnoses[-1], "DiagnosisResult")
        obj._diagnoses = (obj._diagnoses, dirty)
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
        if "details" == "type" or (self.details is not self.__undef__ and (not (dirty and not self._details[1]))):
            dct["details"] = dictify(self.details)
        if "action" == "type" or (self.action is not self.__undef__ and (not (dirty and not self._action[1]))):
            dct["action"] = dictify(self.action)
        if "id" == "type" or (self.id is not self.__undef__ and (not (dirty and not self._id[1]))):
            dct["id"] = dictify(self.id)
        if "command_output" == "type" or (self.command_output is not self.__undef__ and (not (dirty and not self._command_output[1]))):
            dct["commandOutput"] = dictify(self.command_output)
        if "diagnoses" == "type" or (self.diagnoses is not self.__undef__ and (not (dirty and not self._diagnoses[1]))):
            dct["diagnoses"] = dictify(self.diagnoses)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._details = (self._details[0], True)
        self._action = (self._action[0], True)
        self._id = (self._id[0], True)
        self._command_output = (self._command_output[0], True)
        self._diagnoses = (self._diagnoses[0], True)

    def is_dirty(self):
        return any([self._details[1], self._action[1], self._id[1], self._command_output[1], self._diagnoses[1]])

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
        if not isinstance(other, APIError):
            return False
        return super().__eq__(other) and \
               self.details == other.details and \
               self.action == other.action and \
               self.id == other.id and \
               self.command_output == other.command_output and \
               self.diagnoses == other.diagnoses

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def details(self):
        """
        For validation errors, a map of fields to APIError objects. For all
        other errors, a string with further details of the error.

        :rtype: ``dict`` *or* ``str``
        """
        return self._details[0]

    @details.setter
    def details(self, value):
        self._details = (value, True)

    @property
    def action(self):
        """
        Action to be taken by the user, if any, to fix the underlying problem.

        :rtype: ``str``
        """
        return self._action[0]

    @action.setter
    def action(self, value):
        self._action = (value, True)

    @property
    def id(self):
        """
        A stable identifier for the class of error encountered.

        :rtype: ``str``
        """
        return self._id[0]

    @id.setter
    def id(self, value):
        self._id = (value, True)

    @property
    def command_output(self):
        """
        Extra output, often from a script or other external process, that may
        give more insight into the cause of this error.

        :rtype: ``str``
        """
        return self._command_output[0]

    @command_output.setter
    def command_output(self, value):
        self._command_output = (value, True)

    @property
    def diagnoses(self):
        """
        Results of diagnostic checks run, if any, if the job failed.

        :rtype: ``list`` of :py:class:`v1_11_40.web.vo.DiagnosisResult`
        """
        return self._diagnoses[0]

    @diagnoses.setter
    def diagnoses(self, value):
        self._diagnoses = (value, True)

