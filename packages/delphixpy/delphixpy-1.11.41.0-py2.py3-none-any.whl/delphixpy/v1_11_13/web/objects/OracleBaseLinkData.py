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
#     /delphix-oracle-base-link-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_13.web.objects.LinkData import LinkData
from delphixpy.v1_11_13 import factory
from delphixpy.v1_11_13 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleBaseLinkData(LinkData):
    """
    *(extends* :py:class:`v1_11_13.web.vo.LinkData` *)* Represents common
    parameters to link all Oracle databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleBaseLinkData", True)
        self._sync_strategy = (self.__undef__, True)
        self._external_file_path = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._sourcing_policy = (self.__undef__, True)
        self._sync_parameters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "syncStrategy" in data and data["syncStrategy"] is not None:
            obj._sync_strategy = (factory.create_object(data["syncStrategy"], "OracleSyncStrategy"), dirty)
            factory.validate_type(obj._sync_strategy[0], "OracleSyncStrategy")
        else:
            obj._sync_strategy = (obj.__undef__, dirty)
        obj._external_file_path = (data.get("externalFilePath", obj.__undef__), dirty)
        if obj._external_file_path[0] is not None and obj._external_file_path[0] is not obj.__undef__:
            assert isinstance(obj._external_file_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._external_file_path[0], type(obj._external_file_path[0])))
            common.validate_format(obj._external_file_path[0], "None", None, 1024)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "LinkedSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "LinkedSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        if "sourcingPolicy" in data and data["sourcingPolicy"] is not None:
            obj._sourcing_policy = (factory.create_object(data["sourcingPolicy"], "OracleSourcingPolicy"), dirty)
            factory.validate_type(obj._sourcing_policy[0], "OracleSourcingPolicy")
        else:
            obj._sourcing_policy = (obj.__undef__, dirty)
        if "syncParameters" in data and data["syncParameters"] is not None:
            obj._sync_parameters = (factory.create_object(data["syncParameters"], "OracleSyncParameters"), dirty)
            factory.validate_type(obj._sync_parameters[0], "OracleSyncParameters")
        else:
            obj._sync_parameters = (obj.__undef__, dirty)
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
        if "sync_strategy" == "type" or (self.sync_strategy is not self.__undef__ and (not (dirty and not self._sync_strategy[1]) or self.is_dirty_list(self.sync_strategy, self._sync_strategy) or belongs_to_parent)):
            dct["syncStrategy"] = dictify(self.sync_strategy, prop_is_list_or_vo=True)
        if "external_file_path" == "type" or (self.external_file_path is not self.__undef__ and (not (dirty and not self._external_file_path[1]) or self.is_dirty_list(self.external_file_path, self._external_file_path) or belongs_to_parent)):
            dct["externalFilePath"] = dictify(self.external_file_path)
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "sourcing_policy" == "type" or (self.sourcing_policy is not self.__undef__ and (not (dirty and not self._sourcing_policy[1]) or self.is_dirty_list(self.sourcing_policy, self._sourcing_policy) or belongs_to_parent)):
            dct["sourcingPolicy"] = dictify(self.sourcing_policy, prop_is_list_or_vo=True)
        if "sync_parameters" == "type" or (self.sync_parameters is not self.__undef__ and (not (dirty and not self._sync_parameters[1]) or self.is_dirty_list(self.sync_parameters, self._sync_parameters) or belongs_to_parent)):
            dct["syncParameters"] = dictify(self.sync_parameters, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._sync_strategy = (self._sync_strategy[0], True)
        self._external_file_path = (self._external_file_path[0], True)
        self._operations = (self._operations[0], True)
        self._sourcing_policy = (self._sourcing_policy[0], True)
        self._sync_parameters = (self._sync_parameters[0], True)

    def is_dirty(self):
        return any([self._sync_strategy[1], self._external_file_path[1], self._operations[1], self._sourcing_policy[1], self._sync_parameters[1]])

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
        if not isinstance(other, OracleBaseLinkData):
            return False
        return super().__eq__(other) and \
               self.sync_strategy == other.sync_strategy and \
               self.external_file_path == other.external_file_path and \
               self.operations == other.operations and \
               self.sourcing_policy == other.sourcing_policy and \
               self.sync_parameters == other.sync_parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def sync_strategy(self):
        """
        Persistent parameters to sync the container.

        :rtype: :py:class:`v1_11_13.web.vo.OracleSyncStrategy`
        """
        return self._sync_strategy[0]

    @sync_strategy.setter
    def sync_strategy(self, value):
        self._sync_strategy = (value, True)

    @property
    def external_file_path(self):
        """
        External file path.

        :rtype: ``str``
        """
        return self._external_file_path[0]

    @external_file_path.setter
    def external_file_path(self, value):
        self._external_file_path = (value, True)

    @property
    def operations(self):
        """
        User-specified operation hooks for this source.

        :rtype: :py:class:`v1_11_13.web.vo.LinkedSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

    @property
    def sourcing_policy(self):
        """
        Policies for managing LogSync and SnapSync across sources.

        :rtype: :py:class:`v1_11_13.web.vo.OracleSourcingPolicy`
        """
        return self._sourcing_policy[0]

    @sourcing_policy.setter
    def sourcing_policy(self, value):
        self._sourcing_policy = (value, True)

    @property
    def sync_parameters(self):
        """
        Parameters used to initially sync the database.

        :rtype: :py:class:`v1_11_13.web.vo.OracleSyncParameters`
        """
        return self._sync_parameters[0]

    @sync_parameters.setter
    def sync_parameters(self, value):
        self._sync_parameters = (value, True)

