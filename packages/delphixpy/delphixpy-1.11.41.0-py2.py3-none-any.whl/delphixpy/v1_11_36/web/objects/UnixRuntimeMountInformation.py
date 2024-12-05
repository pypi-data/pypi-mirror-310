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
#     /delphix-unix-mount-information.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.RuntimeMountInformation import RuntimeMountInformation
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UnixRuntimeMountInformation(RuntimeMountInformation):
    """
    *(extends* :py:class:`v1_11_36.web.vo.RuntimeMountInformation` *)* The
    representation of runtime mount information.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UnixRuntimeMountInformation", True)
        self._nfs_version = (self.__undef__, True)
        self._nfs_version_reason = (self.__undef__, True)
        self._encryption_enabled = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._nfs_version = (data.get("nfsVersion", obj.__undef__), dirty)
        if obj._nfs_version[0] is not None and obj._nfs_version[0] is not obj.__undef__:
            assert isinstance(obj._nfs_version[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._nfs_version[0], type(obj._nfs_version[0])))
            common.validate_format(obj._nfs_version[0], "None", None, None)
        obj._nfs_version_reason = (data.get("nfsVersionReason", obj.__undef__), dirty)
        if obj._nfs_version_reason[0] is not None and obj._nfs_version_reason[0] is not obj.__undef__:
            assert isinstance(obj._nfs_version_reason[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._nfs_version_reason[0], type(obj._nfs_version_reason[0])))
            assert obj._nfs_version_reason[0] in ['DEFAULT', 'OLD_REDHAT', 'UNSUPPORTED_OS', 'DNFS', 'TUNABLE_OVERRIDE', 'NO_RECOVER_LOST_LOCKS', 'UNSUPPORTED_DATA_PLATFORM', 'INCOMPLETE_V4_CONFIG'], "Expected enum ['DEFAULT', 'OLD_REDHAT', 'UNSUPPORTED_OS', 'DNFS', 'TUNABLE_OVERRIDE', 'NO_RECOVER_LOST_LOCKS', 'UNSUPPORTED_DATA_PLATFORM', 'INCOMPLETE_V4_CONFIG'] but got %s" % obj._nfs_version_reason[0]
            common.validate_format(obj._nfs_version_reason[0], "None", None, None)
        obj._encryption_enabled = (data.get("encryptionEnabled", obj.__undef__), dirty)
        if obj._encryption_enabled[0] is not None and obj._encryption_enabled[0] is not obj.__undef__:
            assert isinstance(obj._encryption_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._encryption_enabled[0], type(obj._encryption_enabled[0])))
            common.validate_format(obj._encryption_enabled[0], "None", None, None)
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
        if "nfs_version" == "type" or (self.nfs_version is not self.__undef__ and (not (dirty and not self._nfs_version[1]))):
            dct["nfsVersion"] = dictify(self.nfs_version)
        if dirty and "nfsVersion" in dct:
            del dct["nfsVersion"]
        if "nfs_version_reason" == "type" or (self.nfs_version_reason is not self.__undef__ and (not (dirty and not self._nfs_version_reason[1]))):
            dct["nfsVersionReason"] = dictify(self.nfs_version_reason)
        if dirty and "nfsVersionReason" in dct:
            del dct["nfsVersionReason"]
        if "encryption_enabled" == "type" or (self.encryption_enabled is not self.__undef__ and (not (dirty and not self._encryption_enabled[1]))):
            dct["encryptionEnabled"] = dictify(self.encryption_enabled)
        if dirty and "encryptionEnabled" in dct:
            del dct["encryptionEnabled"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._nfs_version = (self._nfs_version[0], True)
        self._nfs_version_reason = (self._nfs_version_reason[0], True)
        self._encryption_enabled = (self._encryption_enabled[0], True)

    def is_dirty(self):
        return any([self._nfs_version[1], self._nfs_version_reason[1], self._encryption_enabled[1]])

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
        if not isinstance(other, UnixRuntimeMountInformation):
            return False
        return super().__eq__(other) and \
               self.nfs_version == other.nfs_version and \
               self.nfs_version_reason == other.nfs_version_reason and \
               self.encryption_enabled == other.encryption_enabled

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.nfs_version,
            self.nfs_version_reason,
            self.encryption_enabled,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def nfs_version(self):
        """
        The NFS version that was last used to mount this source.

        :rtype: ``int``
        """
        return self._nfs_version[0]

    @property
    def nfs_version_reason(self):
        """
        The reason why the source is being mounted with nfsVersion. *(permitted
        values: DEFAULT, OLD_REDHAT, UNSUPPORTED_OS, DNFS, TUNABLE_OVERRIDE,
        NO_RECOVER_LOST_LOCKS, UNSUPPORTED_DATA_PLATFORM,
        INCOMPLETE_V4_CONFIG)*

        :rtype: ``str``
        """
        return self._nfs_version_reason[0]

    @property
    def encryption_enabled(self):
        """
        The flag for data transaction Encryption.

        :rtype: ``bool``
        """
        return self._encryption_enabled[0]

