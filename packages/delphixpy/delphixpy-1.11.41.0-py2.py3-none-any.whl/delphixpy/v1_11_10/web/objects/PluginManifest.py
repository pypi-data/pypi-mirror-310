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
#     /delphix-plugin-manifest.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_10.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_10 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PluginManifest(TypedObject):
    """
    *(extends* :py:class:`v1_11_10.web.vo.TypedObject` *)* A manifest
    describing a plugin.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PluginManifest", True)
        self._has_repository_discovery = (self.__undef__, True)
        self._has_source_config_discovery = (self.__undef__, True)
        self._has_linked_pre_snapshot = (self.__undef__, True)
        self._has_linked_post_snapshot = (self.__undef__, True)
        self._has_linked_start_staging = (self.__undef__, True)
        self._has_linked_stop_staging = (self.__undef__, True)
        self._has_linked_status = (self.__undef__, True)
        self._has_linked_worker = (self.__undef__, True)
        self._has_linked_mount_specification = (self.__undef__, True)
        self._has_virtual_configure = (self.__undef__, True)
        self._has_virtual_unconfigure = (self.__undef__, True)
        self._has_virtual_reconfigure = (self.__undef__, True)
        self._has_virtual_start = (self.__undef__, True)
        self._has_virtual_stop = (self.__undef__, True)
        self._has_virtual_pre_snapshot = (self.__undef__, True)
        self._has_virtual_post_snapshot = (self.__undef__, True)
        self._has_virtual_mount_specification = (self.__undef__, True)
        self._has_virtual_status = (self.__undef__, True)
        self._has_initialize = (self.__undef__, True)
        self._migration_id_list = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "hasRepositoryDiscovery" not in data:
            raise ValueError("Missing required property \"hasRepositoryDiscovery\".")
        obj._has_repository_discovery = (data.get("hasRepositoryDiscovery", obj.__undef__), dirty)
        if obj._has_repository_discovery[0] is not None and obj._has_repository_discovery[0] is not obj.__undef__:
            assert isinstance(obj._has_repository_discovery[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_repository_discovery[0], type(obj._has_repository_discovery[0])))
            common.validate_format(obj._has_repository_discovery[0], "None", None, None)
        if "hasSourceConfigDiscovery" not in data:
            raise ValueError("Missing required property \"hasSourceConfigDiscovery\".")
        obj._has_source_config_discovery = (data.get("hasSourceConfigDiscovery", obj.__undef__), dirty)
        if obj._has_source_config_discovery[0] is not None and obj._has_source_config_discovery[0] is not obj.__undef__:
            assert isinstance(obj._has_source_config_discovery[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_source_config_discovery[0], type(obj._has_source_config_discovery[0])))
            common.validate_format(obj._has_source_config_discovery[0], "None", None, None)
        if "hasLinkedPreSnapshot" not in data:
            raise ValueError("Missing required property \"hasLinkedPreSnapshot\".")
        obj._has_linked_pre_snapshot = (data.get("hasLinkedPreSnapshot", obj.__undef__), dirty)
        if obj._has_linked_pre_snapshot[0] is not None and obj._has_linked_pre_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_pre_snapshot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_pre_snapshot[0], type(obj._has_linked_pre_snapshot[0])))
            common.validate_format(obj._has_linked_pre_snapshot[0], "None", None, None)
        if "hasLinkedPostSnapshot" not in data:
            raise ValueError("Missing required property \"hasLinkedPostSnapshot\".")
        obj._has_linked_post_snapshot = (data.get("hasLinkedPostSnapshot", obj.__undef__), dirty)
        if obj._has_linked_post_snapshot[0] is not None and obj._has_linked_post_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_post_snapshot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_post_snapshot[0], type(obj._has_linked_post_snapshot[0])))
            common.validate_format(obj._has_linked_post_snapshot[0], "None", None, None)
        if "hasLinkedStartStaging" not in data:
            raise ValueError("Missing required property \"hasLinkedStartStaging\".")
        obj._has_linked_start_staging = (data.get("hasLinkedStartStaging", obj.__undef__), dirty)
        if obj._has_linked_start_staging[0] is not None and obj._has_linked_start_staging[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_start_staging[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_start_staging[0], type(obj._has_linked_start_staging[0])))
            common.validate_format(obj._has_linked_start_staging[0], "None", None, None)
        if "hasLinkedStopStaging" not in data:
            raise ValueError("Missing required property \"hasLinkedStopStaging\".")
        obj._has_linked_stop_staging = (data.get("hasLinkedStopStaging", obj.__undef__), dirty)
        if obj._has_linked_stop_staging[0] is not None and obj._has_linked_stop_staging[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_stop_staging[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_stop_staging[0], type(obj._has_linked_stop_staging[0])))
            common.validate_format(obj._has_linked_stop_staging[0], "None", None, None)
        if "hasLinkedStatus" not in data:
            raise ValueError("Missing required property \"hasLinkedStatus\".")
        obj._has_linked_status = (data.get("hasLinkedStatus", obj.__undef__), dirty)
        if obj._has_linked_status[0] is not None and obj._has_linked_status[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_status[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_status[0], type(obj._has_linked_status[0])))
            common.validate_format(obj._has_linked_status[0], "None", None, None)
        if "hasLinkedWorker" not in data:
            raise ValueError("Missing required property \"hasLinkedWorker\".")
        obj._has_linked_worker = (data.get("hasLinkedWorker", obj.__undef__), dirty)
        if obj._has_linked_worker[0] is not None and obj._has_linked_worker[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_worker[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_worker[0], type(obj._has_linked_worker[0])))
            common.validate_format(obj._has_linked_worker[0], "None", None, None)
        if "hasLinkedMountSpecification" not in data:
            raise ValueError("Missing required property \"hasLinkedMountSpecification\".")
        obj._has_linked_mount_specification = (data.get("hasLinkedMountSpecification", obj.__undef__), dirty)
        if obj._has_linked_mount_specification[0] is not None and obj._has_linked_mount_specification[0] is not obj.__undef__:
            assert isinstance(obj._has_linked_mount_specification[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_linked_mount_specification[0], type(obj._has_linked_mount_specification[0])))
            common.validate_format(obj._has_linked_mount_specification[0], "None", None, None)
        if "hasVirtualConfigure" not in data:
            raise ValueError("Missing required property \"hasVirtualConfigure\".")
        obj._has_virtual_configure = (data.get("hasVirtualConfigure", obj.__undef__), dirty)
        if obj._has_virtual_configure[0] is not None and obj._has_virtual_configure[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_configure[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_configure[0], type(obj._has_virtual_configure[0])))
            common.validate_format(obj._has_virtual_configure[0], "None", None, None)
        if "hasVirtualUnconfigure" not in data:
            raise ValueError("Missing required property \"hasVirtualUnconfigure\".")
        obj._has_virtual_unconfigure = (data.get("hasVirtualUnconfigure", obj.__undef__), dirty)
        if obj._has_virtual_unconfigure[0] is not None and obj._has_virtual_unconfigure[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_unconfigure[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_unconfigure[0], type(obj._has_virtual_unconfigure[0])))
            common.validate_format(obj._has_virtual_unconfigure[0], "None", None, None)
        if "hasVirtualReconfigure" not in data:
            raise ValueError("Missing required property \"hasVirtualReconfigure\".")
        obj._has_virtual_reconfigure = (data.get("hasVirtualReconfigure", obj.__undef__), dirty)
        if obj._has_virtual_reconfigure[0] is not None and obj._has_virtual_reconfigure[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_reconfigure[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_reconfigure[0], type(obj._has_virtual_reconfigure[0])))
            common.validate_format(obj._has_virtual_reconfigure[0], "None", None, None)
        if "hasVirtualStart" not in data:
            raise ValueError("Missing required property \"hasVirtualStart\".")
        obj._has_virtual_start = (data.get("hasVirtualStart", obj.__undef__), dirty)
        if obj._has_virtual_start[0] is not None and obj._has_virtual_start[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_start[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_start[0], type(obj._has_virtual_start[0])))
            common.validate_format(obj._has_virtual_start[0], "None", None, None)
        if "hasVirtualStop" not in data:
            raise ValueError("Missing required property \"hasVirtualStop\".")
        obj._has_virtual_stop = (data.get("hasVirtualStop", obj.__undef__), dirty)
        if obj._has_virtual_stop[0] is not None and obj._has_virtual_stop[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_stop[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_stop[0], type(obj._has_virtual_stop[0])))
            common.validate_format(obj._has_virtual_stop[0], "None", None, None)
        if "hasVirtualPreSnapshot" not in data:
            raise ValueError("Missing required property \"hasVirtualPreSnapshot\".")
        obj._has_virtual_pre_snapshot = (data.get("hasVirtualPreSnapshot", obj.__undef__), dirty)
        if obj._has_virtual_pre_snapshot[0] is not None and obj._has_virtual_pre_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_pre_snapshot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_pre_snapshot[0], type(obj._has_virtual_pre_snapshot[0])))
            common.validate_format(obj._has_virtual_pre_snapshot[0], "None", None, None)
        if "hasVirtualPostSnapshot" not in data:
            raise ValueError("Missing required property \"hasVirtualPostSnapshot\".")
        obj._has_virtual_post_snapshot = (data.get("hasVirtualPostSnapshot", obj.__undef__), dirty)
        if obj._has_virtual_post_snapshot[0] is not None and obj._has_virtual_post_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_post_snapshot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_post_snapshot[0], type(obj._has_virtual_post_snapshot[0])))
            common.validate_format(obj._has_virtual_post_snapshot[0], "None", None, None)
        if "hasVirtualMountSpecification" not in data:
            raise ValueError("Missing required property \"hasVirtualMountSpecification\".")
        obj._has_virtual_mount_specification = (data.get("hasVirtualMountSpecification", obj.__undef__), dirty)
        if obj._has_virtual_mount_specification[0] is not None and obj._has_virtual_mount_specification[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_mount_specification[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_mount_specification[0], type(obj._has_virtual_mount_specification[0])))
            common.validate_format(obj._has_virtual_mount_specification[0], "None", None, None)
        if "hasVirtualStatus" not in data:
            raise ValueError("Missing required property \"hasVirtualStatus\".")
        obj._has_virtual_status = (data.get("hasVirtualStatus", obj.__undef__), dirty)
        if obj._has_virtual_status[0] is not None and obj._has_virtual_status[0] is not obj.__undef__:
            assert isinstance(obj._has_virtual_status[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_virtual_status[0], type(obj._has_virtual_status[0])))
            common.validate_format(obj._has_virtual_status[0], "None", None, None)
        if "hasInitialize" not in data:
            raise ValueError("Missing required property \"hasInitialize\".")
        obj._has_initialize = (data.get("hasInitialize", obj.__undef__), dirty)
        if obj._has_initialize[0] is not None and obj._has_initialize[0] is not obj.__undef__:
            assert isinstance(obj._has_initialize[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._has_initialize[0], type(obj._has_initialize[0])))
            common.validate_format(obj._has_initialize[0], "None", None, None)
        obj._migration_id_list = []
        for item in data.get("migrationIdList") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "dotDecimal", None, None)
            obj._migration_id_list.append(item)
        obj._migration_id_list = (obj._migration_id_list, dirty)
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
        if "has_repository_discovery" == "type" or (self.has_repository_discovery is not self.__undef__ and (not (dirty and not self._has_repository_discovery[1]) or self.is_dirty_list(self.has_repository_discovery, self._has_repository_discovery) or belongs_to_parent)):
            dct["hasRepositoryDiscovery"] = dictify(self.has_repository_discovery)
        if "has_source_config_discovery" == "type" or (self.has_source_config_discovery is not self.__undef__ and (not (dirty and not self._has_source_config_discovery[1]) or self.is_dirty_list(self.has_source_config_discovery, self._has_source_config_discovery) or belongs_to_parent)):
            dct["hasSourceConfigDiscovery"] = dictify(self.has_source_config_discovery)
        if "has_linked_pre_snapshot" == "type" or (self.has_linked_pre_snapshot is not self.__undef__ and (not (dirty and not self._has_linked_pre_snapshot[1]) or self.is_dirty_list(self.has_linked_pre_snapshot, self._has_linked_pre_snapshot) or belongs_to_parent)):
            dct["hasLinkedPreSnapshot"] = dictify(self.has_linked_pre_snapshot)
        if "has_linked_post_snapshot" == "type" or (self.has_linked_post_snapshot is not self.__undef__ and (not (dirty and not self._has_linked_post_snapshot[1]) or self.is_dirty_list(self.has_linked_post_snapshot, self._has_linked_post_snapshot) or belongs_to_parent)):
            dct["hasLinkedPostSnapshot"] = dictify(self.has_linked_post_snapshot)
        if "has_linked_start_staging" == "type" or (self.has_linked_start_staging is not self.__undef__ and (not (dirty and not self._has_linked_start_staging[1]) or self.is_dirty_list(self.has_linked_start_staging, self._has_linked_start_staging) or belongs_to_parent)):
            dct["hasLinkedStartStaging"] = dictify(self.has_linked_start_staging)
        if "has_linked_stop_staging" == "type" or (self.has_linked_stop_staging is not self.__undef__ and (not (dirty and not self._has_linked_stop_staging[1]) or self.is_dirty_list(self.has_linked_stop_staging, self._has_linked_stop_staging) or belongs_to_parent)):
            dct["hasLinkedStopStaging"] = dictify(self.has_linked_stop_staging)
        if "has_linked_status" == "type" or (self.has_linked_status is not self.__undef__ and (not (dirty and not self._has_linked_status[1]) or self.is_dirty_list(self.has_linked_status, self._has_linked_status) or belongs_to_parent)):
            dct["hasLinkedStatus"] = dictify(self.has_linked_status)
        if "has_linked_worker" == "type" or (self.has_linked_worker is not self.__undef__ and (not (dirty and not self._has_linked_worker[1]) or self.is_dirty_list(self.has_linked_worker, self._has_linked_worker) or belongs_to_parent)):
            dct["hasLinkedWorker"] = dictify(self.has_linked_worker)
        if "has_linked_mount_specification" == "type" or (self.has_linked_mount_specification is not self.__undef__ and (not (dirty and not self._has_linked_mount_specification[1]) or self.is_dirty_list(self.has_linked_mount_specification, self._has_linked_mount_specification) or belongs_to_parent)):
            dct["hasLinkedMountSpecification"] = dictify(self.has_linked_mount_specification)
        if "has_virtual_configure" == "type" or (self.has_virtual_configure is not self.__undef__ and (not (dirty and not self._has_virtual_configure[1]) or self.is_dirty_list(self.has_virtual_configure, self._has_virtual_configure) or belongs_to_parent)):
            dct["hasVirtualConfigure"] = dictify(self.has_virtual_configure)
        if "has_virtual_unconfigure" == "type" or (self.has_virtual_unconfigure is not self.__undef__ and (not (dirty and not self._has_virtual_unconfigure[1]) or self.is_dirty_list(self.has_virtual_unconfigure, self._has_virtual_unconfigure) or belongs_to_parent)):
            dct["hasVirtualUnconfigure"] = dictify(self.has_virtual_unconfigure)
        if "has_virtual_reconfigure" == "type" or (self.has_virtual_reconfigure is not self.__undef__ and (not (dirty and not self._has_virtual_reconfigure[1]) or self.is_dirty_list(self.has_virtual_reconfigure, self._has_virtual_reconfigure) or belongs_to_parent)):
            dct["hasVirtualReconfigure"] = dictify(self.has_virtual_reconfigure)
        if "has_virtual_start" == "type" or (self.has_virtual_start is not self.__undef__ and (not (dirty and not self._has_virtual_start[1]) or self.is_dirty_list(self.has_virtual_start, self._has_virtual_start) or belongs_to_parent)):
            dct["hasVirtualStart"] = dictify(self.has_virtual_start)
        if "has_virtual_stop" == "type" or (self.has_virtual_stop is not self.__undef__ and (not (dirty and not self._has_virtual_stop[1]) or self.is_dirty_list(self.has_virtual_stop, self._has_virtual_stop) or belongs_to_parent)):
            dct["hasVirtualStop"] = dictify(self.has_virtual_stop)
        if "has_virtual_pre_snapshot" == "type" or (self.has_virtual_pre_snapshot is not self.__undef__ and (not (dirty and not self._has_virtual_pre_snapshot[1]) or self.is_dirty_list(self.has_virtual_pre_snapshot, self._has_virtual_pre_snapshot) or belongs_to_parent)):
            dct["hasVirtualPreSnapshot"] = dictify(self.has_virtual_pre_snapshot)
        if "has_virtual_post_snapshot" == "type" or (self.has_virtual_post_snapshot is not self.__undef__ and (not (dirty and not self._has_virtual_post_snapshot[1]) or self.is_dirty_list(self.has_virtual_post_snapshot, self._has_virtual_post_snapshot) or belongs_to_parent)):
            dct["hasVirtualPostSnapshot"] = dictify(self.has_virtual_post_snapshot)
        if "has_virtual_mount_specification" == "type" or (self.has_virtual_mount_specification is not self.__undef__ and (not (dirty and not self._has_virtual_mount_specification[1]) or self.is_dirty_list(self.has_virtual_mount_specification, self._has_virtual_mount_specification) or belongs_to_parent)):
            dct["hasVirtualMountSpecification"] = dictify(self.has_virtual_mount_specification)
        if "has_virtual_status" == "type" or (self.has_virtual_status is not self.__undef__ and (not (dirty and not self._has_virtual_status[1]) or self.is_dirty_list(self.has_virtual_status, self._has_virtual_status) or belongs_to_parent)):
            dct["hasVirtualStatus"] = dictify(self.has_virtual_status)
        if "has_initialize" == "type" or (self.has_initialize is not self.__undef__ and (not (dirty and not self._has_initialize[1]) or self.is_dirty_list(self.has_initialize, self._has_initialize) or belongs_to_parent)):
            dct["hasInitialize"] = dictify(self.has_initialize)
        if "migration_id_list" == "type" or (self.migration_id_list is not self.__undef__ and (not (dirty and not self._migration_id_list[1]))):
            dct["migrationIdList"] = dictify(self.migration_id_list)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._has_repository_discovery = (self._has_repository_discovery[0], True)
        self._has_source_config_discovery = (self._has_source_config_discovery[0], True)
        self._has_linked_pre_snapshot = (self._has_linked_pre_snapshot[0], True)
        self._has_linked_post_snapshot = (self._has_linked_post_snapshot[0], True)
        self._has_linked_start_staging = (self._has_linked_start_staging[0], True)
        self._has_linked_stop_staging = (self._has_linked_stop_staging[0], True)
        self._has_linked_status = (self._has_linked_status[0], True)
        self._has_linked_worker = (self._has_linked_worker[0], True)
        self._has_linked_mount_specification = (self._has_linked_mount_specification[0], True)
        self._has_virtual_configure = (self._has_virtual_configure[0], True)
        self._has_virtual_unconfigure = (self._has_virtual_unconfigure[0], True)
        self._has_virtual_reconfigure = (self._has_virtual_reconfigure[0], True)
        self._has_virtual_start = (self._has_virtual_start[0], True)
        self._has_virtual_stop = (self._has_virtual_stop[0], True)
        self._has_virtual_pre_snapshot = (self._has_virtual_pre_snapshot[0], True)
        self._has_virtual_post_snapshot = (self._has_virtual_post_snapshot[0], True)
        self._has_virtual_mount_specification = (self._has_virtual_mount_specification[0], True)
        self._has_virtual_status = (self._has_virtual_status[0], True)
        self._has_initialize = (self._has_initialize[0], True)
        self._migration_id_list = (self._migration_id_list[0], True)

    def is_dirty(self):
        return any([self._has_repository_discovery[1], self._has_source_config_discovery[1], self._has_linked_pre_snapshot[1], self._has_linked_post_snapshot[1], self._has_linked_start_staging[1], self._has_linked_stop_staging[1], self._has_linked_status[1], self._has_linked_worker[1], self._has_linked_mount_specification[1], self._has_virtual_configure[1], self._has_virtual_unconfigure[1], self._has_virtual_reconfigure[1], self._has_virtual_start[1], self._has_virtual_stop[1], self._has_virtual_pre_snapshot[1], self._has_virtual_post_snapshot[1], self._has_virtual_mount_specification[1], self._has_virtual_status[1], self._has_initialize[1], self._migration_id_list[1]])

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
        if not isinstance(other, PluginManifest):
            return False
        return super().__eq__(other) and \
               self.has_repository_discovery == other.has_repository_discovery and \
               self.has_source_config_discovery == other.has_source_config_discovery and \
               self.has_linked_pre_snapshot == other.has_linked_pre_snapshot and \
               self.has_linked_post_snapshot == other.has_linked_post_snapshot and \
               self.has_linked_start_staging == other.has_linked_start_staging and \
               self.has_linked_stop_staging == other.has_linked_stop_staging and \
               self.has_linked_status == other.has_linked_status and \
               self.has_linked_worker == other.has_linked_worker and \
               self.has_linked_mount_specification == other.has_linked_mount_specification and \
               self.has_virtual_configure == other.has_virtual_configure and \
               self.has_virtual_unconfigure == other.has_virtual_unconfigure and \
               self.has_virtual_reconfigure == other.has_virtual_reconfigure and \
               self.has_virtual_start == other.has_virtual_start and \
               self.has_virtual_stop == other.has_virtual_stop and \
               self.has_virtual_pre_snapshot == other.has_virtual_pre_snapshot and \
               self.has_virtual_post_snapshot == other.has_virtual_post_snapshot and \
               self.has_virtual_mount_specification == other.has_virtual_mount_specification and \
               self.has_virtual_status == other.has_virtual_status and \
               self.has_initialize == other.has_initialize and \
               self.migration_id_list == other.migration_id_list

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def has_repository_discovery(self):
        """
        Indicates whether discovery.repository() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_repository_discovery[0]

    @has_repository_discovery.setter
    def has_repository_discovery(self, value):
        self._has_repository_discovery = (value, True)

    @property
    def has_source_config_discovery(self):
        """
        Indicates whether discovery.source_config() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_source_config_discovery[0]

    @has_source_config_discovery.setter
    def has_source_config_discovery(self, value):
        self._has_source_config_discovery = (value, True)

    @property
    def has_linked_pre_snapshot(self):
        """
        Indicates whether linked.pre_snapshot() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_linked_pre_snapshot[0]

    @has_linked_pre_snapshot.setter
    def has_linked_pre_snapshot(self, value):
        self._has_linked_pre_snapshot = (value, True)

    @property
    def has_linked_post_snapshot(self):
        """
        Indicates whether linked.post_snapshot() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_linked_post_snapshot[0]

    @has_linked_post_snapshot.setter
    def has_linked_post_snapshot(self, value):
        self._has_linked_post_snapshot = (value, True)

    @property
    def has_linked_start_staging(self):
        """
        Indicates whether linked.start_staging() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_linked_start_staging[0]

    @has_linked_start_staging.setter
    def has_linked_start_staging(self, value):
        self._has_linked_start_staging = (value, True)

    @property
    def has_linked_stop_staging(self):
        """
        Indicates whether linked.stop_staging() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_linked_stop_staging[0]

    @has_linked_stop_staging.setter
    def has_linked_stop_staging(self, value):
        self._has_linked_stop_staging = (value, True)

    @property
    def has_linked_status(self):
        """
        Indicates whether linked.status() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_linked_status[0]

    @has_linked_status.setter
    def has_linked_status(self, value):
        self._has_linked_status = (value, True)

    @property
    def has_linked_worker(self):
        """
        Indicates whether linked.worker() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_linked_worker[0]

    @has_linked_worker.setter
    def has_linked_worker(self, value):
        self._has_linked_worker = (value, True)

    @property
    def has_linked_mount_specification(self):
        """
        Indicates whether linked.mount_specification() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_linked_mount_specification[0]

    @has_linked_mount_specification.setter
    def has_linked_mount_specification(self, value):
        self._has_linked_mount_specification = (value, True)

    @property
    def has_virtual_configure(self):
        """
        Indicates whether virtual.configure() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_configure[0]

    @has_virtual_configure.setter
    def has_virtual_configure(self, value):
        self._has_virtual_configure = (value, True)

    @property
    def has_virtual_unconfigure(self):
        """
        Indicates whether virtual.unconfigure() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_unconfigure[0]

    @has_virtual_unconfigure.setter
    def has_virtual_unconfigure(self, value):
        self._has_virtual_unconfigure = (value, True)

    @property
    def has_virtual_reconfigure(self):
        """
        Indicates whether virtual.reconfigure() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_reconfigure[0]

    @has_virtual_reconfigure.setter
    def has_virtual_reconfigure(self, value):
        self._has_virtual_reconfigure = (value, True)

    @property
    def has_virtual_start(self):
        """
        Indicates whether virtual.start() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_start[0]

    @has_virtual_start.setter
    def has_virtual_start(self, value):
        self._has_virtual_start = (value, True)

    @property
    def has_virtual_stop(self):
        """
        Indicates whether virtual.stop() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_stop[0]

    @has_virtual_stop.setter
    def has_virtual_stop(self, value):
        self._has_virtual_stop = (value, True)

    @property
    def has_virtual_pre_snapshot(self):
        """
        Indicates whether virtual.pre_snapshot() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_pre_snapshot[0]

    @has_virtual_pre_snapshot.setter
    def has_virtual_pre_snapshot(self, value):
        self._has_virtual_pre_snapshot = (value, True)

    @property
    def has_virtual_post_snapshot(self):
        """
        Indicates whether virtual.post_snapshot() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_post_snapshot[0]

    @has_virtual_post_snapshot.setter
    def has_virtual_post_snapshot(self, value):
        self._has_virtual_post_snapshot = (value, True)

    @property
    def has_virtual_mount_specification(self):
        """
        Indicates whether virtual.mount_specification() operation has been
        implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_mount_specification[0]

    @has_virtual_mount_specification.setter
    def has_virtual_mount_specification(self, value):
        self._has_virtual_mount_specification = (value, True)

    @property
    def has_virtual_status(self):
        """
        Indicates whether virtual.status() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_virtual_status[0]

    @has_virtual_status.setter
    def has_virtual_status(self, value):
        self._has_virtual_status = (value, True)

    @property
    def has_initialize(self):
        """
        Indicates whether virtual.initialize() operation has been implemented.

        :rtype: ``bool``
        """
        return self._has_initialize[0]

    @has_initialize.setter
    def has_initialize(self, value):
        self._has_initialize = (value, True)

    @property
    def migration_id_list(self):
        """
        The list of migration IDs that exist in this plugin.

        :rtype: ``list`` of ``str``
        """
        return self._migration_id_list[0]

    @migration_id_list.setter
    def migration_id_list(self, value):
        self._migration_id_list = (value, True)

