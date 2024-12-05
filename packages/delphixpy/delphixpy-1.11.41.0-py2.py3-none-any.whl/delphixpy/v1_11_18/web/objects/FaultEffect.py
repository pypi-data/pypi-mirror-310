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
#     /delphix-fault-effect.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class FaultEffect(PersistentObject):
    """
    *(extends* :py:class:`v1_11_18.web.vo.PersistentObject` *)* An error
    affecting a user object whose root cause is a fault. A fault effect can
    only be resolved by resolving the fault which is its root cause.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("FaultEffect", True)
        self._bundle_id = (self.__undef__, True)
        self._title = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._response = (self.__undef__, True)
        self._action = (self.__undef__, True)
        self._severity = (self.__undef__, True)
        self._target = (self.__undef__, True)
        self._target_name = (self.__undef__, True)
        self._caused_by = (self.__undef__, True)
        self._root_cause = (self.__undef__, True)
        self._date_diagnosed = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._bundle_id = (data.get("bundleID", obj.__undef__), dirty)
        if obj._bundle_id[0] is not None and obj._bundle_id[0] is not obj.__undef__:
            assert isinstance(obj._bundle_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bundle_id[0], type(obj._bundle_id[0])))
            common.validate_format(obj._bundle_id[0], "None", None, None)
        obj._title = (data.get("title", obj.__undef__), dirty)
        if obj._title[0] is not None and obj._title[0] is not obj.__undef__:
            assert isinstance(obj._title[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._title[0], type(obj._title[0])))
            common.validate_format(obj._title[0], "None", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        obj._response = (data.get("response", obj.__undef__), dirty)
        if obj._response[0] is not None and obj._response[0] is not obj.__undef__:
            assert isinstance(obj._response[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._response[0], type(obj._response[0])))
            common.validate_format(obj._response[0], "None", None, None)
        obj._action = (data.get("action", obj.__undef__), dirty)
        if obj._action[0] is not None and obj._action[0] is not obj.__undef__:
            assert isinstance(obj._action[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._action[0], type(obj._action[0])))
            common.validate_format(obj._action[0], "None", None, None)
        obj._severity = (data.get("severity", obj.__undef__), dirty)
        if obj._severity[0] is not None and obj._severity[0] is not obj.__undef__:
            assert isinstance(obj._severity[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._severity[0], type(obj._severity[0])))
            assert obj._severity[0] in ['CRITICAL', 'WARNING'], "Expected enum ['CRITICAL', 'WARNING'] but got %s" % obj._severity[0]
            common.validate_format(obj._severity[0], "None", None, None)
        obj._target = (data.get("target", obj.__undef__), dirty)
        if obj._target[0] is not None and obj._target[0] is not obj.__undef__:
            assert isinstance(obj._target[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target[0], type(obj._target[0])))
            common.validate_format(obj._target[0], "objectReference", None, None)
        obj._target_name = (data.get("targetName", obj.__undef__), dirty)
        if obj._target_name[0] is not None and obj._target_name[0] is not obj.__undef__:
            assert isinstance(obj._target_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_name[0], type(obj._target_name[0])))
            common.validate_format(obj._target_name[0], "None", None, None)
        obj._caused_by = (data.get("causedBy", obj.__undef__), dirty)
        if obj._caused_by[0] is not None and obj._caused_by[0] is not obj.__undef__:
            assert isinstance(obj._caused_by[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._caused_by[0], type(obj._caused_by[0])))
            common.validate_format(obj._caused_by[0], "objectReference", None, None)
        obj._root_cause = (data.get("rootCause", obj.__undef__), dirty)
        if obj._root_cause[0] is not None and obj._root_cause[0] is not obj.__undef__:
            assert isinstance(obj._root_cause[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._root_cause[0], type(obj._root_cause[0])))
            common.validate_format(obj._root_cause[0], "objectReference", None, None)
        obj._date_diagnosed = (data.get("dateDiagnosed", obj.__undef__), dirty)
        if obj._date_diagnosed[0] is not None and obj._date_diagnosed[0] is not obj.__undef__:
            assert isinstance(obj._date_diagnosed[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._date_diagnosed[0], type(obj._date_diagnosed[0])))
            common.validate_format(obj._date_diagnosed[0], "date", None, None)
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
        if "bundle_id" == "type" or (self.bundle_id is not self.__undef__ and (not (dirty and not self._bundle_id[1]))):
            dct["bundleID"] = dictify(self.bundle_id)
        if "title" == "type" or (self.title is not self.__undef__ and (not (dirty and not self._title[1]))):
            dct["title"] = dictify(self.title)
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]))):
            dct["description"] = dictify(self.description)
        if "response" == "type" or (self.response is not self.__undef__ and (not (dirty and not self._response[1]))):
            dct["response"] = dictify(self.response)
        if "action" == "type" or (self.action is not self.__undef__ and (not (dirty and not self._action[1]))):
            dct["action"] = dictify(self.action)
        if "severity" == "type" or (self.severity is not self.__undef__ and (not (dirty and not self._severity[1]))):
            dct["severity"] = dictify(self.severity)
        if "target" == "type" or (self.target is not self.__undef__ and (not (dirty and not self._target[1]))):
            dct["target"] = dictify(self.target)
        if "target_name" == "type" or (self.target_name is not self.__undef__ and (not (dirty and not self._target_name[1]))):
            dct["targetName"] = dictify(self.target_name)
        if "caused_by" == "type" or (self.caused_by is not self.__undef__ and (not (dirty and not self._caused_by[1]))):
            dct["causedBy"] = dictify(self.caused_by)
        if "root_cause" == "type" or (self.root_cause is not self.__undef__ and (not (dirty and not self._root_cause[1]))):
            dct["rootCause"] = dictify(self.root_cause)
        if "date_diagnosed" == "type" or (self.date_diagnosed is not self.__undef__ and (not (dirty and not self._date_diagnosed[1]))):
            dct["dateDiagnosed"] = dictify(self.date_diagnosed)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._bundle_id = (self._bundle_id[0], True)
        self._title = (self._title[0], True)
        self._description = (self._description[0], True)
        self._response = (self._response[0], True)
        self._action = (self._action[0], True)
        self._severity = (self._severity[0], True)
        self._target = (self._target[0], True)
        self._target_name = (self._target_name[0], True)
        self._caused_by = (self._caused_by[0], True)
        self._root_cause = (self._root_cause[0], True)
        self._date_diagnosed = (self._date_diagnosed[0], True)

    def is_dirty(self):
        return any([self._bundle_id[1], self._title[1], self._description[1], self._response[1], self._action[1], self._severity[1], self._target[1], self._target_name[1], self._caused_by[1], self._root_cause[1], self._date_diagnosed[1]])

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
        if not isinstance(other, FaultEffect):
            return False
        return super().__eq__(other) and \
               self.bundle_id == other.bundle_id and \
               self.title == other.title and \
               self.description == other.description and \
               self.response == other.response and \
               self.action == other.action and \
               self.severity == other.severity and \
               self.target == other.target and \
               self.target_name == other.target_name and \
               self.caused_by == other.caused_by and \
               self.root_cause == other.root_cause and \
               self.date_diagnosed == other.date_diagnosed

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def bundle_id(self):
        """
        A unique dot delimited identifier associated with the fault effect.

        :rtype: ``str``
        """
        return self._bundle_id[0]

    @bundle_id.setter
    def bundle_id(self, value):
        self._bundle_id = (value, True)

    @property
    def title(self):
        """
        Summary of the fault effect.

        :rtype: ``str``
        """
        return self._title[0]

    @title.setter
    def title(self, value):
        self._title = (value, True)

    @property
    def description(self):
        """
        Full description of the fault effect.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def response(self):
        """
        The automated response taken by the system.

        :rtype: ``str``
        """
        return self._response[0]

    @response.setter
    def response(self, value):
        self._response = (value, True)

    @property
    def action(self):
        """
        A suggested user action.

        :rtype: ``str``
        """
        return self._action[0]

    @action.setter
    def action(self, value):
        self._action = (value, True)

    @property
    def severity(self):
        """
        The severity of the fault effect. This can either be CRITICAL or
        WARNING. *(permitted values: CRITICAL, WARNING)*

        :rtype: ``str``
        """
        return self._severity[0]

    @severity.setter
    def severity(self, value):
        self._severity = (value, True)

    @property
    def target(self):
        """
        The user-visible Delphix object that has a fault effect.

        :rtype: ``str``
        """
        return self._target[0]

    @target.setter
    def target(self, value):
        self._target = (value, True)

    @property
    def target_name(self):
        """
        The name of the user-visible Delphix object that has a fault effect.

        :rtype: ``str``
        """
        return self._target_name[0]

    @target_name.setter
    def target_name(self, value):
        self._target_name = (value, True)

    @property
    def caused_by(self):
        """
        The cause of the fault effect, in case there is a chain of fault
        effects originating from the root cause which resulted in this effect.

        :rtype: ``str``
        """
        return self._caused_by[0]

    @caused_by.setter
    def caused_by(self, value):
        self._caused_by = (value, True)

    @property
    def root_cause(self):
        """
        The root cause of this fault effect. Resolving the fault effect can
        only occur by resolving its root cause.

        :rtype: ``str``
        """
        return self._root_cause[0]

    @root_cause.setter
    def root_cause(self, value):
        self._root_cause = (value, True)

    @property
    def date_diagnosed(self):
        """
        The date when the root cause fault was diagnosed.

        :rtype: ``str``
        """
        return self._date_diagnosed[0]

    @date_diagnosed.setter
    def date_diagnosed(self, value):
        self._date_diagnosed = (value, True)

