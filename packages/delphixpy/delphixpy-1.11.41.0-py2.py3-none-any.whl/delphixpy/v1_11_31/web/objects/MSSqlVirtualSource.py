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
#     /delphix-mssql-virtual-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_31.web.objects.MSSqlSource import MSSqlSource
from delphixpy.v1_11_31 import factory
from delphixpy.v1_11_31 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlVirtualSource(MSSqlSource):
    """
    *(extends* :py:class:`v1_11_31.web.vo.MSSqlSource` *)* A virtual MSSQL
    source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlVirtualSource", True)
        self._pre_script = (self.__undef__, True)
        self._post_script = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._mount_base = (self.__undef__, True)
        self._file_mapping_rules = (self.__undef__, True)
        self._config_template = (self.__undef__, True)
        self._config_params = (self.__undef__, True)
        self._allow_auto_vdb_restart_on_host_reboot = (self.__undef__, True)
        self._enable_cdc_on_provision = (self.__undef__, True)
        self._config = (self.__undef__, True)
        self._ag_provision_config = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._pre_script = (data.get("preScript", obj.__undef__), dirty)
        if obj._pre_script[0] is not None and obj._pre_script[0] is not obj.__undef__:
            assert isinstance(obj._pre_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pre_script[0], type(obj._pre_script[0])))
            common.validate_format(obj._pre_script[0], "None", None, 256)
        obj._post_script = (data.get("postScript", obj.__undef__), dirty)
        if obj._post_script[0] is not None and obj._post_script[0] is not obj.__undef__:
            assert isinstance(obj._post_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._post_script[0], type(obj._post_script[0])))
            common.validate_format(obj._post_script[0], "None", None, 256)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "VirtualSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "VirtualSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        obj._mount_base = (data.get("mountBase", obj.__undef__), dirty)
        if obj._mount_base[0] is not None and obj._mount_base[0] is not obj.__undef__:
            assert isinstance(obj._mount_base[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_base[0], type(obj._mount_base[0])))
            common.validate_format(obj._mount_base[0], "None", None, 256)
        obj._file_mapping_rules = (data.get("fileMappingRules", obj.__undef__), dirty)
        if obj._file_mapping_rules[0] is not None and obj._file_mapping_rules[0] is not obj.__undef__:
            assert isinstance(obj._file_mapping_rules[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._file_mapping_rules[0], type(obj._file_mapping_rules[0])))
            common.validate_format(obj._file_mapping_rules[0], "None", None, None)
        obj._config_template = (data.get("configTemplate", obj.__undef__), dirty)
        if obj._config_template[0] is not None and obj._config_template[0] is not obj.__undef__:
            assert isinstance(obj._config_template[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._config_template[0], type(obj._config_template[0])))
            common.validate_format(obj._config_template[0], "objectReference", None, None)
        obj._config_params = (data.get("configParams", obj.__undef__), dirty)
        if obj._config_params[0] is not None and obj._config_params[0] is not obj.__undef__:
            assert isinstance(obj._config_params[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._config_params[0], type(obj._config_params[0])))
            common.validate_format(obj._config_params[0], "None", None, None)
        obj._allow_auto_vdb_restart_on_host_reboot = (data.get("allowAutoVDBRestartOnHostReboot", obj.__undef__), dirty)
        if obj._allow_auto_vdb_restart_on_host_reboot[0] is not None and obj._allow_auto_vdb_restart_on_host_reboot[0] is not obj.__undef__:
            assert isinstance(obj._allow_auto_vdb_restart_on_host_reboot[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._allow_auto_vdb_restart_on_host_reboot[0], type(obj._allow_auto_vdb_restart_on_host_reboot[0])))
            common.validate_format(obj._allow_auto_vdb_restart_on_host_reboot[0], "None", None, None)
        obj._enable_cdc_on_provision = (data.get("enableCdcOnProvision", obj.__undef__), dirty)
        if obj._enable_cdc_on_provision[0] is not None and obj._enable_cdc_on_provision[0] is not obj.__undef__:
            assert isinstance(obj._enable_cdc_on_provision[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enable_cdc_on_provision[0], type(obj._enable_cdc_on_provision[0])))
            common.validate_format(obj._enable_cdc_on_provision[0], "None", None, None)
        obj._config = (data.get("config", obj.__undef__), dirty)
        if obj._config[0] is not None and obj._config[0] is not obj.__undef__:
            assert isinstance(obj._config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config[0], type(obj._config[0])))
            common.validate_format(obj._config[0], "objectReference", None, None)
        if "agProvisionConfig" in data and data["agProvisionConfig"] is not None:
            obj._ag_provision_config = (factory.create_object(data["agProvisionConfig"], "MSSqlAGProvisionConfig"), dirty)
            factory.validate_type(obj._ag_provision_config[0], "MSSqlAGProvisionConfig")
        else:
            obj._ag_provision_config = (obj.__undef__, dirty)
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
        if "pre_script" == "type" or (self.pre_script is not self.__undef__ and (not (dirty and not self._pre_script[1]) or self.is_dirty_list(self.pre_script, self._pre_script) or belongs_to_parent)):
            dct["preScript"] = dictify(self.pre_script)
        if "post_script" == "type" or (self.post_script is not self.__undef__ and (not (dirty and not self._post_script[1]) or self.is_dirty_list(self.post_script, self._post_script) or belongs_to_parent)):
            dct["postScript"] = dictify(self.post_script)
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "mount_base" == "type" or (self.mount_base is not self.__undef__ and (not (dirty and not self._mount_base[1]))):
            dct["mountBase"] = dictify(self.mount_base)
        if "file_mapping_rules" == "type" or (self.file_mapping_rules is not self.__undef__ and (not (dirty and not self._file_mapping_rules[1]) or self.is_dirty_list(self.file_mapping_rules, self._file_mapping_rules) or belongs_to_parent)):
            dct["fileMappingRules"] = dictify(self.file_mapping_rules)
        if "config_template" == "type" or (self.config_template is not self.__undef__ and (not (dirty and not self._config_template[1]) or self.is_dirty_list(self.config_template, self._config_template) or belongs_to_parent)):
            dct["configTemplate"] = dictify(self.config_template)
        if "config_params" == "type" or (self.config_params is not self.__undef__ and (not (dirty and not self._config_params[1]) or self.is_dirty_list(self.config_params, self._config_params) or belongs_to_parent)):
            dct["configParams"] = dictify(self.config_params, prop_is_list_or_vo=True)
        if "allow_auto_vdb_restart_on_host_reboot" == "type" or (self.allow_auto_vdb_restart_on_host_reboot is not self.__undef__ and (not (dirty and not self._allow_auto_vdb_restart_on_host_reboot[1]) or self.is_dirty_list(self.allow_auto_vdb_restart_on_host_reboot, self._allow_auto_vdb_restart_on_host_reboot) or belongs_to_parent)):
            dct["allowAutoVDBRestartOnHostReboot"] = dictify(self.allow_auto_vdb_restart_on_host_reboot)
        elif belongs_to_parent and self.allow_auto_vdb_restart_on_host_reboot is self.__undef__:
            dct["allowAutoVDBRestartOnHostReboot"] = True
        if "enable_cdc_on_provision" == "type" or (self.enable_cdc_on_provision is not self.__undef__ and (not (dirty and not self._enable_cdc_on_provision[1]) or self.is_dirty_list(self.enable_cdc_on_provision, self._enable_cdc_on_provision) or belongs_to_parent)):
            dct["enableCdcOnProvision"] = dictify(self.enable_cdc_on_provision)
        elif belongs_to_parent and self.enable_cdc_on_provision is self.__undef__:
            dct["enableCdcOnProvision"] = False
        if "config" == "type" or (self.config is not self.__undef__ and (not (dirty and not self._config[1]) or self.is_dirty_list(self.config, self._config) or belongs_to_parent)):
            dct["config"] = dictify(self.config)
        if "ag_provision_config" == "type" or (self.ag_provision_config is not self.__undef__ and (not (dirty and not self._ag_provision_config[1]) or self.is_dirty_list(self.ag_provision_config, self._ag_provision_config) or belongs_to_parent)):
            dct["agProvisionConfig"] = dictify(self.ag_provision_config)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._pre_script = (self._pre_script[0], True)
        self._post_script = (self._post_script[0], True)
        self._operations = (self._operations[0], True)
        self._mount_base = (self._mount_base[0], True)
        self._file_mapping_rules = (self._file_mapping_rules[0], True)
        self._config_template = (self._config_template[0], True)
        self._config_params = (self._config_params[0], True)
        self._allow_auto_vdb_restart_on_host_reboot = (self._allow_auto_vdb_restart_on_host_reboot[0], True)
        self._enable_cdc_on_provision = (self._enable_cdc_on_provision[0], True)
        self._config = (self._config[0], True)
        self._ag_provision_config = (self._ag_provision_config[0], True)

    def is_dirty(self):
        return any([self._pre_script[1], self._post_script[1], self._operations[1], self._mount_base[1], self._file_mapping_rules[1], self._config_template[1], self._config_params[1], self._allow_auto_vdb_restart_on_host_reboot[1], self._enable_cdc_on_provision[1], self._config[1], self._ag_provision_config[1]])

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
        if not isinstance(other, MSSqlVirtualSource):
            return False
        return super().__eq__(other) and \
               self.pre_script == other.pre_script and \
               self.post_script == other.post_script and \
               self.operations == other.operations and \
               self.mount_base == other.mount_base and \
               self.file_mapping_rules == other.file_mapping_rules and \
               self.config_template == other.config_template and \
               self.config_params == other.config_params and \
               self.allow_auto_vdb_restart_on_host_reboot == other.allow_auto_vdb_restart_on_host_reboot and \
               self.enable_cdc_on_provision == other.enable_cdc_on_provision and \
               self.config == other.config and \
               self.ag_provision_config == other.ag_provision_config

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def pre_script(self):
        """
        A user-provided PowerShell script or executable to run prior to
        provisioning.

        :rtype: ``str``
        """
        return self._pre_script[0]

    @pre_script.setter
    def pre_script(self, value):
        self._pre_script = (value, True)

    @property
    def post_script(self):
        """
        A user-provided PowerShell script or executable to run after
        provisioning.

        :rtype: ``str``
        """
        return self._post_script[0]

    @post_script.setter
    def post_script(self, value):
        self._post_script = (value, True)

    @property
    def operations(self):
        """
        User-specified operation hooks for this source.

        :rtype: :py:class:`v1_11_31.web.vo.VirtualSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

    @property
    def mount_base(self):
        """
        The base mount point for the iSCSI LUN mounts.

        :rtype: ``str``
        """
        return self._mount_base[0]

    @mount_base.setter
    def mount_base(self, value):
        self._mount_base = (value, True)

    @property
    def file_mapping_rules(self):
        """
        Database file mapping rules.

        :rtype: ``str``
        """
        return self._file_mapping_rules[0]

    @file_mapping_rules.setter
    def file_mapping_rules(self, value):
        self._file_mapping_rules = (value, True)

    @property
    def config_template(self):
        """
        Optional database template to use for provisioning, refresh and enable.
        If set, configParams will be ignored on provision or refresh.

        :rtype: ``str`` *or* ``null``
        """
        return self._config_template[0]

    @config_template.setter
    def config_template(self, value):
        self._config_template = (value, True)

    @property
    def config_params(self):
        """
        MSSQL database configuration parameter overrides.

        :rtype: ``dict``
        """
        return self._config_params[0]

    @config_params.setter
    def config_params(self, value):
        self._config_params = (value, True)

    @property
    def allow_auto_vdb_restart_on_host_reboot(self):
        """
        *(default value: True)* Indicates whether Delphix should automatically
        restart this virtual source when target host reboot is detected.

        :rtype: ``bool``
        """
        return self._allow_auto_vdb_restart_on_host_reboot[0]

    @allow_auto_vdb_restart_on_host_reboot.setter
    def allow_auto_vdb_restart_on_host_reboot(self, value):
        self._allow_auto_vdb_restart_on_host_reboot = (value, True)

    @property
    def enable_cdc_on_provision(self):
        """
        Indicates whether to enable CDC on VDB while provisioning and also
        whether to enable CDC or not for subsequent snapshot related
        operations(like refresh, rewind) on the VDB.

        :rtype: ``bool``
        """
        return self._enable_cdc_on_provision[0]

    @enable_cdc_on_provision.setter
    def enable_cdc_on_provision(self, value):
        self._enable_cdc_on_provision = (value, True)

    @property
    def config(self):
        """
        Reference to the configuration for the source.

        :rtype: ``str``
        """
        return self._config[0]

    @config.setter
    def config(self, value):
        self._config = (value, True)

    @property
    def ag_provision_config(self):
        """
        AG provision configuration.

        :rtype: :py:class:`v1_11_31.web.vo.MSSqlAGProvisionConfig`
        """
        return self._ag_provision_config[0]

    @ag_provision_config.setter
    def ag_provision_config(self, value):
        self._ag_provision_config = (value, True)

