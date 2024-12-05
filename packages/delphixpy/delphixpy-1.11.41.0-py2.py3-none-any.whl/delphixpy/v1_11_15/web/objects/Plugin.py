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
#     /delphix-plugin.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_15.web.objects.AbstractToolkit import AbstractToolkit
from delphixpy.v1_11_15 import factory
from delphixpy.v1_11_15 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Plugin(AbstractToolkit):
    """
    *(extends* :py:class:`v1_11_15.web.vo.AbstractToolkit` *)* An installed
    plugin.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Plugin", True)
        self._plugin_id = (self.__undef__, True)
        self._language = (self.__undef__, True)
        self._name = (self.__undef__, True)
        self._external_version = (self.__undef__, True)
        self._build_number = (self.__undef__, True)
        self._extended_start_stop_hooks = (self.__undef__, True)
        self._virtual_source_definition = (self.__undef__, True)
        self._linked_source_definition = (self.__undef__, True)
        self._discovery_definition = (self.__undef__, True)
        self._snapshot_parameters_definition = (self.__undef__, True)
        self._upgrade_definition = (self.__undef__, True)
        self._entry_point = (self.__undef__, True)
        self._lua_name = (self.__undef__, True)
        self._minimum_lua_version = (self.__undef__, True)
        self._source_code = (self.__undef__, True)
        self._manifest = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "pluginId" not in data:
            raise ValueError("Missing required property \"pluginId\".")
        obj._plugin_id = (data.get("pluginId", obj.__undef__), dirty)
        if obj._plugin_id[0] is not None and obj._plugin_id[0] is not obj.__undef__:
            assert isinstance(obj._plugin_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._plugin_id[0], type(obj._plugin_id[0])))
            common.validate_format(obj._plugin_id[0], "None", None, 256)
        if "language" not in data:
            raise ValueError("Missing required property \"language\".")
        obj._language = (data.get("language", obj.__undef__), dirty)
        if obj._language[0] is not None and obj._language[0] is not obj.__undef__:
            assert isinstance(obj._language[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._language[0], type(obj._language[0])))
            assert obj._language[0] in ['PYTHON27', 'PYTHON38'], "Expected enum ['PYTHON27', 'PYTHON38'] but got %s" % obj._language[0]
            common.validate_format(obj._language[0], "None", None, None)
        if "name" not in data:
            raise ValueError("Missing required property \"name\".")
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, 256)
        obj._external_version = (data.get("externalVersion", obj.__undef__), dirty)
        if obj._external_version[0] is not None and obj._external_version[0] is not obj.__undef__:
            assert isinstance(obj._external_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._external_version[0], type(obj._external_version[0])))
            common.validate_format(obj._external_version[0], "None", None, None)
        if "buildNumber" not in data:
            raise ValueError("Missing required property \"buildNumber\".")
        obj._build_number = (data.get("buildNumber", obj.__undef__), dirty)
        if obj._build_number[0] is not None and obj._build_number[0] is not obj.__undef__:
            assert isinstance(obj._build_number[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._build_number[0], type(obj._build_number[0])))
            common.validate_format(obj._build_number[0], "dotDecimal", None, None)
        obj._extended_start_stop_hooks = (data.get("extendedStartStopHooks", obj.__undef__), dirty)
        if obj._extended_start_stop_hooks[0] is not None and obj._extended_start_stop_hooks[0] is not obj.__undef__:
            assert isinstance(obj._extended_start_stop_hooks[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._extended_start_stop_hooks[0], type(obj._extended_start_stop_hooks[0])))
            common.validate_format(obj._extended_start_stop_hooks[0], "None", None, None)
        if "virtualSourceDefinition" not in data:
            raise ValueError("Missing required property \"virtualSourceDefinition\".")
        if "virtualSourceDefinition" in data and data["virtualSourceDefinition"] is not None:
            obj._virtual_source_definition = (factory.create_object(data["virtualSourceDefinition"], "PluginVirtualSourceDefinition"), dirty)
            factory.validate_type(obj._virtual_source_definition[0], "PluginVirtualSourceDefinition")
        else:
            obj._virtual_source_definition = (obj.__undef__, dirty)
        if "linkedSourceDefinition" not in data:
            raise ValueError("Missing required property \"linkedSourceDefinition\".")
        if "linkedSourceDefinition" in data and data["linkedSourceDefinition"] is not None:
            obj._linked_source_definition = (factory.create_object(data["linkedSourceDefinition"], "PluginLinkedSourceDefinition"), dirty)
            factory.validate_type(obj._linked_source_definition[0], "PluginLinkedSourceDefinition")
        else:
            obj._linked_source_definition = (obj.__undef__, dirty)
        if "discoveryDefinition" not in data:
            raise ValueError("Missing required property \"discoveryDefinition\".")
        if "discoveryDefinition" in data and data["discoveryDefinition"] is not None:
            obj._discovery_definition = (factory.create_object(data["discoveryDefinition"], "PluginDiscoveryDefinition"), dirty)
            factory.validate_type(obj._discovery_definition[0], "PluginDiscoveryDefinition")
        else:
            obj._discovery_definition = (obj.__undef__, dirty)
        if "snapshotParametersDefinition" not in data:
            raise ValueError("Missing required property \"snapshotParametersDefinition\".")
        if "snapshotParametersDefinition" in data and data["snapshotParametersDefinition"] is not None:
            obj._snapshot_parameters_definition = (factory.create_object(data["snapshotParametersDefinition"], "PluginSnapshotParametersDefinition"), dirty)
            factory.validate_type(obj._snapshot_parameters_definition[0], "PluginSnapshotParametersDefinition")
        else:
            obj._snapshot_parameters_definition = (obj.__undef__, dirty)
        if "upgradeDefinition" in data and data["upgradeDefinition"] is not None:
            obj._upgrade_definition = (factory.create_object(data["upgradeDefinition"], "PluginUpgradeDefinition"), dirty)
            factory.validate_type(obj._upgrade_definition[0], "PluginUpgradeDefinition")
        else:
            obj._upgrade_definition = (obj.__undef__, dirty)
        if "entryPoint" not in data:
            raise ValueError("Missing required property \"entryPoint\".")
        obj._entry_point = (data.get("entryPoint", obj.__undef__), dirty)
        if obj._entry_point[0] is not None and obj._entry_point[0] is not obj.__undef__:
            assert isinstance(obj._entry_point[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._entry_point[0], type(obj._entry_point[0])))
            common.validate_format(obj._entry_point[0], "None", None, None)
        obj._lua_name = (data.get("luaName", obj.__undef__), dirty)
        if obj._lua_name[0] is not None and obj._lua_name[0] is not obj.__undef__:
            assert isinstance(obj._lua_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._lua_name[0], type(obj._lua_name[0])))
            common.validate_format(obj._lua_name[0], "None", None, 256)
        obj._minimum_lua_version = (data.get("minimumLuaVersion", obj.__undef__), dirty)
        if obj._minimum_lua_version[0] is not None and obj._minimum_lua_version[0] is not obj.__undef__:
            assert isinstance(obj._minimum_lua_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._minimum_lua_version[0], type(obj._minimum_lua_version[0])))
            common.validate_format(obj._minimum_lua_version[0], "None", None, None)
        if "sourceCode" not in data:
            raise ValueError("Missing required property \"sourceCode\".")
        obj._source_code = (data.get("sourceCode", obj.__undef__), dirty)
        if obj._source_code[0] is not None and obj._source_code[0] is not obj.__undef__:
            assert isinstance(obj._source_code[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source_code[0], type(obj._source_code[0])))
            common.validate_format(obj._source_code[0], "None", None, None)
        if "manifest" not in data:
            raise ValueError("Missing required property \"manifest\".")
        if "manifest" in data and data["manifest"] is not None:
            obj._manifest = (factory.create_object(data["manifest"], "PluginManifest"), dirty)
            factory.validate_type(obj._manifest[0], "PluginManifest")
        else:
            obj._manifest = (obj.__undef__, dirty)
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
        if "plugin_id" == "type" or (self.plugin_id is not self.__undef__ and (not (dirty and not self._plugin_id[1]) or self.is_dirty_list(self.plugin_id, self._plugin_id) or belongs_to_parent)):
            dct["pluginId"] = dictify(self.plugin_id)
        if "language" == "type" or (self.language is not self.__undef__ and (not (dirty and not self._language[1]) or self.is_dirty_list(self.language, self._language) or belongs_to_parent)):
            dct["language"] = dictify(self.language)
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "external_version" == "type" or (self.external_version is not self.__undef__ and (not (dirty and not self._external_version[1]))):
            dct["externalVersion"] = dictify(self.external_version)
        if "build_number" == "type" or (self.build_number is not self.__undef__ and (not (dirty and not self._build_number[1]) or self.is_dirty_list(self.build_number, self._build_number) or belongs_to_parent)):
            dct["buildNumber"] = dictify(self.build_number)
        if "extended_start_stop_hooks" == "type" or (self.extended_start_stop_hooks is not self.__undef__ and (not (dirty and not self._extended_start_stop_hooks[1]))):
            dct["extendedStartStopHooks"] = dictify(self.extended_start_stop_hooks)
        if "virtual_source_definition" == "type" or (self.virtual_source_definition is not self.__undef__ and (not (dirty and not self._virtual_source_definition[1]) or self.is_dirty_list(self.virtual_source_definition, self._virtual_source_definition) or belongs_to_parent)):
            dct["virtualSourceDefinition"] = dictify(self.virtual_source_definition, prop_is_list_or_vo=True)
        if "linked_source_definition" == "type" or (self.linked_source_definition is not self.__undef__ and (not (dirty and not self._linked_source_definition[1]) or self.is_dirty_list(self.linked_source_definition, self._linked_source_definition) or belongs_to_parent)):
            dct["linkedSourceDefinition"] = dictify(self.linked_source_definition, prop_is_list_or_vo=True)
        if "discovery_definition" == "type" or (self.discovery_definition is not self.__undef__ and (not (dirty and not self._discovery_definition[1]) or self.is_dirty_list(self.discovery_definition, self._discovery_definition) or belongs_to_parent)):
            dct["discoveryDefinition"] = dictify(self.discovery_definition, prop_is_list_or_vo=True)
        if "snapshot_parameters_definition" == "type" or (self.snapshot_parameters_definition is not self.__undef__ and (not (dirty and not self._snapshot_parameters_definition[1]) or self.is_dirty_list(self.snapshot_parameters_definition, self._snapshot_parameters_definition) or belongs_to_parent)):
            dct["snapshotParametersDefinition"] = dictify(self.snapshot_parameters_definition, prop_is_list_or_vo=True)
        if "upgrade_definition" == "type" or (self.upgrade_definition is not self.__undef__ and (not (dirty and not self._upgrade_definition[1]))):
            dct["upgradeDefinition"] = dictify(self.upgrade_definition)
        if "entry_point" == "type" or (self.entry_point is not self.__undef__ and (not (dirty and not self._entry_point[1]) or self.is_dirty_list(self.entry_point, self._entry_point) or belongs_to_parent)):
            dct["entryPoint"] = dictify(self.entry_point)
        if "lua_name" == "type" or (self.lua_name is not self.__undef__ and (not (dirty and not self._lua_name[1]))):
            dct["luaName"] = dictify(self.lua_name)
        if "minimum_lua_version" == "type" or (self.minimum_lua_version is not self.__undef__ and (not (dirty and not self._minimum_lua_version[1]))):
            dct["minimumLuaVersion"] = dictify(self.minimum_lua_version)
        if "source_code" == "type" or (self.source_code is not self.__undef__ and (not (dirty and not self._source_code[1]) or self.is_dirty_list(self.source_code, self._source_code) or belongs_to_parent)):
            dct["sourceCode"] = dictify(self.source_code)
        if "manifest" == "type" or (self.manifest is not self.__undef__ and (not (dirty and not self._manifest[1]) or self.is_dirty_list(self.manifest, self._manifest) or belongs_to_parent)):
            dct["manifest"] = dictify(self.manifest, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._plugin_id = (self._plugin_id[0], True)
        self._language = (self._language[0], True)
        self._name = (self._name[0], True)
        self._external_version = (self._external_version[0], True)
        self._build_number = (self._build_number[0], True)
        self._extended_start_stop_hooks = (self._extended_start_stop_hooks[0], True)
        self._virtual_source_definition = (self._virtual_source_definition[0], True)
        self._linked_source_definition = (self._linked_source_definition[0], True)
        self._discovery_definition = (self._discovery_definition[0], True)
        self._snapshot_parameters_definition = (self._snapshot_parameters_definition[0], True)
        self._upgrade_definition = (self._upgrade_definition[0], True)
        self._entry_point = (self._entry_point[0], True)
        self._lua_name = (self._lua_name[0], True)
        self._minimum_lua_version = (self._minimum_lua_version[0], True)
        self._source_code = (self._source_code[0], True)
        self._manifest = (self._manifest[0], True)

    def is_dirty(self):
        return any([self._plugin_id[1], self._language[1], self._name[1], self._external_version[1], self._build_number[1], self._extended_start_stop_hooks[1], self._virtual_source_definition[1], self._linked_source_definition[1], self._discovery_definition[1], self._snapshot_parameters_definition[1], self._upgrade_definition[1], self._entry_point[1], self._lua_name[1], self._minimum_lua_version[1], self._source_code[1], self._manifest[1]])

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
        if not isinstance(other, Plugin):
            return False
        return super().__eq__(other) and \
               self.plugin_id == other.plugin_id and \
               self.language == other.language and \
               self.name == other.name and \
               self.external_version == other.external_version and \
               self.build_number == other.build_number and \
               self.extended_start_stop_hooks == other.extended_start_stop_hooks and \
               self.virtual_source_definition == other.virtual_source_definition and \
               self.linked_source_definition == other.linked_source_definition and \
               self.discovery_definition == other.discovery_definition and \
               self.snapshot_parameters_definition == other.snapshot_parameters_definition and \
               self.upgrade_definition == other.upgrade_definition and \
               self.entry_point == other.entry_point and \
               self.lua_name == other.lua_name and \
               self.minimum_lua_version == other.minimum_lua_version and \
               self.source_code == other.source_code and \
               self.manifest == other.manifest

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def plugin_id(self):
        """
        The UUID for the plugin.

        :rtype: ``str``
        """
        return self._plugin_id[0]

    @plugin_id.setter
    def plugin_id(self, value):
        self._plugin_id = (value, True)

    @property
    def language(self):
        """
        Implementation language for workflows in this plugin. *(permitted
        values: PYTHON27, PYTHON38)*

        :rtype: ``str``
        """
        return self._language[0]

    @language.setter
    def language(self, value):
        self._language = (value, True)

    @property
    def name(self):
        """
        A human readable name for the toolkit.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def external_version(self):
        """
        The user-facing version of the plugin that can be any format. If not
        set, the build number will be used.

        :rtype: ``str``
        """
        return self._external_version[0]

    @external_version.setter
    def external_version(self, value):
        self._external_version = (value, True)

    @property
    def build_number(self):
        """
        The internal build number of the plugin used to determine if a version
        of the plugin should be accepted.

        :rtype: ``str``
        """
        return self._build_number[0]

    @build_number.setter
    def build_number(self, value):
        self._build_number = (value, True)

    @property
    def extended_start_stop_hooks(self):
        """
        Indicates whether user start/stop hooks should run when container is
        enabled/disabled.

        :rtype: ``bool``
        """
        return self._extended_start_stop_hooks[0]

    @extended_start_stop_hooks.setter
    def extended_start_stop_hooks(self, value):
        self._extended_start_stop_hooks = (value, True)

    @property
    def virtual_source_definition(self):
        """
        Definition of how to provision virtual sources of this type.

        :rtype: :py:class:`v1_11_15.web.vo.PluginVirtualSourceDefinition`
        """
        return self._virtual_source_definition[0]

    @virtual_source_definition.setter
    def virtual_source_definition(self, value):
        self._virtual_source_definition = (value, True)

    @property
    def linked_source_definition(self):
        """
        Definition of how to link sources of this type.

        :rtype: :py:class:`v1_11_15.web.vo.PluginLinkedSourceDefinition`
        """
        return self._linked_source_definition[0]

    @linked_source_definition.setter
    def linked_source_definition(self, value):
        self._linked_source_definition = (value, True)

    @property
    def discovery_definition(self):
        """
        Definition of how to discover sources of this type.

        :rtype: :py:class:`v1_11_15.web.vo.PluginDiscoveryDefinition`
        """
        return self._discovery_definition[0]

    @discovery_definition.setter
    def discovery_definition(self, value):
        self._discovery_definition = (value, True)

    @property
    def snapshot_parameters_definition(self):
        """
        The schema that defines the structure of the fields in
        AppDataSyncParameters.

        :rtype: :py:class:`v1_11_15.web.vo.PluginSnapshotParametersDefinition`
        """
        return self._snapshot_parameters_definition[0]

    @snapshot_parameters_definition.setter
    def snapshot_parameters_definition(self, value):
        self._snapshot_parameters_definition = (value, True)

    @property
    def upgrade_definition(self):
        """
        Definition of how to upgrade sources of this type.

        :rtype: :py:class:`v1_11_15.web.vo.PluginUpgradeDefinition`
        """
        return self._upgrade_definition[0]

    @upgrade_definition.setter
    def upgrade_definition(self, value):
        self._upgrade_definition = (value, True)

    @property
    def entry_point(self):
        """
        A fully qualified symbol that in the plugin's source code that is used
        to execute a plugin operation.

        :rtype: ``str``
        """
        return self._entry_point[0]

    @entry_point.setter
    def entry_point(self, value):
        self._entry_point = (value, True)

    @property
    def lua_name(self):
        """
        The name of the LUA toolkit that this plugin can upgrade.

        :rtype: ``str``
        """
        return self._lua_name[0]

    @lua_name.setter
    def lua_name(self, value):
        self._lua_name = (value, True)

    @property
    def minimum_lua_version(self):
        """
        The minimum version (in major.minor format) of a LUA toolkit that this
        plugin can upgrade.

        :rtype: ``str``
        """
        return self._minimum_lua_version[0]

    @minimum_lua_version.setter
    def minimum_lua_version(self, value):
        self._minimum_lua_version = (value, True)

    @property
    def source_code(self):
        """
        Source code for this plugin.

        :rtype: ``str``
        """
        return self._source_code[0]

    @source_code.setter
    def source_code(self, value):
        self._source_code = (value, True)

    @property
    def manifest(self):
        """
        A manifest describing the plugin.

        :rtype: :py:class:`v1_11_15.web.vo.PluginManifest`
        """
        return self._manifest[0]

    @manifest.setter
    def manifest(self, value):
        self._manifest = (value, True)

