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
#     /delphix-system.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_37.web.objects.PublicSystemInfo import PublicSystemInfo
from delphixpy.v1_11_37 import factory
from delphixpy.v1_11_37 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SystemInfo(PublicSystemInfo):
    """
    *(extends* :py:class:`v1_11_37.web.vo.PublicSystemInfo` *)* Retrieve
    system-wide properties and manage the state of the system.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SystemInfo", True)
        self._hostname = (self.__undef__, True)
        self._max_heap_size_gb = (self.__undef__, True)
        self._max_native_memory_gb = (self.__undef__, True)
        self._ssh_public_key = (self.__undef__, True)
        self._memory_size = (self.__undef__, True)
        self._platform = (self.__undef__, True)
        self._cloud_region = (self.__undef__, True)
        self._uuid = (self.__undef__, True)
        self._processors = (self.__undef__, True)
        self._storage_used = (self.__undef__, True)
        self._storage_total = (self.__undef__, True)
        self._installation_time = (self.__undef__, True)
        self._up_time = (self.__undef__, True)
        self._memory_reservation = (self.__undef__, True)
        self._cpu_reservation = (self.__undef__, True)
        self._hotfixes = (self.__undef__, True)
        self._pool_fragmentation = (self.__undef__, True)
        self._smtp_configured = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._hostname = (data.get("hostname", obj.__undef__), dirty)
        if obj._hostname[0] is not None and obj._hostname[0] is not obj.__undef__:
            assert isinstance(obj._hostname[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._hostname[0], type(obj._hostname[0])))
            common.validate_format(obj._hostname[0], "hostname", None, None)
        obj._max_heap_size_gb = (data.get("maxHeapSizeGb", obj.__undef__), dirty)
        if obj._max_heap_size_gb[0] is not None and obj._max_heap_size_gb[0] is not obj.__undef__:
            assert isinstance(obj._max_heap_size_gb[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._max_heap_size_gb[0], type(obj._max_heap_size_gb[0])))
            common.validate_format(obj._max_heap_size_gb[0], "None", None, None)
        obj._max_native_memory_gb = (data.get("maxNativeMemoryGb", obj.__undef__), dirty)
        if obj._max_native_memory_gb[0] is not None and obj._max_native_memory_gb[0] is not obj.__undef__:
            assert isinstance(obj._max_native_memory_gb[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._max_native_memory_gb[0], type(obj._max_native_memory_gb[0])))
            common.validate_format(obj._max_native_memory_gb[0], "None", None, None)
        obj._ssh_public_key = (data.get("sshPublicKey", obj.__undef__), dirty)
        if obj._ssh_public_key[0] is not None and obj._ssh_public_key[0] is not obj.__undef__:
            assert isinstance(obj._ssh_public_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ssh_public_key[0], type(obj._ssh_public_key[0])))
            common.validate_format(obj._ssh_public_key[0], "None", None, None)
        obj._memory_size = (data.get("memorySize", obj.__undef__), dirty)
        if obj._memory_size[0] is not None and obj._memory_size[0] is not obj.__undef__:
            assert isinstance(obj._memory_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._memory_size[0], type(obj._memory_size[0])))
            common.validate_format(obj._memory_size[0], "None", None, None)
        obj._platform = (data.get("platform", obj.__undef__), dirty)
        if obj._platform[0] is not None and obj._platform[0] is not obj.__undef__:
            assert isinstance(obj._platform[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._platform[0], type(obj._platform[0])))
            common.validate_format(obj._platform[0], "None", None, None)
        obj._cloud_region = (data.get("cloudRegion", obj.__undef__), dirty)
        if obj._cloud_region[0] is not None and obj._cloud_region[0] is not obj.__undef__:
            assert isinstance(obj._cloud_region[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._cloud_region[0], type(obj._cloud_region[0])))
            common.validate_format(obj._cloud_region[0], "None", None, None)
        obj._uuid = (data.get("uuid", obj.__undef__), dirty)
        if obj._uuid[0] is not None and obj._uuid[0] is not obj.__undef__:
            assert isinstance(obj._uuid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._uuid[0], type(obj._uuid[0])))
            common.validate_format(obj._uuid[0], "None", None, None)
        obj._processors = []
        for item in data.get("processors") or []:
            obj._processors.append(factory.create_object(item))
            factory.validate_type(obj._processors[-1], "CPUInfo")
        obj._processors = (obj._processors, dirty)
        obj._storage_used = (data.get("storageUsed", obj.__undef__), dirty)
        if obj._storage_used[0] is not None and obj._storage_used[0] is not obj.__undef__:
            assert isinstance(obj._storage_used[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._storage_used[0], type(obj._storage_used[0])))
            common.validate_format(obj._storage_used[0], "None", None, None)
        obj._storage_total = (data.get("storageTotal", obj.__undef__), dirty)
        if obj._storage_total[0] is not None and obj._storage_total[0] is not obj.__undef__:
            assert isinstance(obj._storage_total[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._storage_total[0], type(obj._storage_total[0])))
            common.validate_format(obj._storage_total[0], "None", None, None)
        obj._installation_time = (data.get("installationTime", obj.__undef__), dirty)
        if obj._installation_time[0] is not None and obj._installation_time[0] is not obj.__undef__:
            assert isinstance(obj._installation_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._installation_time[0], type(obj._installation_time[0])))
            common.validate_format(obj._installation_time[0], "date", None, None)
        if "upTime" in data and data["upTime"] is not None:
            obj._up_time = (factory.create_object(data["upTime"], "UpTimeInfo"), dirty)
            factory.validate_type(obj._up_time[0], "UpTimeInfo")
        else:
            obj._up_time = (obj.__undef__, dirty)
        obj._memory_reservation = (data.get("memoryReservation", obj.__undef__), dirty)
        if obj._memory_reservation[0] is not None and obj._memory_reservation[0] is not obj.__undef__:
            assert isinstance(obj._memory_reservation[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._memory_reservation[0], type(obj._memory_reservation[0])))
            common.validate_format(obj._memory_reservation[0], "None", None, None)
        obj._cpu_reservation = (data.get("cpuReservation", obj.__undef__), dirty)
        if obj._cpu_reservation[0] is not None and obj._cpu_reservation[0] is not obj.__undef__:
            assert isinstance(obj._cpu_reservation[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._cpu_reservation[0], type(obj._cpu_reservation[0])))
            common.validate_format(obj._cpu_reservation[0], "None", None, None)
        obj._hotfixes = (data.get("hotfixes", obj.__undef__), dirty)
        if obj._hotfixes[0] is not None and obj._hotfixes[0] is not obj.__undef__:
            assert isinstance(obj._hotfixes[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._hotfixes[0], type(obj._hotfixes[0])))
            common.validate_format(obj._hotfixes[0], "None", None, None)
        obj._pool_fragmentation = (data.get("poolFragmentation", obj.__undef__), dirty)
        if obj._pool_fragmentation[0] is not None and obj._pool_fragmentation[0] is not obj.__undef__:
            assert isinstance(obj._pool_fragmentation[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._pool_fragmentation[0], type(obj._pool_fragmentation[0])))
            common.validate_format(obj._pool_fragmentation[0], "None", None, None)
        obj._smtp_configured = (data.get("smtpConfigured", obj.__undef__), dirty)
        if obj._smtp_configured[0] is not None and obj._smtp_configured[0] is not obj.__undef__:
            assert isinstance(obj._smtp_configured[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._smtp_configured[0], type(obj._smtp_configured[0])))
            common.validate_format(obj._smtp_configured[0], "None", None, None)
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
        if "hostname" == "type" or (self.hostname is not self.__undef__ and (not (dirty and not self._hostname[1]) or self.is_dirty_list(self.hostname, self._hostname) or belongs_to_parent)):
            dct["hostname"] = dictify(self.hostname)
        if "max_heap_size_gb" == "type" or (self.max_heap_size_gb is not self.__undef__ and (not (dirty and not self._max_heap_size_gb[1]) or self.is_dirty_list(self.max_heap_size_gb, self._max_heap_size_gb) or belongs_to_parent)):
            dct["maxHeapSizeGb"] = dictify(self.max_heap_size_gb)
        if "max_native_memory_gb" == "type" or (self.max_native_memory_gb is not self.__undef__ and (not (dirty and not self._max_native_memory_gb[1]) or self.is_dirty_list(self.max_native_memory_gb, self._max_native_memory_gb) or belongs_to_parent)):
            dct["maxNativeMemoryGb"] = dictify(self.max_native_memory_gb)
        if "ssh_public_key" == "type" or (self.ssh_public_key is not self.__undef__ and (not (dirty and not self._ssh_public_key[1]))):
            dct["sshPublicKey"] = dictify(self.ssh_public_key)
        if "memory_size" == "type" or (self.memory_size is not self.__undef__ and (not (dirty and not self._memory_size[1]))):
            dct["memorySize"] = dictify(self.memory_size)
        if "platform" == "type" or (self.platform is not self.__undef__ and (not (dirty and not self._platform[1]))):
            dct["platform"] = dictify(self.platform)
        if "cloud_region" == "type" or (self.cloud_region is not self.__undef__ and (not (dirty and not self._cloud_region[1]))):
            dct["cloudRegion"] = dictify(self.cloud_region)
        if "uuid" == "type" or (self.uuid is not self.__undef__ and (not (dirty and not self._uuid[1]))):
            dct["uuid"] = dictify(self.uuid)
        if "processors" == "type" or (self.processors is not self.__undef__ and (not (dirty and not self._processors[1]))):
            dct["processors"] = dictify(self.processors)
        if "storage_used" == "type" or (self.storage_used is not self.__undef__ and (not (dirty and not self._storage_used[1]))):
            dct["storageUsed"] = dictify(self.storage_used)
        if "storage_total" == "type" or (self.storage_total is not self.__undef__ and (not (dirty and not self._storage_total[1]))):
            dct["storageTotal"] = dictify(self.storage_total)
        if "installation_time" == "type" or (self.installation_time is not self.__undef__ and (not (dirty and not self._installation_time[1]))):
            dct["installationTime"] = dictify(self.installation_time)
        if "up_time" == "type" or (self.up_time is not self.__undef__ and (not (dirty and not self._up_time[1]))):
            dct["upTime"] = dictify(self.up_time)
        if "memory_reservation" == "type" or (self.memory_reservation is not self.__undef__ and (not (dirty and not self._memory_reservation[1]))):
            dct["memoryReservation"] = dictify(self.memory_reservation)
        if "cpu_reservation" == "type" or (self.cpu_reservation is not self.__undef__ and (not (dirty and not self._cpu_reservation[1]))):
            dct["cpuReservation"] = dictify(self.cpu_reservation)
        if "hotfixes" == "type" or (self.hotfixes is not self.__undef__ and (not (dirty and not self._hotfixes[1]))):
            dct["hotfixes"] = dictify(self.hotfixes)
        if "pool_fragmentation" == "type" or (self.pool_fragmentation is not self.__undef__ and (not (dirty and not self._pool_fragmentation[1]))):
            dct["poolFragmentation"] = dictify(self.pool_fragmentation)
        if "smtp_configured" == "type" or (self.smtp_configured is not self.__undef__ and (not (dirty and not self._smtp_configured[1]))):
            dct["smtpConfigured"] = dictify(self.smtp_configured)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._hostname = (self._hostname[0], True)
        self._max_heap_size_gb = (self._max_heap_size_gb[0], True)
        self._max_native_memory_gb = (self._max_native_memory_gb[0], True)
        self._ssh_public_key = (self._ssh_public_key[0], True)
        self._memory_size = (self._memory_size[0], True)
        self._platform = (self._platform[0], True)
        self._cloud_region = (self._cloud_region[0], True)
        self._uuid = (self._uuid[0], True)
        self._processors = (self._processors[0], True)
        self._storage_used = (self._storage_used[0], True)
        self._storage_total = (self._storage_total[0], True)
        self._installation_time = (self._installation_time[0], True)
        self._up_time = (self._up_time[0], True)
        self._memory_reservation = (self._memory_reservation[0], True)
        self._cpu_reservation = (self._cpu_reservation[0], True)
        self._hotfixes = (self._hotfixes[0], True)
        self._pool_fragmentation = (self._pool_fragmentation[0], True)
        self._smtp_configured = (self._smtp_configured[0], True)

    def is_dirty(self):
        return any([self._hostname[1], self._max_heap_size_gb[1], self._max_native_memory_gb[1], self._ssh_public_key[1], self._memory_size[1], self._platform[1], self._cloud_region[1], self._uuid[1], self._processors[1], self._storage_used[1], self._storage_total[1], self._installation_time[1], self._up_time[1], self._memory_reservation[1], self._cpu_reservation[1], self._hotfixes[1], self._pool_fragmentation[1], self._smtp_configured[1]])

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
        if not isinstance(other, SystemInfo):
            return False
        return super().__eq__(other) and \
               self.hostname == other.hostname and \
               self.max_heap_size_gb == other.max_heap_size_gb and \
               self.max_native_memory_gb == other.max_native_memory_gb and \
               self.ssh_public_key == other.ssh_public_key and \
               self.memory_size == other.memory_size and \
               self.platform == other.platform and \
               self.cloud_region == other.cloud_region and \
               self.uuid == other.uuid and \
               self.processors == other.processors and \
               self.storage_used == other.storage_used and \
               self.storage_total == other.storage_total and \
               self.installation_time == other.installation_time and \
               self.up_time == other.up_time and \
               self.memory_reservation == other.memory_reservation and \
               self.cpu_reservation == other.cpu_reservation and \
               self.hotfixes == other.hotfixes and \
               self.pool_fragmentation == other.pool_fragmentation and \
               self.smtp_configured == other.smtp_configured

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def hostname(self):
        """
        System hostname.

        :rtype: ``str``
        """
        return self._hostname[0]

    @hostname.setter
    def hostname(self, value):
        self._hostname = (value, True)

    @property
    def max_heap_size_gb(self):
        """
        Maximum heap size of the management application.

        :rtype: ``int``
        """
        return self._max_heap_size_gb[0]

    @max_heap_size_gb.setter
    def max_heap_size_gb(self, value):
        self._max_heap_size_gb = (value, True)

    @property
    def max_native_memory_gb(self):
        """
        Maximum native memory of the management application.

        :rtype: ``int``
        """
        return self._max_native_memory_gb[0]

    @max_native_memory_gb.setter
    def max_native_memory_gb(self, value):
        self._max_native_memory_gb = (value, True)

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

    @property
    def memory_size(self):
        """
        Total memory on the system, in bytes.

        :rtype: ``float``
        """
        return self._memory_size[0]

    @memory_size.setter
    def memory_size(self, value):
        self._memory_size = (value, True)

    @property
    def platform(self):
        """
        Description of the current system platform.

        :rtype: ``str``
        """
        return self._platform[0]

    @platform.setter
    def platform(self, value):
        self._platform = (value, True)

    @property
    def cloud_region(self):
        """
        The region of the current system if hosted on an applicable cloud
        service provider.

        :rtype: ``str``
        """
        return self._cloud_region[0]

    @cloud_region.setter
    def cloud_region(self, value):
        self._cloud_region = (value, True)

    @property
    def uuid(self):
        """
        Globally unique identifier for this software installation.

        :rtype: ``str``
        """
        return self._uuid[0]

    @uuid.setter
    def uuid(self, value):
        self._uuid = (value, True)

    @property
    def processors(self):
        """
        Processors on the system.

        :rtype: ``list`` of :py:class:`v1_11_37.web.vo.CPUInfo`
        """
        return self._processors[0]

    @processors.setter
    def processors(self, value):
        self._processors = (value, True)

    @property
    def storage_used(self):
        """
        Amount of raw storage used by dSources, VDBs and system metadata.

        :rtype: ``float``
        """
        return self._storage_used[0]

    @storage_used.setter
    def storage_used(self, value):
        self._storage_used = (value, True)

    @property
    def storage_total(self):
        """
        Total amount of raw storage allocated for dSources, VDBs, and system
        metadata. Zero if storage has not yet been configured.

        :rtype: ``float``
        """
        return self._storage_total[0]

    @storage_total.setter
    def storage_total(self, value):
        self._storage_total = (value, True)

    @property
    def installation_time(self):
        """
        The date and time that the Delphix Engine was installed.

        :rtype: ``str``
        """
        return self._installation_time[0]

    @installation_time.setter
    def installation_time(self, value):
        self._installation_time = (value, True)

    @property
    def up_time(self):
        """
        Delphix Engine up time.

        :rtype: :py:class:`v1_11_37.web.vo.UpTimeInfo`
        """
        return self._up_time[0]

    @up_time.setter
    def up_time(self, value):
        self._up_time = (value, True)

    @property
    def memory_reservation(self):
        """
        Amount of memory reserved on the host.

        :rtype: ``float``
        """
        return self._memory_reservation[0]

    @memory_reservation.setter
    def memory_reservation(self, value):
        self._memory_reservation = (value, True)

    @property
    def cpu_reservation(self):
        """
        Percentage of CPU reserved on the host.

        :rtype: ``float``
        """
        return self._cpu_reservation[0]

    @cpu_reservation.setter
    def cpu_reservation(self, value):
        self._cpu_reservation = (value, True)

    @property
    def hotfixes(self):
        """
        List of hotfixes that were applied to this host.

        :rtype: ``str``
        """
        return self._hotfixes[0]

    @hotfixes.setter
    def hotfixes(self, value):
        self._hotfixes = (value, True)

    @property
    def pool_fragmentation(self):
        """
        Percent fragmentation for the domain0 pool.

        :rtype: ``float``
        """
        return self._pool_fragmentation[0]

    @pool_fragmentation.setter
    def pool_fragmentation(self, value):
        self._pool_fragmentation = (value, True)

    @property
    def smtp_configured(self):
        """
        Whether SMTP has been configured.

        :rtype: ``bool``
        """
        return self._smtp_configured[0]

    @smtp_configured.setter
    def smtp_configured(self, value):
        self._smtp_configured = (value, True)

