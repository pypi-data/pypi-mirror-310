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
#     /delphix-repave-engine-summary.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_27 import factory
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RepaveEngineSummary(TypedObject):
    """
    *(extends* :py:class:`v1_11_27.web.vo.TypedObject` *)* Engine summary for
    Repave.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RepaveEngineSummary", True)
        self._domain0_pool_guid = (self.__undef__, True)
        self._platform = (self.__undef__, True)
        self._engine_type = (self.__undef__, True)
        self._engine_uuid = (self.__undef__, True)
        self._engine_installation_time = (self.__undef__, True)
        self._engine_build_version = (self.__undef__, True)
        self._engine_storage_type = (self.__undef__, True)
        self._cache_devices = (self.__undef__, True)
        self._hotfixes = (self.__undef__, True)
        self._ssh_public_key = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._domain0_pool_guid = (data.get("domain0PoolGUID", obj.__undef__), dirty)
        if obj._domain0_pool_guid[0] is not None and obj._domain0_pool_guid[0] is not obj.__undef__:
            assert isinstance(obj._domain0_pool_guid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._domain0_pool_guid[0], type(obj._domain0_pool_guid[0])))
            common.validate_format(obj._domain0_pool_guid[0], "None", None, None)
        obj._platform = (data.get("platform", obj.__undef__), dirty)
        if obj._platform[0] is not None and obj._platform[0] is not obj.__undef__:
            assert isinstance(obj._platform[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._platform[0], type(obj._platform[0])))
            common.validate_format(obj._platform[0], "None", None, None)
        obj._engine_type = (data.get("engineType", obj.__undef__), dirty)
        if obj._engine_type[0] is not None and obj._engine_type[0] is not obj.__undef__:
            assert isinstance(obj._engine_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine_type[0], type(obj._engine_type[0])))
            assert obj._engine_type[0] in ['VIRTUALIZATION', 'MASKING', 'BOTH', 'UNSET'], "Expected enum ['VIRTUALIZATION', 'MASKING', 'BOTH', 'UNSET'] but got %s" % obj._engine_type[0]
            common.validate_format(obj._engine_type[0], "None", None, None)
        obj._engine_uuid = (data.get("engineUUID", obj.__undef__), dirty)
        if obj._engine_uuid[0] is not None and obj._engine_uuid[0] is not obj.__undef__:
            assert isinstance(obj._engine_uuid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine_uuid[0], type(obj._engine_uuid[0])))
            common.validate_format(obj._engine_uuid[0], "None", None, None)
        obj._engine_installation_time = (data.get("engineInstallationTime", obj.__undef__), dirty)
        if obj._engine_installation_time[0] is not None and obj._engine_installation_time[0] is not obj.__undef__:
            assert isinstance(obj._engine_installation_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine_installation_time[0], type(obj._engine_installation_time[0])))
            common.validate_format(obj._engine_installation_time[0], "date", None, None)
        if "engineBuildVersion" in data and data["engineBuildVersion"] is not None:
            obj._engine_build_version = (factory.create_object(data["engineBuildVersion"], "VersionInfo"), dirty)
            factory.validate_type(obj._engine_build_version[0], "VersionInfo")
        else:
            obj._engine_build_version = (obj.__undef__, dirty)
        obj._engine_storage_type = (data.get("engineStorageType", obj.__undef__), dirty)
        if obj._engine_storage_type[0] is not None and obj._engine_storage_type[0] is not obj.__undef__:
            assert isinstance(obj._engine_storage_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine_storage_type[0], type(obj._engine_storage_type[0])))
            assert obj._engine_storage_type[0] in ['UNINITIALIZED', 'S3', 'BLOB', 'BLOCK_STORAGE'], "Expected enum ['UNINITIALIZED', 'S3', 'BLOB', 'BLOCK_STORAGE'] but got %s" % obj._engine_storage_type[0]
            common.validate_format(obj._engine_storage_type[0], "None", None, None)
        obj._cache_devices = []
        for item in data.get("cacheDevices") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "objectReference", None, None)
            obj._cache_devices.append(item)
        obj._cache_devices = (obj._cache_devices, dirty)
        obj._hotfixes = (data.get("hotfixes", obj.__undef__), dirty)
        if obj._hotfixes[0] is not None and obj._hotfixes[0] is not obj.__undef__:
            assert isinstance(obj._hotfixes[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._hotfixes[0], type(obj._hotfixes[0])))
            common.validate_format(obj._hotfixes[0], "None", None, None)
        obj._ssh_public_key = (data.get("sshPublicKey", obj.__undef__), dirty)
        if obj._ssh_public_key[0] is not None and obj._ssh_public_key[0] is not obj.__undef__:
            assert isinstance(obj._ssh_public_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ssh_public_key[0], type(obj._ssh_public_key[0])))
            common.validate_format(obj._ssh_public_key[0], "None", None, None)
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
        if "domain0_pool_guid" == "type" or (self.domain0_pool_guid is not self.__undef__ and (not (dirty and not self._domain0_pool_guid[1]))):
            dct["domain0PoolGUID"] = dictify(self.domain0_pool_guid)
        if dirty and "domain0PoolGUID" in dct:
            del dct["domain0PoolGUID"]
        if "platform" == "type" or (self.platform is not self.__undef__ and (not (dirty and not self._platform[1]))):
            dct["platform"] = dictify(self.platform)
        if dirty and "platform" in dct:
            del dct["platform"]
        if "engine_type" == "type" or (self.engine_type is not self.__undef__ and (not (dirty and not self._engine_type[1]))):
            dct["engineType"] = dictify(self.engine_type)
        if dirty and "engineType" in dct:
            del dct["engineType"]
        if "engine_uuid" == "type" or (self.engine_uuid is not self.__undef__ and (not (dirty and not self._engine_uuid[1]))):
            dct["engineUUID"] = dictify(self.engine_uuid)
        if dirty and "engineUUID" in dct:
            del dct["engineUUID"]
        if "engine_installation_time" == "type" or (self.engine_installation_time is not self.__undef__ and (not (dirty and not self._engine_installation_time[1]))):
            dct["engineInstallationTime"] = dictify(self.engine_installation_time)
        if dirty and "engineInstallationTime" in dct:
            del dct["engineInstallationTime"]
        if "engine_build_version" == "type" or (self.engine_build_version is not self.__undef__ and (not (dirty and not self._engine_build_version[1]))):
            dct["engineBuildVersion"] = dictify(self.engine_build_version)
        if dirty and "engineBuildVersion" in dct:
            del dct["engineBuildVersion"]
        if "engine_storage_type" == "type" or (self.engine_storage_type is not self.__undef__ and (not (dirty and not self._engine_storage_type[1]))):
            dct["engineStorageType"] = dictify(self.engine_storage_type)
        if dirty and "engineStorageType" in dct:
            del dct["engineStorageType"]
        if "cache_devices" == "type" or (self.cache_devices is not self.__undef__ and (not (dirty and not self._cache_devices[1]))):
            dct["cacheDevices"] = dictify(self.cache_devices)
        if dirty and "cacheDevices" in dct:
            del dct["cacheDevices"]
        if "hotfixes" == "type" or (self.hotfixes is not self.__undef__ and (not (dirty and not self._hotfixes[1]))):
            dct["hotfixes"] = dictify(self.hotfixes)
        if dirty and "hotfixes" in dct:
            del dct["hotfixes"]
        if "ssh_public_key" == "type" or (self.ssh_public_key is not self.__undef__ and (not (dirty and not self._ssh_public_key[1]))):
            dct["sshPublicKey"] = dictify(self.ssh_public_key)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._domain0_pool_guid = (self._domain0_pool_guid[0], True)
        self._platform = (self._platform[0], True)
        self._engine_type = (self._engine_type[0], True)
        self._engine_uuid = (self._engine_uuid[0], True)
        self._engine_installation_time = (self._engine_installation_time[0], True)
        self._engine_build_version = (self._engine_build_version[0], True)
        self._engine_storage_type = (self._engine_storage_type[0], True)
        self._cache_devices = (self._cache_devices[0], True)
        self._hotfixes = (self._hotfixes[0], True)
        self._ssh_public_key = (self._ssh_public_key[0], True)

    def is_dirty(self):
        return any([self._domain0_pool_guid[1], self._platform[1], self._engine_type[1], self._engine_uuid[1], self._engine_installation_time[1], self._engine_build_version[1], self._engine_storage_type[1], self._cache_devices[1], self._hotfixes[1], self._ssh_public_key[1]])

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
        if not isinstance(other, RepaveEngineSummary):
            return False
        return super().__eq__(other) and \
               self.domain0_pool_guid == other.domain0_pool_guid and \
               self.platform == other.platform and \
               self.engine_type == other.engine_type and \
               self.engine_uuid == other.engine_uuid and \
               self.engine_installation_time == other.engine_installation_time and \
               self.engine_build_version == other.engine_build_version and \
               self.engine_storage_type == other.engine_storage_type and \
               self.cache_devices == other.cache_devices and \
               self.hotfixes == other.hotfixes and \
               self.ssh_public_key == other.ssh_public_key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def domain0_pool_guid(self):
        """
        GUID of DOMAIN0 Pool.

        :rtype: ``str``
        """
        return self._domain0_pool_guid[0]

    @property
    def platform(self):
        """
        Description of the current system platform.

        :rtype: ``str``
        """
        return self._platform[0]

    @property
    def engine_type(self):
        """
        *(default value: UNSET)* Engine type, could be Masking or
        Virtualization. *(permitted values: VIRTUALIZATION, MASKING, BOTH,
        UNSET)*

        :rtype: ``str``
        """
        return self._engine_type[0]

    @property
    def engine_uuid(self):
        """
        The UUID for this Delphix Engine.

        :rtype: ``str``
        """
        return self._engine_uuid[0]

    @property
    def engine_installation_time(self):
        """
        The date and time that the Delphix Engine was installed.

        :rtype: ``str``
        """
        return self._engine_installation_time[0]

    @property
    def engine_build_version(self):
        """
        Delphix version of the current system software.

        :rtype: :py:class:`v1_11_27.web.vo.VersionInfo`
        """
        return self._engine_build_version[0]

    @property
    def engine_storage_type(self):
        """
        *(default value: UNINITIALIZED)* Storage type of delphix engine.
        *(permitted values: UNINITIALIZED, S3, BLOB, BLOCK_STORAGE)*

        :rtype: ``str``
        """
        return self._engine_storage_type[0]

    @property
    def cache_devices(self):
        """
        List of storage devices to use.

        :rtype: ``list`` of ``str``
        """
        return self._cache_devices[0]

    @property
    def hotfixes(self):
        """
        List of hotfixes that were applied to this host.

        :rtype: ``str``
        """
        return self._hotfixes[0]

    @property
    def ssh_public_key(self):
        """
        SSH public key to be added to SSH authorized_keys for environment users
        using the SystemKeyCredential authorization mechanism.

        :rtype: ``str``
        """
        return self._ssh_public_key[0]

    @ssh_public_key.setter
    def ssh_public_key(self, value):
        self._ssh_public_key = (value, True)

