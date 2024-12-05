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
#     /delphix-upgrade-check-result.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UpgradeCheckResult(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_39.web.vo.NamedUserObject` *)* Describes
    unsatisfied upgrade requirements.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UpgradeCheckResult", True)
        self._title = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._impact = (self.__undef__, True)
        self._action = (self.__undef__, True)
        self._output = (self.__undef__, True)
        self._severity = (self.__undef__, True)
        self._status = (self.__undef__, True)
        self._version = (self.__undef__, True)
        self._bundle_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._title = (data.get("title", obj.__undef__), dirty)
        if obj._title[0] is not None and obj._title[0] is not obj.__undef__:
            assert isinstance(obj._title[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._title[0], type(obj._title[0])))
            common.validate_format(obj._title[0], "None", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        obj._impact = (data.get("impact", obj.__undef__), dirty)
        if obj._impact[0] is not None and obj._impact[0] is not obj.__undef__:
            assert isinstance(obj._impact[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._impact[0], type(obj._impact[0])))
            common.validate_format(obj._impact[0], "None", None, None)
        obj._action = (data.get("action", obj.__undef__), dirty)
        if obj._action[0] is not None and obj._action[0] is not obj.__undef__:
            assert isinstance(obj._action[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._action[0], type(obj._action[0])))
            common.validate_format(obj._action[0], "None", None, None)
        obj._output = (data.get("output", obj.__undef__), dirty)
        if obj._output[0] is not None and obj._output[0] is not obj.__undef__:
            assert isinstance(obj._output[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._output[0], type(obj._output[0])))
            common.validate_format(obj._output[0], "None", None, None)
        obj._severity = (data.get("severity", obj.__undef__), dirty)
        if obj._severity[0] is not None and obj._severity[0] is not obj.__undef__:
            assert isinstance(obj._severity[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._severity[0], type(obj._severity[0])))
            assert obj._severity[0] in ['WARNING', 'CRITICAL', 'INFORMATIONAL'], "Expected enum ['WARNING', 'CRITICAL', 'INFORMATIONAL'] but got %s" % obj._severity[0]
            common.validate_format(obj._severity[0], "None", None, None)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            assert obj._status[0] in ['ACTIVE', 'IGNORED', 'RESOLVED'], "Expected enum ['ACTIVE', 'IGNORED', 'RESOLVED'] but got %s" % obj._status[0]
            common.validate_format(obj._status[0], "None", None, None)
        obj._version = (data.get("version", obj.__undef__), dirty)
        if obj._version[0] is not None and obj._version[0] is not obj.__undef__:
            assert isinstance(obj._version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._version[0], type(obj._version[0])))
            common.validate_format(obj._version[0], "objectReference", None, None)
        obj._bundle_id = (data.get("bundleId", obj.__undef__), dirty)
        if obj._bundle_id[0] is not None and obj._bundle_id[0] is not obj.__undef__:
            assert isinstance(obj._bundle_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bundle_id[0], type(obj._bundle_id[0])))
            common.validate_format(obj._bundle_id[0], "None", None, None)
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
        if "title" == "type" or (self.title is not self.__undef__ and (not (dirty and not self._title[1]))):
            dct["title"] = dictify(self.title)
        if dirty and "title" in dct:
            del dct["title"]
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]))):
            dct["description"] = dictify(self.description)
        if dirty and "description" in dct:
            del dct["description"]
        if "impact" == "type" or (self.impact is not self.__undef__ and (not (dirty and not self._impact[1]))):
            dct["impact"] = dictify(self.impact)
        if dirty and "impact" in dct:
            del dct["impact"]
        if "action" == "type" or (self.action is not self.__undef__ and (not (dirty and not self._action[1]))):
            dct["action"] = dictify(self.action)
        if dirty and "action" in dct:
            del dct["action"]
        if "output" == "type" or (self.output is not self.__undef__ and (not (dirty and not self._output[1]))):
            dct["output"] = dictify(self.output)
        if dirty and "output" in dct:
            del dct["output"]
        if "severity" == "type" or (self.severity is not self.__undef__ and (not (dirty and not self._severity[1]))):
            dct["severity"] = dictify(self.severity)
        if dirty and "severity" in dct:
            del dct["severity"]
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        if dirty and "status" in dct:
            del dct["status"]
        if "version" == "type" or (self.version is not self.__undef__ and (not (dirty and not self._version[1]))):
            dct["version"] = dictify(self.version)
        if dirty and "version" in dct:
            del dct["version"]
        if "bundle_id" == "type" or (self.bundle_id is not self.__undef__ and (not (dirty and not self._bundle_id[1]))):
            dct["bundleId"] = dictify(self.bundle_id)
        if dirty and "bundleId" in dct:
            del dct["bundleId"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._title = (self._title[0], True)
        self._description = (self._description[0], True)
        self._impact = (self._impact[0], True)
        self._action = (self._action[0], True)
        self._output = (self._output[0], True)
        self._severity = (self._severity[0], True)
        self._status = (self._status[0], True)
        self._version = (self._version[0], True)
        self._bundle_id = (self._bundle_id[0], True)

    def is_dirty(self):
        return any([self._title[1], self._description[1], self._impact[1], self._action[1], self._output[1], self._severity[1], self._status[1], self._version[1], self._bundle_id[1]])

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
        if not isinstance(other, UpgradeCheckResult):
            return False
        return super().__eq__(other) and \
               self.title == other.title and \
               self.description == other.description and \
               self.impact == other.impact and \
               self.action == other.action and \
               self.output == other.output and \
               self.severity == other.severity and \
               self.status == other.status and \
               self.version == other.version and \
               self.bundle_id == other.bundle_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.title,
            self.description,
            self.impact,
            self.action,
            self.output,
            self.severity,
            self.status,
            self.version,
            self.bundle_id,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def title(self):
        """
        A localized string that is the broad category of this check.

        :rtype: ``str``
        """
        return self._title[0]

    @property
    def description(self):
        """
        A localized, textual description of the error.

        :rtype: ``str``
        """
        return self._description[0]

    @property
    def impact(self):
        """
        A localized, textual description of the impact the error might have on
        the system.

        :rtype: ``str``
        """
        return self._impact[0]

    @property
    def action(self):
        """
        A localized, textual description of the action the user should take to
        overcome the error.

        :rtype: ``str``
        """
        return self._action[0]

    @property
    def output(self):
        """
        Script output related to the check result to assist in resolving the
        issue.

        :rtype: ``str``
        """
        return self._output[0]

    @property
    def severity(self):
        """
        The severity of the missing upgrade requirement. CRITICAL check results
        block the upgrade. *(permitted values: WARNING, CRITICAL,
        INFORMATIONAL)*

        :rtype: ``str``
        """
        return self._severity[0]

    @property
    def status(self):
        """
        The status of the upgrade check result. *(permitted values: ACTIVE,
        IGNORED, RESOLVED)*

        :rtype: ``str``
        """
        return self._status[0]

    @property
    def version(self):
        """
        A reference to the upgrade version that generated this check result.

        :rtype: ``str``
        """
        return self._version[0]

    @property
    def bundle_id(self):
        """
        A unique identifier for the type of the upgrade check result.

        :rtype: ``str``
        """
        return self._bundle_id[0]

