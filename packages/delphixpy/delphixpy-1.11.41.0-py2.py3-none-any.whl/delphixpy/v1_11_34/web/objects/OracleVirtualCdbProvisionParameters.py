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
#     /delphix-oracle-virtual-cdb-provision-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_34 import factory
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleVirtualCdbProvisionParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_34.web.vo.TypedObject` *)* The parameters to
    use as input to provision Oracle virtual container databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleVirtualCdbProvisionParameters", True)
        self._container = (self.__undef__, True)
        self._source = (self.__undef__, True)
        self._source_config = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "container" not in data:
            raise ValueError("Missing required property \"container\".")
        if "container" in data and data["container"] is not None:
            obj._container = (factory.create_object(data["container"], "OracleDatabaseContainer"), dirty)
            factory.validate_type(obj._container[0], "OracleDatabaseContainer")
        else:
            obj._container = (obj.__undef__, dirty)
        if "source" not in data:
            raise ValueError("Missing required property \"source\".")
        if "source" in data and data["source"] is not None:
            obj._source = (factory.create_object(data["source"], "OracleVirtualCdbSource"), dirty)
            factory.validate_type(obj._source[0], "OracleVirtualCdbSource")
        else:
            obj._source = (obj.__undef__, dirty)
        if "sourceConfig" not in data:
            raise ValueError("Missing required property \"sourceConfig\".")
        if "sourceConfig" in data and data["sourceConfig"] is not None:
            obj._source_config = (factory.create_object(data["sourceConfig"], "OracleDBConfig"), dirty)
            factory.validate_type(obj._source_config[0], "OracleDBConfig")
        else:
            obj._source_config = (obj.__undef__, dirty)
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
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]) or self.is_dirty_list(self.container, self._container) or belongs_to_parent)):
            dct["container"] = dictify(self.container, prop_is_list_or_vo=True)
        if "source" == "type" or (self.source is not self.__undef__ and (not (dirty and not self._source[1]) or self.is_dirty_list(self.source, self._source) or belongs_to_parent)):
            dct["source"] = dictify(self.source, prop_is_list_or_vo=True)
        if "source_config" == "type" or (self.source_config is not self.__undef__ and (not (dirty and not self._source_config[1]) or self.is_dirty_list(self.source_config, self._source_config) or belongs_to_parent)):
            dct["sourceConfig"] = dictify(self.source_config, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._container = (self._container[0], True)
        self._source = (self._source[0], True)
        self._source_config = (self._source_config[0], True)

    def is_dirty(self):
        return any([self._container[1], self._source[1], self._source_config[1]])

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
        if not isinstance(other, OracleVirtualCdbProvisionParameters):
            return False
        return super().__eq__(other) and \
               self.container == other.container and \
               self.source == other.source and \
               self.source_config == other.source_config

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def container(self):
        """
        The new container for the created database.

        :rtype: :py:class:`v1_11_34.web.vo.OracleDatabaseContainer`
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def source(self):
        """
        The source that describes an external database instance.

        :rtype: :py:class:`v1_11_34.web.vo.OracleVirtualCdbSource`
        """
        return self._source[0]

    @source.setter
    def source(self, value):
        self._source = (value, True)

    @property
    def source_config(self):
        """
        The source config including dynamically discovered attributes of the
        source.

        :rtype: :py:class:`v1_11_34.web.vo.OracleDBConfig`
        """
        return self._source_config[0]

    @source_config.setter
    def source_config(self, value):
        self._source_config = (value, True)

