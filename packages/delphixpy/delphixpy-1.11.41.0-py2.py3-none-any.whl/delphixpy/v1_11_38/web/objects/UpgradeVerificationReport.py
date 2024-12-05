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
#     /delphix-upgrade-verification-report.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UpgradeVerificationReport(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_38.web.vo.NamedUserObject` *)* Describes the
    verification report of upgrade checks.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UpgradeVerificationReport", True)
        self._id = (self.__undef__, True)
        self._version = (self.__undef__, True)
        self._verification_version = (self.__undef__, True)
        self._report = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._id = (data.get("id", obj.__undef__), dirty)
        if obj._id[0] is not None and obj._id[0] is not obj.__undef__:
            assert isinstance(obj._id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._id[0], type(obj._id[0])))
            common.validate_format(obj._id[0], "None", None, None)
        obj._version = (data.get("version", obj.__undef__), dirty)
        if obj._version[0] is not None and obj._version[0] is not obj.__undef__:
            assert isinstance(obj._version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._version[0], type(obj._version[0])))
            common.validate_format(obj._version[0], "objectReference", None, None)
        obj._verification_version = (data.get("verificationVersion", obj.__undef__), dirty)
        if obj._verification_version[0] is not None and obj._verification_version[0] is not obj.__undef__:
            assert isinstance(obj._verification_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._verification_version[0], type(obj._verification_version[0])))
            common.validate_format(obj._verification_version[0], "None", None, None)
        obj._report = (data.get("report", obj.__undef__), dirty)
        if obj._report[0] is not None and obj._report[0] is not obj.__undef__:
            assert isinstance(obj._report[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._report[0], type(obj._report[0])))
            common.validate_format(obj._report[0], "None", None, None)
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
        if "id" == "type" or (self.id is not self.__undef__ and (not (dirty and not self._id[1]))):
            dct["id"] = dictify(self.id)
        if dirty and "id" in dct:
            del dct["id"]
        if "version" == "type" or (self.version is not self.__undef__ and (not (dirty and not self._version[1]))):
            dct["version"] = dictify(self.version)
        if dirty and "version" in dct:
            del dct["version"]
        if "verification_version" == "type" or (self.verification_version is not self.__undef__ and (not (dirty and not self._verification_version[1]))):
            dct["verificationVersion"] = dictify(self.verification_version)
        if dirty and "verificationVersion" in dct:
            del dct["verificationVersion"]
        if "report" == "type" or (self.report is not self.__undef__ and (not (dirty and not self._report[1]))):
            dct["report"] = dictify(self.report)
        if dirty and "report" in dct:
            del dct["report"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._id = (self._id[0], True)
        self._version = (self._version[0], True)
        self._verification_version = (self._verification_version[0], True)
        self._report = (self._report[0], True)

    def is_dirty(self):
        return any([self._id[1], self._version[1], self._verification_version[1], self._report[1]])

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
        if not isinstance(other, UpgradeVerificationReport):
            return False
        return super().__eq__(other) and \
               self.id == other.id and \
               self.version == other.version and \
               self.verification_version == other.verification_version and \
               self.report == other.report

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.id,
            self.version,
            self.verification_version,
            self.report,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def id(self):
        """
        A unique identifier for upgrade verification report.

        :rtype: ``str``
        """
        return self._id[0]

    @property
    def version(self):
        """
        A reference to the upgrade version that generated this check result.

        :rtype: ``str``
        """
        return self._version[0]

    @property
    def verification_version(self):
        """
        Verification package version.

        :rtype: ``str``
        """
        return self._verification_version[0]

    @property
    def report(self):
        """
        Upgrade verification report stored in json format.

        :rtype: ``str``
        """
        return self._report[0]

