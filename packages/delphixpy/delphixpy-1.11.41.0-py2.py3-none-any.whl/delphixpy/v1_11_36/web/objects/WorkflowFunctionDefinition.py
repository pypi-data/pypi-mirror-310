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
#     /delphix-workflow-function-definition.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class WorkflowFunctionDefinition(TypedObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TypedObject` *)* The definition of a
    Workflow Function.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("WorkflowFunctionDefinition", True)
        self._name = (self.__undef__, True)
        self._input_schema = (self.__undef__, True)
        self._output_schema = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, None)
        if "inputSchema" in data and data["inputSchema"] is not None:
            obj._input_schema = (data["inputSchema"], dirty)
        else:
            obj._input_schema = (obj.__undef__, dirty)
        if "outputSchema" in data and data["outputSchema"] is not None:
            obj._output_schema = (data["outputSchema"], dirty)
        else:
            obj._output_schema = (obj.__undef__, dirty)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "input_schema" == "type" or (self.input_schema is not self.__undef__ and (not (dirty and not self._input_schema[1]) or self.is_dirty_list(self.input_schema, self._input_schema) or belongs_to_parent)):
            dct["inputSchema"] = dictify(self.input_schema, prop_is_list_or_vo=True)
        if "output_schema" == "type" or (self.output_schema is not self.__undef__ and (not (dirty and not self._output_schema[1]) or self.is_dirty_list(self.output_schema, self._output_schema) or belongs_to_parent)):
            dct["outputSchema"] = dictify(self.output_schema, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._input_schema = (self._input_schema[0], True)
        self._output_schema = (self._output_schema[0], True)

    def is_dirty(self):
        return any([self._name[1], self._input_schema[1], self._output_schema[1]])

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
        if not isinstance(other, WorkflowFunctionDefinition):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.input_schema == other.input_schema and \
               self.output_schema == other.output_schema

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        The name of this function.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def input_schema(self):
        """
        The input schema for this function according to DRAFTV4.

        :rtype: :py:class:`v1_11_36.web.vo.SchemaDraftV4`
        """
        return self._input_schema[0]

    @input_schema.setter
    def input_schema(self, value):
        self._input_schema = (value, True)

    @property
    def output_schema(self):
        """
        The output schema for this function according to DRAFTV4.

        :rtype: :py:class:`v1_11_36.web.vo.SchemaDraftV4`
        """
        return self._output_schema[0]

    @output_schema.setter
    def output_schema(self, value):
        self._output_schema = (value, True)

