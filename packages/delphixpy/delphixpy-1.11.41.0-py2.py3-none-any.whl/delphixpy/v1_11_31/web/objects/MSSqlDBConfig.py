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
#     /delphix-mssql-db-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_31.web.objects.SourceConfig import SourceConfig
from delphixpy.v1_11_31 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlDBConfig(SourceConfig):
    """
    *(extends* :py:class:`v1_11_31.web.vo.SourceConfig` *)* Configuration
    information for a MSSQL Source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlDBConfig", True)
        self._database_name = (self.__undef__, True)
        self._repository = (self.__undef__, True)
        self._recovery_model = (self.__undef__, True)
        self._mirroring_state = (self.__undef__, True)
        self._replica = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._database_name = (data.get("databaseName", obj.__undef__), dirty)
        if obj._database_name[0] is not None and obj._database_name[0] is not obj.__undef__:
            assert isinstance(obj._database_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._database_name[0], type(obj._database_name[0])))
            common.validate_format(obj._database_name[0], "None", None, 128)
        obj._repository = (data.get("repository", obj.__undef__), dirty)
        if obj._repository[0] is not None and obj._repository[0] is not obj.__undef__:
            assert isinstance(obj._repository[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._repository[0], type(obj._repository[0])))
            common.validate_format(obj._repository[0], "objectReference", None, None)
        obj._recovery_model = (data.get("recoveryModel", obj.__undef__), dirty)
        if obj._recovery_model[0] is not None and obj._recovery_model[0] is not obj.__undef__:
            assert isinstance(obj._recovery_model[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._recovery_model[0], type(obj._recovery_model[0])))
            assert obj._recovery_model[0] in ['FULL', 'SIMPLE', 'BULK_LOGGED'], "Expected enum ['FULL', 'SIMPLE', 'BULK_LOGGED'] but got %s" % obj._recovery_model[0]
            common.validate_format(obj._recovery_model[0], "None", None, None)
        obj._mirroring_state = (data.get("mirroringState", obj.__undef__), dirty)
        if obj._mirroring_state[0] is not None and obj._mirroring_state[0] is not obj.__undef__:
            assert isinstance(obj._mirroring_state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mirroring_state[0], type(obj._mirroring_state[0])))
            assert obj._mirroring_state[0] in ['SUSPENDED', 'DISCONNECTED', 'SYNCHRONIZING', 'PENDING_FAILOVER', 'SYNCHRONIZED', 'NOT_SYNCHRONIZED', 'FAILOVER_POSSIBLE', 'NONE'], "Expected enum ['SUSPENDED', 'DISCONNECTED', 'SYNCHRONIZING', 'PENDING_FAILOVER', 'SYNCHRONIZED', 'NOT_SYNCHRONIZED', 'FAILOVER_POSSIBLE', 'NONE'] but got %s" % obj._mirroring_state[0]
            common.validate_format(obj._mirroring_state[0], "None", None, None)
        obj._replica = (data.get("replica", obj.__undef__), dirty)
        if obj._replica[0] is not None and obj._replica[0] is not obj.__undef__:
            assert isinstance(obj._replica[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._replica[0], type(obj._replica[0])))
            common.validate_format(obj._replica[0], "None", None, None)
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
        if "database_name" == "type" or (self.database_name is not self.__undef__ and (not (dirty and not self._database_name[1]) or self.is_dirty_list(self.database_name, self._database_name) or belongs_to_parent)):
            dct["databaseName"] = dictify(self.database_name)
        if "repository" == "type" or (self.repository is not self.__undef__ and (not (dirty and not self._repository[1]) or self.is_dirty_list(self.repository, self._repository) or belongs_to_parent)):
            dct["repository"] = dictify(self.repository)
        if "recovery_model" == "type" or (self.recovery_model is not self.__undef__ and (not (dirty and not self._recovery_model[1]) or self.is_dirty_list(self.recovery_model, self._recovery_model) or belongs_to_parent)):
            dct["recoveryModel"] = dictify(self.recovery_model)
        elif belongs_to_parent and self.recovery_model is self.__undef__:
            dct["recoveryModel"] = "SIMPLE"
        if "mirroring_state" == "type" or (self.mirroring_state is not self.__undef__ and (not (dirty and not self._mirroring_state[1]) or self.is_dirty_list(self.mirroring_state, self._mirroring_state) or belongs_to_parent)):
            dct["mirroringState"] = dictify(self.mirroring_state)
        elif belongs_to_parent and self.mirroring_state is self.__undef__:
            dct["mirroringState"] = "NONE"
        if "replica" == "type" or (self.replica is not self.__undef__ and (not (dirty and not self._replica[1]))):
            dct["replica"] = dictify(self.replica)
        if dirty and "replica" in dct:
            del dct["replica"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._database_name = (self._database_name[0], True)
        self._repository = (self._repository[0], True)
        self._recovery_model = (self._recovery_model[0], True)
        self._mirroring_state = (self._mirroring_state[0], True)
        self._replica = (self._replica[0], True)

    def is_dirty(self):
        return any([self._database_name[1], self._repository[1], self._recovery_model[1], self._mirroring_state[1], self._replica[1]])

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
        if not isinstance(other, MSSqlDBConfig):
            return False
        return super().__eq__(other) and \
               self.database_name == other.database_name and \
               self.repository == other.repository and \
               self.recovery_model == other.recovery_model and \
               self.mirroring_state == other.mirroring_state and \
               self.replica == other.replica

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def database_name(self):
        """
        The name of the database.

        :rtype: ``str``
        """
        return self._database_name[0]

    @database_name.setter
    def database_name(self, value):
        self._database_name = (value, True)

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
    def recovery_model(self):
        """
        *(default value: SIMPLE)* Specifies the current recovery model of the
        source database. *(permitted values: FULL, SIMPLE, BULK_LOGGED)*

        :rtype: ``str``
        """
        return self._recovery_model[0]

    @recovery_model.setter
    def recovery_model(self, value):
        self._recovery_model = (value, True)

    @property
    def mirroring_state(self):
        """
        *(default value: NONE)* SQL Server DB mirroring state. *(permitted
        values: SUSPENDED, DISCONNECTED, SYNCHRONIZING, PENDING_FAILOVER,
        SYNCHRONIZED, NOT_SYNCHRONIZED, FAILOVER_POSSIBLE, NONE)*

        :rtype: ``str``
        """
        return self._mirroring_state[0]

    @mirroring_state.setter
    def mirroring_state(self, value):
        self._mirroring_state = (value, True)

    @property
    def replica(self):
        """
        Whether this config belongs to a replica source.

        :rtype: ``bool``
        """
        return self._replica[0]

