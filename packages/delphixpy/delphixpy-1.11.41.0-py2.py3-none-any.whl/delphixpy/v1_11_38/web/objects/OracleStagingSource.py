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
#     /delphix-oracle-staging-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.OracleManagedSource import OracleManagedSource
from delphixpy.v1_11_38 import factory
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleStagingSource(OracleManagedSource):
    """
    *(extends* :py:class:`v1_11_38.web.vo.OracleManagedSource` *)* A staging
    Oracle source used for Delphix operations such as log collection and
    snapshot generation.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleStagingSource", True)
        self._locked = (self.__undef__, True)
        self._physical_standby = (self.__undef__, True)
        self._allow_auto_staging_restart_on_host_reboot = (self.__undef__, True)
        self._custom_env_vars = (self.__undef__, True)
        self._datafile_mount_path = (self.__undef__, True)
        self._archive_mount_path = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._locked = (data.get("locked", obj.__undef__), dirty)
        if obj._locked[0] is not None and obj._locked[0] is not obj.__undef__:
            assert isinstance(obj._locked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._locked[0], type(obj._locked[0])))
            common.validate_format(obj._locked[0], "None", None, None)
        obj._physical_standby = (data.get("physicalStandby", obj.__undef__), dirty)
        if obj._physical_standby[0] is not None and obj._physical_standby[0] is not obj.__undef__:
            assert isinstance(obj._physical_standby[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._physical_standby[0], type(obj._physical_standby[0])))
            common.validate_format(obj._physical_standby[0], "None", None, None)
        obj._allow_auto_staging_restart_on_host_reboot = (data.get("allowAutoStagingRestartOnHostReboot", obj.__undef__), dirty)
        if obj._allow_auto_staging_restart_on_host_reboot[0] is not None and obj._allow_auto_staging_restart_on_host_reboot[0] is not obj.__undef__:
            assert isinstance(obj._allow_auto_staging_restart_on_host_reboot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._allow_auto_staging_restart_on_host_reboot[0], type(obj._allow_auto_staging_restart_on_host_reboot[0])))
            common.validate_format(obj._allow_auto_staging_restart_on_host_reboot[0], "None", None, None)
        obj._custom_env_vars = []
        for item in data.get("customEnvVars") or []:
            obj._custom_env_vars.append(factory.create_object(item))
            factory.validate_type(obj._custom_env_vars[-1], "OracleCustomEnvVar")
        obj._custom_env_vars = (obj._custom_env_vars, dirty)
        obj._datafile_mount_path = (data.get("datafileMountPath", obj.__undef__), dirty)
        if obj._datafile_mount_path[0] is not None and obj._datafile_mount_path[0] is not obj.__undef__:
            assert isinstance(obj._datafile_mount_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._datafile_mount_path[0], type(obj._datafile_mount_path[0])))
            common.validate_format(obj._datafile_mount_path[0], "unixrestrictedpath", None, 256)
        obj._archive_mount_path = (data.get("archiveMountPath", obj.__undef__), dirty)
        if obj._archive_mount_path[0] is not None and obj._archive_mount_path[0] is not obj.__undef__:
            assert isinstance(obj._archive_mount_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._archive_mount_path[0], type(obj._archive_mount_path[0])))
            common.validate_format(obj._archive_mount_path[0], "unixrestrictedpath", None, 256)
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
        if "locked" == "type" or (self.locked is not self.__undef__ and (not (dirty and not self._locked[1]))):
            dct["locked"] = dictify(self.locked)
        if "physical_standby" == "type" or (self.physical_standby is not self.__undef__ and (not (dirty and not self._physical_standby[1]) or self.is_dirty_list(self.physical_standby, self._physical_standby) or belongs_to_parent)):
            dct["physicalStandby"] = dictify(self.physical_standby)
        if "allow_auto_staging_restart_on_host_reboot" == "type" or (self.allow_auto_staging_restart_on_host_reboot is not self.__undef__ and (not (dirty and not self._allow_auto_staging_restart_on_host_reboot[1]) or self.is_dirty_list(self.allow_auto_staging_restart_on_host_reboot, self._allow_auto_staging_restart_on_host_reboot) or belongs_to_parent)):
            dct["allowAutoStagingRestartOnHostReboot"] = dictify(self.allow_auto_staging_restart_on_host_reboot)
        if "custom_env_vars" == "type" or (self.custom_env_vars is not self.__undef__ and (not (dirty and not self._custom_env_vars[1]) or self.is_dirty_list(self.custom_env_vars, self._custom_env_vars) or belongs_to_parent)):
            dct["customEnvVars"] = dictify(self.custom_env_vars, prop_is_list_or_vo=True)
        if "datafile_mount_path" == "type" or (self.datafile_mount_path is not self.__undef__ and (not (dirty and not self._datafile_mount_path[1]))):
            dct["datafileMountPath"] = dictify(self.datafile_mount_path)
        if "archive_mount_path" == "type" or (self.archive_mount_path is not self.__undef__ and (not (dirty and not self._archive_mount_path[1]))):
            dct["archiveMountPath"] = dictify(self.archive_mount_path)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._locked = (self._locked[0], True)
        self._physical_standby = (self._physical_standby[0], True)
        self._allow_auto_staging_restart_on_host_reboot = (self._allow_auto_staging_restart_on_host_reboot[0], True)
        self._custom_env_vars = (self._custom_env_vars[0], True)
        self._datafile_mount_path = (self._datafile_mount_path[0], True)
        self._archive_mount_path = (self._archive_mount_path[0], True)

    def is_dirty(self):
        return any([self._locked[1], self._physical_standby[1], self._allow_auto_staging_restart_on_host_reboot[1], self._custom_env_vars[1], self._datafile_mount_path[1], self._archive_mount_path[1]])

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
        if not isinstance(other, OracleStagingSource):
            return False
        return super().__eq__(other) and \
               self.locked == other.locked and \
               self.physical_standby == other.physical_standby and \
               self.allow_auto_staging_restart_on_host_reboot == other.allow_auto_staging_restart_on_host_reboot and \
               self.custom_env_vars == other.custom_env_vars and \
               self.datafile_mount_path == other.datafile_mount_path and \
               self.archive_mount_path == other.archive_mount_path

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def locked(self):
        """
        Whether the source is protected from deletion and other data-losing
        actions.

        :rtype: ``bool``
        """
        return self._locked[0]

    @locked.setter
    def locked(self, value):
        self._locked = (value, True)

    @property
    def physical_standby(self):
        """
        Whether this staging database will be configured as a physical standby.

        :rtype: ``bool``
        """
        return self._physical_standby[0]

    @physical_standby.setter
    def physical_standby(self, value):
        self._physical_standby = (value, True)

    @property
    def allow_auto_staging_restart_on_host_reboot(self):
        """
        Indicates whether Delphix should automatically restart this staging
        source when target host reboot is detected.

        :rtype: ``bool``
        """
        return self._allow_auto_staging_restart_on_host_reboot[0]

    @allow_auto_staging_restart_on_host_reboot.setter
    def allow_auto_staging_restart_on_host_reboot(self, value):
        self._allow_auto_staging_restart_on_host_reboot = (value, True)

    @property
    def custom_env_vars(self):
        """
        Custom environment variables for Oracle databases.

        :rtype: ``list`` of :py:class:`v1_11_38.web.vo.OracleCustomEnvVar`
        """
        return self._custom_env_vars[0]

    @custom_env_vars.setter
    def custom_env_vars(self, value):
        self._custom_env_vars = (value, True)

    @property
    def datafile_mount_path(self):
        """
        The datafile mount point to use for the NFS mounts.

        :rtype: ``str``
        """
        return self._datafile_mount_path[0]

    @datafile_mount_path.setter
    def datafile_mount_path(self, value):
        self._datafile_mount_path = (value, True)

    @property
    def archive_mount_path(self):
        """
        The archive mount point to use for the NFS mounts.

        :rtype: ``str``
        """
        return self._archive_mount_path[0]

    @archive_mount_path.setter
    def archive_mount_path(self, value):
        self._archive_mount_path = (value, True)

