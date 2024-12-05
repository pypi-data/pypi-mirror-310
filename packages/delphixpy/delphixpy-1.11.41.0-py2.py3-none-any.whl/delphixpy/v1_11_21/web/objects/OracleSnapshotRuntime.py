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
#     /delphix-oracle-snapshot-runtime.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.SnapshotRuntime import SnapshotRuntime
from delphixpy.v1_11_21 import factory
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleSnapshotRuntime(SnapshotRuntime):
    """
    *(extends* :py:class:`v1_11_21.web.vo.SnapshotRuntime` *)* Runtime (non-
    persistent) properties of an Oracle TimeFlow snapshot.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleSnapshotRuntime", True)
        self._missing_logs = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._missing_logs = []
        for item in data.get("missingLogs") or []:
            obj._missing_logs.append(factory.create_object(item))
            factory.validate_type(obj._missing_logs[-1], "OracleLog")
        obj._missing_logs = (obj._missing_logs, dirty)
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
        if "missing_logs" == "type" or (self.missing_logs is not self.__undef__ and (not (dirty and not self._missing_logs[1]))):
            dct["missingLogs"] = dictify(self.missing_logs)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._missing_logs = (self._missing_logs[0], True)

    def is_dirty(self):
        return any([self._missing_logs[1]])

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
        if not isinstance(other, OracleSnapshotRuntime):
            return False
        return super().__eq__(other) and \
               self.missing_logs == other.missing_logs

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def missing_logs(self):
        """
        List of missing log files for this snapshot, if any.

        :rtype: ``list`` of :py:class:`v1_11_21.web.vo.OracleLog`
        """
        return self._missing_logs[0]

    @missing_logs.setter
    def missing_logs(self, value):
        self._missing_logs = (value, True)

