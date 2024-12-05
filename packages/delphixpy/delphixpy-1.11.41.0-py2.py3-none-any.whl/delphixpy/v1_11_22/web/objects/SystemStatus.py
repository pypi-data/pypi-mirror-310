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
#     /delphix-system-status.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_22.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_22 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SystemStatus(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_22.web.vo.NamedUserObject` *)* Provide
    important messages to System Admin User.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SystemStatus", True)
        self._description = (self.__undef__, True)
        self._severity = (self.__undef__, True)
        self._bundle_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        obj._severity = (data.get("severity", obj.__undef__), dirty)
        if obj._severity[0] is not None and obj._severity[0] is not obj.__undef__:
            assert isinstance(obj._severity[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._severity[0], type(obj._severity[0])))
            common.validate_format(obj._severity[0], "None", None, None)
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
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]))):
            dct["description"] = dictify(self.description)
        if dirty and "description" in dct:
            del dct["description"]
        if "severity" == "type" or (self.severity is not self.__undef__ and (not (dirty and not self._severity[1]))):
            dct["severity"] = dictify(self.severity)
        if dirty and "severity" in dct:
            del dct["severity"]
        if "bundle_id" == "type" or (self.bundle_id is not self.__undef__ and (not (dirty and not self._bundle_id[1]))):
            dct["bundleId"] = dictify(self.bundle_id)
        if dirty and "bundleId" in dct:
            del dct["bundleId"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._description = (self._description[0], True)
        self._severity = (self._severity[0], True)
        self._bundle_id = (self._bundle_id[0], True)

    def is_dirty(self):
        return any([self._description[1], self._severity[1], self._bundle_id[1]])

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
        if not isinstance(other, SystemStatus):
            return False
        return super().__eq__(other) and \
               self.description == other.description and \
               self.severity == other.severity and \
               self.bundle_id == other.bundle_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.description,
            self.severity,
            self.bundle_id,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def description(self):
        """
        A localized, textual description.

        :rtype: ``str``
        """
        return self._description[0]

    @property
    def severity(self):
        """
        A categorization of the impact of the event we are describing.

        :rtype: ``str``
        """
        return self._severity[0]

    @property
    def bundle_id(self):
        """
        A unique identifier for the type of the status message.

        :rtype: ``str``
        """
        return self._bundle_id[0]

