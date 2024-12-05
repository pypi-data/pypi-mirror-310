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
#     /delphix-plugin-discovery-definition.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PluginDiscoveryDefinition(TypedObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.TypedObject` *)* Defines the
    discovery schemas for a plugin.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PluginDiscoveryDefinition", True)
        self._repository_schema = (self.__undef__, True)
        self._repository_identity_fields = (self.__undef__, True)
        self._repository_name_field = (self.__undef__, True)
        self._source_config_schema = (self.__undef__, True)
        self._source_config_identity_fields = (self.__undef__, True)
        self._source_config_name_field = (self.__undef__, True)
        self._manual_source_config_discovery = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "repositorySchema" not in data:
            raise ValueError("Missing required property \"repositorySchema\".")
        if "repositorySchema" in data and data["repositorySchema"] is not None:
            obj._repository_schema = (data["repositorySchema"], dirty)
        else:
            obj._repository_schema = (obj.__undef__, dirty)
        if "repositoryIdentityFields" not in data:
            raise ValueError("Missing required property \"repositoryIdentityFields\".")
        obj._repository_identity_fields = []
        for item in data.get("repositoryIdentityFields") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._repository_identity_fields.append(item)
        obj._repository_identity_fields = (obj._repository_identity_fields, dirty)
        if "repositoryNameField" not in data:
            raise ValueError("Missing required property \"repositoryNameField\".")
        obj._repository_name_field = (data.get("repositoryNameField", obj.__undef__), dirty)
        if obj._repository_name_field[0] is not None and obj._repository_name_field[0] is not obj.__undef__:
            assert isinstance(obj._repository_name_field[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._repository_name_field[0], type(obj._repository_name_field[0])))
            common.validate_format(obj._repository_name_field[0], "None", None, None)
        if "sourceConfigSchema" not in data:
            raise ValueError("Missing required property \"sourceConfigSchema\".")
        if "sourceConfigSchema" in data and data["sourceConfigSchema"] is not None:
            obj._source_config_schema = (data["sourceConfigSchema"], dirty)
        else:
            obj._source_config_schema = (obj.__undef__, dirty)
        if "sourceConfigIdentityFields" not in data:
            raise ValueError("Missing required property \"sourceConfigIdentityFields\".")
        obj._source_config_identity_fields = []
        for item in data.get("sourceConfigIdentityFields") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._source_config_identity_fields.append(item)
        obj._source_config_identity_fields = (obj._source_config_identity_fields, dirty)
        if "sourceConfigNameField" not in data:
            raise ValueError("Missing required property \"sourceConfigNameField\".")
        obj._source_config_name_field = (data.get("sourceConfigNameField", obj.__undef__), dirty)
        if obj._source_config_name_field[0] is not None and obj._source_config_name_field[0] is not obj.__undef__:
            assert isinstance(obj._source_config_name_field[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source_config_name_field[0], type(obj._source_config_name_field[0])))
            common.validate_format(obj._source_config_name_field[0], "None", None, None)
        obj._manual_source_config_discovery = (data.get("manualSourceConfigDiscovery", obj.__undef__), dirty)
        if obj._manual_source_config_discovery[0] is not None and obj._manual_source_config_discovery[0] is not obj.__undef__:
            assert isinstance(obj._manual_source_config_discovery[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._manual_source_config_discovery[0], type(obj._manual_source_config_discovery[0])))
            common.validate_format(obj._manual_source_config_discovery[0], "None", None, None)
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
        if "repository_schema" == "type" or (self.repository_schema is not self.__undef__ and (not (dirty and not self._repository_schema[1]) or self.is_dirty_list(self.repository_schema, self._repository_schema) or belongs_to_parent)):
            dct["repositorySchema"] = dictify(self.repository_schema, prop_is_list_or_vo=True)
        if "repository_identity_fields" == "type" or (self.repository_identity_fields is not self.__undef__ and (not (dirty and not self._repository_identity_fields[1]) or self.is_dirty_list(self.repository_identity_fields, self._repository_identity_fields) or belongs_to_parent)):
            dct["repositoryIdentityFields"] = dictify(self.repository_identity_fields, prop_is_list_or_vo=True)
        if "repository_name_field" == "type" or (self.repository_name_field is not self.__undef__ and (not (dirty and not self._repository_name_field[1]) or self.is_dirty_list(self.repository_name_field, self._repository_name_field) or belongs_to_parent)):
            dct["repositoryNameField"] = dictify(self.repository_name_field)
        if "source_config_schema" == "type" or (self.source_config_schema is not self.__undef__ and (not (dirty and not self._source_config_schema[1]) or self.is_dirty_list(self.source_config_schema, self._source_config_schema) or belongs_to_parent)):
            dct["sourceConfigSchema"] = dictify(self.source_config_schema, prop_is_list_or_vo=True)
        if "source_config_identity_fields" == "type" or (self.source_config_identity_fields is not self.__undef__ and (not (dirty and not self._source_config_identity_fields[1]) or self.is_dirty_list(self.source_config_identity_fields, self._source_config_identity_fields) or belongs_to_parent)):
            dct["sourceConfigIdentityFields"] = dictify(self.source_config_identity_fields, prop_is_list_or_vo=True)
        if "source_config_name_field" == "type" or (self.source_config_name_field is not self.__undef__ and (not (dirty and not self._source_config_name_field[1]) or self.is_dirty_list(self.source_config_name_field, self._source_config_name_field) or belongs_to_parent)):
            dct["sourceConfigNameField"] = dictify(self.source_config_name_field)
        if "manual_source_config_discovery" == "type" or (self.manual_source_config_discovery is not self.__undef__ and (not (dirty and not self._manual_source_config_discovery[1]))):
            dct["manualSourceConfigDiscovery"] = dictify(self.manual_source_config_discovery)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._repository_schema = (self._repository_schema[0], True)
        self._repository_identity_fields = (self._repository_identity_fields[0], True)
        self._repository_name_field = (self._repository_name_field[0], True)
        self._source_config_schema = (self._source_config_schema[0], True)
        self._source_config_identity_fields = (self._source_config_identity_fields[0], True)
        self._source_config_name_field = (self._source_config_name_field[0], True)
        self._manual_source_config_discovery = (self._manual_source_config_discovery[0], True)

    def is_dirty(self):
        return any([self._repository_schema[1], self._repository_identity_fields[1], self._repository_name_field[1], self._source_config_schema[1], self._source_config_identity_fields[1], self._source_config_name_field[1], self._manual_source_config_discovery[1]])

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
        if not isinstance(other, PluginDiscoveryDefinition):
            return False
        return super().__eq__(other) and \
               self.repository_schema == other.repository_schema and \
               self.repository_identity_fields == other.repository_identity_fields and \
               self.repository_name_field == other.repository_name_field and \
               self.source_config_schema == other.source_config_schema and \
               self.source_config_identity_fields == other.source_config_identity_fields and \
               self.source_config_name_field == other.source_config_name_field and \
               self.manual_source_config_discovery == other.manual_source_config_discovery

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def repository_schema(self):
        """
        A user defined schema to represent the repository.

        :rtype: :py:class:`v1_11_20.web.vo.SchemaDraftV4`
        """
        return self._repository_schema[0]

    @repository_schema.setter
    def repository_schema(self, value):
        self._repository_schema = (value, True)

    @property
    def repository_identity_fields(self):
        """
        A list of fields in the repositorySchema that collectively identify
        each discovered repository.

        :rtype: ``list`` of ``str``
        """
        return self._repository_identity_fields[0]

    @repository_identity_fields.setter
    def repository_identity_fields(self, value):
        self._repository_identity_fields = (value, True)

    @property
    def repository_name_field(self):
        """
        The field of the repositorySchema to display to the end user for naming
        this repository.

        :rtype: ``str``
        """
        return self._repository_name_field[0]

    @repository_name_field.setter
    def repository_name_field(self, value):
        self._repository_name_field = (value, True)

    @property
    def source_config_schema(self):
        """
        A user defined schema to represent the source config.

        :rtype: :py:class:`v1_11_20.web.vo.SchemaDraftV4`
        """
        return self._source_config_schema[0]

    @source_config_schema.setter
    def source_config_schema(self, value):
        self._source_config_schema = (value, True)

    @property
    def source_config_identity_fields(self):
        """
        A list of fields in the sourceConfigSchema that collectively identify
        each discovered source config.

        :rtype: ``list`` of ``str``
        """
        return self._source_config_identity_fields[0]

    @source_config_identity_fields.setter
    def source_config_identity_fields(self, value):
        self._source_config_identity_fields = (value, True)

    @property
    def source_config_name_field(self):
        """
        The field of the sourceConfigSchema to display to the end user for
        naming this source config.

        :rtype: ``str``
        """
        return self._source_config_name_field[0]

    @source_config_name_field.setter
    def source_config_name_field(self, value):
        self._source_config_name_field = (value, True)

    @property
    def manual_source_config_discovery(self):
        """
        True if this plugin supports manual discovery of source configs.

        :rtype: ``bool``
        """
        return self._manual_source_config_discovery[0]

    @manual_source_config_discovery.setter
    def manual_source_config_discovery(self, value):
        self._manual_source_config_discovery = (value, True)

