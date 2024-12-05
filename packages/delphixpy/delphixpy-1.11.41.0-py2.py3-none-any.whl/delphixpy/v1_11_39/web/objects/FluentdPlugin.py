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
#     /delphix-fluentd-plugin.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.UserObject import UserObject
from delphixpy.v1_11_39 import factory
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class FluentdPlugin(UserObject):
    """
    *(extends* :py:class:`v1_11_39.web.vo.UserObject` *)* Upload and manage
    fluentd plugins.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("FluentdPlugin", True)
        self._plugin = (self.__undef__, True)
        self._attribute_definitions = (self.__undef__, True)
        self._schema_definition = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._plugin = (data.get("plugin", obj.__undef__), dirty)
        if obj._plugin[0] is not None and obj._plugin[0] is not obj.__undef__:
            assert isinstance(obj._plugin[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._plugin[0], type(obj._plugin[0])))
            common.validate_format(obj._plugin[0], "None", None, None)
        obj._attribute_definitions = []
        for item in data.get("attributeDefinitions") or []:
            obj._attribute_definitions.append(factory.create_object(item))
            factory.validate_type(obj._attribute_definitions[-1], "FluentdAttributeDefinition")
        obj._attribute_definitions = (obj._attribute_definitions, dirty)
        if "schemaDefinition" in data and data["schemaDefinition"] is not None:
            obj._schema_definition = (data["schemaDefinition"], dirty)
        else:
            obj._schema_definition = (obj.__undef__, dirty)
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
        if "plugin" == "type" or (self.plugin is not self.__undef__ and (not (dirty and not self._plugin[1]))):
            dct["plugin"] = dictify(self.plugin)
        if "attribute_definitions" == "type" or (self.attribute_definitions is not self.__undef__ and (not (dirty and not self._attribute_definitions[1]))):
            dct["attributeDefinitions"] = dictify(self.attribute_definitions)
        if "schema_definition" == "type" or (self.schema_definition is not self.__undef__ and (not (dirty and not self._schema_definition[1]))):
            dct["schemaDefinition"] = dictify(self.schema_definition)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._plugin = (self._plugin[0], True)
        self._attribute_definitions = (self._attribute_definitions[0], True)
        self._schema_definition = (self._schema_definition[0], True)

    def is_dirty(self):
        return any([self._plugin[1], self._attribute_definitions[1], self._schema_definition[1]])

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
        if not isinstance(other, FluentdPlugin):
            return False
        return super().__eq__(other) and \
               self.plugin == other.plugin and \
               self.attribute_definitions == other.attribute_definitions and \
               self.schema_definition == other.schema_definition

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def plugin(self):
        """
        Name of the fluentd plugin.

        :rtype: ``str``
        """
        return self._plugin[0]

    @plugin.setter
    def plugin(self, value):
        self._plugin = (value, True)

    @property
    def attribute_definitions(self):
        """
        A list of the attribute definitions needed for configuration.

        :rtype: ``list`` of
            :py:class:`v1_11_39.web.vo.FluentdAttributeDefinition`
        """
        return self._attribute_definitions[0]

    @attribute_definitions.setter
    def attribute_definitions(self, value):
        self._attribute_definitions = (value, True)

    @property
    def schema_definition(self):
        """
        A schema definition generated with attribute names and their types. The
        type is taken string by default.

        :rtype: :py:class:`v1_11_39.web.vo.SchemaDraftV4`
        """
        return self._schema_definition[0]

    @schema_definition.setter
    def schema_definition(self, value):
        self._schema_definition = (value, True)

