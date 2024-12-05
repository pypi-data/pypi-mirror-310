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
#     /delphix-appdata-source-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.SourceConfig import SourceConfig
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AppDataSourceConfig(SourceConfig):
    """
    *(extends* :py:class:`v1_11_38.web.vo.SourceConfig` *)* Base Source config
    for AppDataToolkits.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AppDataSourceConfig", True)
        self._toolkit = (self.__undef__, True)
        self._name = (self.__undef__, True)
        self._repository = (self.__undef__, True)
        self._parameters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._toolkit = (data.get("toolkit", obj.__undef__), dirty)
        if obj._toolkit[0] is not None and obj._toolkit[0] is not obj.__undef__:
            assert isinstance(obj._toolkit[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._toolkit[0], type(obj._toolkit[0])))
            common.validate_format(obj._toolkit[0], "objectReference", None, None)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, 256)
        obj._repository = (data.get("repository", obj.__undef__), dirty)
        if obj._repository[0] is not None and obj._repository[0] is not obj.__undef__:
            assert isinstance(obj._repository[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._repository[0], type(obj._repository[0])))
            common.validate_format(obj._repository[0], "objectReference", None, None)
        if "parameters" in data and data["parameters"] is not None:
            obj._parameters = (data["parameters"], dirty)
        else:
            obj._parameters = (obj.__undef__, dirty)
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
        if "toolkit" == "type" or (self.toolkit is not self.__undef__ and (not (dirty and not self._toolkit[1]))):
            dct["toolkit"] = dictify(self.toolkit)
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "repository" == "type" or (self.repository is not self.__undef__ and (not (dirty and not self._repository[1]) or self.is_dirty_list(self.repository, self._repository) or belongs_to_parent)):
            dct["repository"] = dictify(self.repository)
        if "parameters" == "type" or (self.parameters is not self.__undef__ and (not (dirty and not self._parameters[1]) or self.is_dirty_list(self.parameters, self._parameters) or belongs_to_parent)):
            dct["parameters"] = dictify(self.parameters, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._toolkit = (self._toolkit[0], True)
        self._name = (self._name[0], True)
        self._repository = (self._repository[0], True)
        self._parameters = (self._parameters[0], True)

    def is_dirty(self):
        return any([self._toolkit[1], self._name[1], self._repository[1], self._parameters[1]])

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
        if not isinstance(other, AppDataSourceConfig):
            return False
        return super().__eq__(other) and \
               self.toolkit == other.toolkit and \
               self.name == other.name and \
               self.repository == other.repository and \
               self.parameters == other.parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def toolkit(self):
        """
        The toolkit associated with this source config.

        :rtype: ``str``
        """
        return self._toolkit[0]

    @toolkit.setter
    def toolkit(self, value):
        self._toolkit = (value, True)

    @property
    def name(self):
        """
        The name of the config.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def repository(self):
        """
        The object reference of the source repository.

        :rtype: ``str``
        """
        return self._repository[0]

    @repository.setter
    def repository(self, value):
        self._repository = (value, True)

    @property
    def parameters(self):
        """
        The list of parameters specified by the source config schema in the
        toolkit. If no schema is specified, this list is empty.

        :rtype: :py:class:`v1_11_38.web.vo.Json`
        """
        return self._parameters[0]

    @parameters.setter
    def parameters(self, value):
        self._parameters = (value, True)

