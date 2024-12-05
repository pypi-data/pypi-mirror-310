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
#     /delphix-oracle-enhanced-export-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_17.web.objects.ExportParameters import ExportParameters
from delphixpy.v1_11_17 import factory
from delphixpy.v1_11_17 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleEnhancedExportParameters(ExportParameters):
    """
    *(extends* :py:class:`v1_11_17.web.vo.ExportParameters` *)* The enhanced
    parameters to use as input to export Oracle databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleEnhancedExportParameters", True)
        self._storage_strategy = (self.__undef__, True)
        self._transfer_strategy = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "storageStrategy" in data and data["storageStrategy"] is not None:
            obj._storage_strategy = (factory.create_object(data["storageStrategy"], "OracleExportStorageStrategy"), dirty)
            factory.validate_type(obj._storage_strategy[0], "OracleExportStorageStrategy")
        else:
            obj._storage_strategy = (obj.__undef__, dirty)
        if "transferStrategy" in data and data["transferStrategy"] is not None:
            obj._transfer_strategy = (factory.create_object(data["transferStrategy"], "OracleExportTransferStrategy"), dirty)
            factory.validate_type(obj._transfer_strategy[0], "OracleExportTransferStrategy")
        else:
            obj._transfer_strategy = (obj.__undef__, dirty)
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
        if "storage_strategy" == "type" or (self.storage_strategy is not self.__undef__ and (not (dirty and not self._storage_strategy[1]) or self.is_dirty_list(self.storage_strategy, self._storage_strategy) or belongs_to_parent)):
            dct["storageStrategy"] = dictify(self.storage_strategy, prop_is_list_or_vo=True)
        if "transfer_strategy" == "type" or (self.transfer_strategy is not self.__undef__ and (not (dirty and not self._transfer_strategy[1]) or self.is_dirty_list(self.transfer_strategy, self._transfer_strategy) or belongs_to_parent)):
            dct["transferStrategy"] = dictify(self.transfer_strategy, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._storage_strategy = (self._storage_strategy[0], True)
        self._transfer_strategy = (self._transfer_strategy[0], True)

    def is_dirty(self):
        return any([self._storage_strategy[1], self._transfer_strategy[1]])

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
        if not isinstance(other, OracleEnhancedExportParameters):
            return False
        return super().__eq__(other) and \
               self.storage_strategy == other.storage_strategy and \
               self.transfer_strategy == other.transfer_strategy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def storage_strategy(self):
        """
        The storage strategy to use while exporting the database.

        :rtype: :py:class:`v1_11_17.web.vo.OracleExportStorageStrategy`
        """
        return self._storage_strategy[0]

    @storage_strategy.setter
    def storage_strategy(self, value):
        self._storage_strategy = (value, True)

    @property
    def transfer_strategy(self):
        """
        The transfer strategy to use while exporting the database.

        :rtype: :py:class:`v1_11_17.web.vo.OracleExportTransferStrategy`
        """
        return self._transfer_strategy[0]

    @transfer_strategy.setter
    def transfer_strategy(self, value):
        self._transfer_strategy = (value, True)

