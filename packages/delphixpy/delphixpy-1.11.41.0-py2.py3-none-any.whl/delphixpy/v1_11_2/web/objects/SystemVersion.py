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
#     /delphix-upgrade-version.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_2.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_2 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SystemVersion(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_2.web.vo.NamedUserObject` *)* Describes a
    Delphix software revision.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SystemVersion", True)
        self._version = (self.__undef__, True)
        self._status = (self.__undef__, True)
        self._min_version = (self.__undef__, True)
        self._min_reboot_optional_version = (self.__undef__, True)
        self._build_date = (self.__undef__, True)
        self._install_date = (self.__undef__, True)
        self._verify_date = (self.__undef__, True)
        self._verification_version = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._version = (data.get("version", obj.__undef__), dirty)
        if obj._version[0] is not None and obj._version[0] is not obj.__undef__:
            assert isinstance(obj._version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._version[0], type(obj._version[0])))
            common.validate_format(obj._version[0], "None", None, None)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            assert obj._status[0] in ['PREVIOUS', 'CURRENTLY_RUNNING', 'DEFERRED', 'UPLOADED', 'UNPACKING', 'DELETING', 'VERIFYING', 'VERIFIED', 'APPLYING', 'UNKNOWN', 'DISABLE_FAILED'], "Expected enum ['PREVIOUS', 'CURRENTLY_RUNNING', 'DEFERRED', 'UPLOADED', 'UNPACKING', 'DELETING', 'VERIFYING', 'VERIFIED', 'APPLYING', 'UNKNOWN', 'DISABLE_FAILED'] but got %s" % obj._status[0]
            common.validate_format(obj._status[0], "None", None, None)
        obj._min_version = (data.get("minVersion", obj.__undef__), dirty)
        if obj._min_version[0] is not None and obj._min_version[0] is not obj.__undef__:
            assert isinstance(obj._min_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._min_version[0], type(obj._min_version[0])))
            common.validate_format(obj._min_version[0], "None", None, None)
        obj._min_reboot_optional_version = (data.get("minRebootOptionalVersion", obj.__undef__), dirty)
        if obj._min_reboot_optional_version[0] is not None and obj._min_reboot_optional_version[0] is not obj.__undef__:
            assert isinstance(obj._min_reboot_optional_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._min_reboot_optional_version[0], type(obj._min_reboot_optional_version[0])))
            common.validate_format(obj._min_reboot_optional_version[0], "None", None, None)
        obj._build_date = (data.get("buildDate", obj.__undef__), dirty)
        if obj._build_date[0] is not None and obj._build_date[0] is not obj.__undef__:
            assert isinstance(obj._build_date[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._build_date[0], type(obj._build_date[0])))
            common.validate_format(obj._build_date[0], "date", None, None)
        obj._install_date = (data.get("installDate", obj.__undef__), dirty)
        if obj._install_date[0] is not None and obj._install_date[0] is not obj.__undef__:
            assert isinstance(obj._install_date[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._install_date[0], type(obj._install_date[0])))
            common.validate_format(obj._install_date[0], "date", None, None)
        obj._verify_date = (data.get("verifyDate", obj.__undef__), dirty)
        if obj._verify_date[0] is not None and obj._verify_date[0] is not obj.__undef__:
            assert isinstance(obj._verify_date[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._verify_date[0], type(obj._verify_date[0])))
            common.validate_format(obj._verify_date[0], "date", None, None)
        obj._verification_version = (data.get("verificationVersion", obj.__undef__), dirty)
        if obj._verification_version[0] is not None and obj._verification_version[0] is not obj.__undef__:
            assert isinstance(obj._verification_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._verification_version[0], type(obj._verification_version[0])))
            common.validate_format(obj._verification_version[0], "None", None, None)
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
        if "version" == "type" or (self.version is not self.__undef__ and (not (dirty and not self._version[1]))):
            dct["version"] = dictify(self.version)
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        if "min_version" == "type" or (self.min_version is not self.__undef__ and (not (dirty and not self._min_version[1]))):
            dct["minVersion"] = dictify(self.min_version)
        if "min_reboot_optional_version" == "type" or (self.min_reboot_optional_version is not self.__undef__ and (not (dirty and not self._min_reboot_optional_version[1]))):
            dct["minRebootOptionalVersion"] = dictify(self.min_reboot_optional_version)
        if "build_date" == "type" or (self.build_date is not self.__undef__ and (not (dirty and not self._build_date[1]))):
            dct["buildDate"] = dictify(self.build_date)
        if "install_date" == "type" or (self.install_date is not self.__undef__ and (not (dirty and not self._install_date[1]))):
            dct["installDate"] = dictify(self.install_date)
        if "verify_date" == "type" or (self.verify_date is not self.__undef__ and (not (dirty and not self._verify_date[1]))):
            dct["verifyDate"] = dictify(self.verify_date)
        if "verification_version" == "type" or (self.verification_version is not self.__undef__ and (not (dirty and not self._verification_version[1]))):
            dct["verificationVersion"] = dictify(self.verification_version)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._version = (self._version[0], True)
        self._status = (self._status[0], True)
        self._min_version = (self._min_version[0], True)
        self._min_reboot_optional_version = (self._min_reboot_optional_version[0], True)
        self._build_date = (self._build_date[0], True)
        self._install_date = (self._install_date[0], True)
        self._verify_date = (self._verify_date[0], True)
        self._verification_version = (self._verification_version[0], True)

    def is_dirty(self):
        return any([self._version[1], self._status[1], self._min_version[1], self._min_reboot_optional_version[1], self._build_date[1], self._install_date[1], self._verify_date[1], self._verification_version[1]])

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
        if not isinstance(other, SystemVersion):
            return False
        return super().__eq__(other) and \
               self.version == other.version and \
               self.status == other.status and \
               self.min_version == other.min_version and \
               self.min_reboot_optional_version == other.min_reboot_optional_version and \
               self.build_date == other.build_date and \
               self.install_date == other.install_date and \
               self.verify_date == other.verify_date and \
               self.verification_version == other.verification_version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def version(self):
        """
        The Delphix version number.

        :rtype: ``str``
        """
        return self._version[0]

    @version.setter
    def version(self, value):
        self._version = (value, True)

    @property
    def status(self):
        """
        The state of the version. *(permitted values: PREVIOUS,
        CURRENTLY_RUNNING, DEFERRED, UPLOADED, UNPACKING, DELETING, VERIFYING,
        VERIFIED, APPLYING, UNKNOWN, DISABLE_FAILED)*

        :rtype: ``str``
        """
        return self._status[0]

    @status.setter
    def status(self, value):
        self._status = (value, True)

    @property
    def min_version(self):
        """
        The minimum required Delphix version in order to upgrade.

        :rtype: ``str``
        """
        return self._min_version[0]

    @min_version.setter
    def min_version(self, value):
        self._min_version = (value, True)

    @property
    def min_reboot_optional_version(self):
        """
        The minimum version from which a reboot upgrade is optional.

        :rtype: ``str``
        """
        return self._min_reboot_optional_version[0]

    @min_reboot_optional_version.setter
    def min_reboot_optional_version(self, value):
        self._min_reboot_optional_version = (value, True)

    @property
    def build_date(self):
        """
        Date on which the version was built.

        :rtype: ``str``
        """
        return self._build_date[0]

    @build_date.setter
    def build_date(self, value):
        self._build_date = (value, True)

    @property
    def install_date(self):
        """
        Date on which this version was installed.

        :rtype: ``str``
        """
        return self._install_date[0]

    @install_date.setter
    def install_date(self, value):
        self._install_date = (value, True)

    @property
    def verify_date(self):
        """
        Date on which this version was last verified.

        :rtype: ``str``
        """
        return self._verify_date[0]

    @verify_date.setter
    def verify_date(self, value):
        self._verify_date = (value, True)

    @property
    def verification_version(self):
        """
        The version number of the verification package.

        :rtype: ``str``
        """
        return self._verification_version[0]

    @verification_version.setter
    def verification_version(self, value):
        self._verification_version = (value, True)

