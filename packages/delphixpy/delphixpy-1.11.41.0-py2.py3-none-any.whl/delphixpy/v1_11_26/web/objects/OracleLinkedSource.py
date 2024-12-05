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
#     /delphix-oracle-linked-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_26.web.objects.OracleSource import OracleSource
from delphixpy.v1_11_26 import factory
from delphixpy.v1_11_26 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleLinkedSource(OracleSource):
    """
    *(extends* :py:class:`v1_11_26.web.vo.OracleSource` *)* A linked Oracle
    source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleLinkedSource", True)
        self._sync_strategy = (self.__undef__, True)
        self._external_file_path = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._locked = (self.__undef__, True)


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
            obj._operations = (factory.create_object(data["operations"], "OracleLinkedSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "OracleLinkedSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        obj._locked = (data.get("locked", obj.__undef__), dirty)
        if obj._locked[0] is not None and obj._locked[0] is not obj.__undef__:
            assert isinstance(obj._locked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._locked[0], type(obj._locked[0])))
            common.validate_format(obj._locked[0], "None", None, None)
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
        if "locked" == "type" or (self.locked is not self.__undef__ and (not (dirty and not self._locked[1]))):
            dct["locked"] = dictify(self.locked)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._sync_strategy = (self._sync_strategy[0], True)
        self._external_file_path = (self._external_file_path[0], True)
        self._operations = (self._operations[0], True)
        self._locked = (self._locked[0], True)

    def is_dirty(self):
        return any([self._sync_strategy[1], self._external_file_path[1], self._operations[1], self._locked[1]])

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
        if not isinstance(other, OracleLinkedSource):
            return False
        return super().__eq__(other) and \
               self.sync_strategy == other.sync_strategy and \
               self.external_file_path == other.external_file_path and \
               self.operations == other.operations and \
               self.locked == other.locked

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def sync_strategy(self):
        """
        Parameters used to sync the container. These are persisted and used for
        every sync operation.

        :rtype: :py:class:`v1_11_26.web.vo.OracleSyncStrategy`
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

        :rtype: :py:class:`v1_11_26.web.vo.OracleLinkedSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

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

