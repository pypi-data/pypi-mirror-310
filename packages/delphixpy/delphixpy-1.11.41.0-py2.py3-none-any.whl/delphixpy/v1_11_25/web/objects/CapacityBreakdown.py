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
#     /delphix-capacity-breakdown.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_25.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_25 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CapacityBreakdown(TypedObject):
    """
    *(extends* :py:class:`v1_11_25.web.vo.TypedObject` *)* Storage stats
    breakdown.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CapacityBreakdown", True)
        self._actual_space = (self.__undef__, True)
        self._unvirtualized_space = (self.__undef__, True)
        self._timeflow_unvirtualized_space = (self.__undef__, True)
        self._active_space = (self.__undef__, True)
        self._log_space = (self.__undef__, True)
        self._sync_space = (self.__undef__, True)
        self._descendant_space = (self.__undef__, True)
        self._policy_space = (self.__undef__, True)
        self._manual_space = (self.__undef__, True)
        self._unowned_snapshot_space = (self.__undef__, True)
        self._ingested_size = (self.__undef__, True)
        self._fallback_ingested_size_timestamp = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._actual_space = (data.get("actualSpace", obj.__undef__), dirty)
        if obj._actual_space[0] is not None and obj._actual_space[0] is not obj.__undef__:
            assert isinstance(obj._actual_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._actual_space[0], type(obj._actual_space[0])))
            common.validate_format(obj._actual_space[0], "None", None, None)
        obj._unvirtualized_space = (data.get("unvirtualizedSpace", obj.__undef__), dirty)
        if obj._unvirtualized_space[0] is not None and obj._unvirtualized_space[0] is not obj.__undef__:
            assert isinstance(obj._unvirtualized_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._unvirtualized_space[0], type(obj._unvirtualized_space[0])))
            common.validate_format(obj._unvirtualized_space[0], "None", None, None)
        obj._timeflow_unvirtualized_space = (data.get("timeflowUnvirtualizedSpace", obj.__undef__), dirty)
        if obj._timeflow_unvirtualized_space[0] is not None and obj._timeflow_unvirtualized_space[0] is not obj.__undef__:
            assert isinstance(obj._timeflow_unvirtualized_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._timeflow_unvirtualized_space[0], type(obj._timeflow_unvirtualized_space[0])))
            common.validate_format(obj._timeflow_unvirtualized_space[0], "None", None, None)
        obj._active_space = (data.get("activeSpace", obj.__undef__), dirty)
        if obj._active_space[0] is not None and obj._active_space[0] is not obj.__undef__:
            assert isinstance(obj._active_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._active_space[0], type(obj._active_space[0])))
            common.validate_format(obj._active_space[0], "None", None, None)
        obj._log_space = (data.get("logSpace", obj.__undef__), dirty)
        if obj._log_space[0] is not None and obj._log_space[0] is not obj.__undef__:
            assert isinstance(obj._log_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._log_space[0], type(obj._log_space[0])))
            common.validate_format(obj._log_space[0], "None", None, None)
        obj._sync_space = (data.get("syncSpace", obj.__undef__), dirty)
        if obj._sync_space[0] is not None and obj._sync_space[0] is not obj.__undef__:
            assert isinstance(obj._sync_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._sync_space[0], type(obj._sync_space[0])))
            common.validate_format(obj._sync_space[0], "None", None, None)
        obj._descendant_space = (data.get("descendantSpace", obj.__undef__), dirty)
        if obj._descendant_space[0] is not None and obj._descendant_space[0] is not obj.__undef__:
            assert isinstance(obj._descendant_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._descendant_space[0], type(obj._descendant_space[0])))
            common.validate_format(obj._descendant_space[0], "None", None, None)
        obj._policy_space = (data.get("policySpace", obj.__undef__), dirty)
        if obj._policy_space[0] is not None and obj._policy_space[0] is not obj.__undef__:
            assert isinstance(obj._policy_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._policy_space[0], type(obj._policy_space[0])))
            common.validate_format(obj._policy_space[0], "None", None, None)
        obj._manual_space = (data.get("manualSpace", obj.__undef__), dirty)
        if obj._manual_space[0] is not None and obj._manual_space[0] is not obj.__undef__:
            assert isinstance(obj._manual_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._manual_space[0], type(obj._manual_space[0])))
            common.validate_format(obj._manual_space[0], "None", None, None)
        obj._unowned_snapshot_space = (data.get("unownedSnapshotSpace", obj.__undef__), dirty)
        if obj._unowned_snapshot_space[0] is not None and obj._unowned_snapshot_space[0] is not obj.__undef__:
            assert isinstance(obj._unowned_snapshot_space[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._unowned_snapshot_space[0], type(obj._unowned_snapshot_space[0])))
            common.validate_format(obj._unowned_snapshot_space[0], "None", None, None)
        obj._ingested_size = (data.get("ingestedSize", obj.__undef__), dirty)
        if obj._ingested_size[0] is not None and obj._ingested_size[0] is not obj.__undef__:
            assert isinstance(obj._ingested_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._ingested_size[0], type(obj._ingested_size[0])))
            common.validate_format(obj._ingested_size[0], "None", None, None)
        obj._fallback_ingested_size_timestamp = (data.get("fallbackIngestedSizeTimestamp", obj.__undef__), dirty)
        if obj._fallback_ingested_size_timestamp[0] is not None and obj._fallback_ingested_size_timestamp[0] is not obj.__undef__:
            assert isinstance(obj._fallback_ingested_size_timestamp[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._fallback_ingested_size_timestamp[0], type(obj._fallback_ingested_size_timestamp[0])))
            common.validate_format(obj._fallback_ingested_size_timestamp[0], "date", None, None)
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
        if "actual_space" == "type" or (self.actual_space is not self.__undef__ and (not (dirty and not self._actual_space[1]))):
            dct["actualSpace"] = dictify(self.actual_space)
        if "unvirtualized_space" == "type" or (self.unvirtualized_space is not self.__undef__ and (not (dirty and not self._unvirtualized_space[1]))):
            dct["unvirtualizedSpace"] = dictify(self.unvirtualized_space)
        if "timeflow_unvirtualized_space" == "type" or (self.timeflow_unvirtualized_space is not self.__undef__ and (not (dirty and not self._timeflow_unvirtualized_space[1]))):
            dct["timeflowUnvirtualizedSpace"] = dictify(self.timeflow_unvirtualized_space)
        if "active_space" == "type" or (self.active_space is not self.__undef__ and (not (dirty and not self._active_space[1]))):
            dct["activeSpace"] = dictify(self.active_space)
        if "log_space" == "type" or (self.log_space is not self.__undef__ and (not (dirty and not self._log_space[1]))):
            dct["logSpace"] = dictify(self.log_space)
        if "sync_space" == "type" or (self.sync_space is not self.__undef__ and (not (dirty and not self._sync_space[1]))):
            dct["syncSpace"] = dictify(self.sync_space)
        if "descendant_space" == "type" or (self.descendant_space is not self.__undef__ and (not (dirty and not self._descendant_space[1]))):
            dct["descendantSpace"] = dictify(self.descendant_space)
        if "policy_space" == "type" or (self.policy_space is not self.__undef__ and (not (dirty and not self._policy_space[1]))):
            dct["policySpace"] = dictify(self.policy_space)
        if "manual_space" == "type" or (self.manual_space is not self.__undef__ and (not (dirty and not self._manual_space[1]))):
            dct["manualSpace"] = dictify(self.manual_space)
        if "unowned_snapshot_space" == "type" or (self.unowned_snapshot_space is not self.__undef__ and (not (dirty and not self._unowned_snapshot_space[1]))):
            dct["unownedSnapshotSpace"] = dictify(self.unowned_snapshot_space)
        if "ingested_size" == "type" or (self.ingested_size is not self.__undef__ and (not (dirty and not self._ingested_size[1]))):
            dct["ingestedSize"] = dictify(self.ingested_size)
        if "fallback_ingested_size_timestamp" == "type" or (self.fallback_ingested_size_timestamp is not self.__undef__ and (not (dirty and not self._fallback_ingested_size_timestamp[1]))):
            dct["fallbackIngestedSizeTimestamp"] = dictify(self.fallback_ingested_size_timestamp)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._actual_space = (self._actual_space[0], True)
        self._unvirtualized_space = (self._unvirtualized_space[0], True)
        self._timeflow_unvirtualized_space = (self._timeflow_unvirtualized_space[0], True)
        self._active_space = (self._active_space[0], True)
        self._log_space = (self._log_space[0], True)
        self._sync_space = (self._sync_space[0], True)
        self._descendant_space = (self._descendant_space[0], True)
        self._policy_space = (self._policy_space[0], True)
        self._manual_space = (self._manual_space[0], True)
        self._unowned_snapshot_space = (self._unowned_snapshot_space[0], True)
        self._ingested_size = (self._ingested_size[0], True)
        self._fallback_ingested_size_timestamp = (self._fallback_ingested_size_timestamp[0], True)

    def is_dirty(self):
        return any([self._actual_space[1], self._unvirtualized_space[1], self._timeflow_unvirtualized_space[1], self._active_space[1], self._log_space[1], self._sync_space[1], self._descendant_space[1], self._policy_space[1], self._manual_space[1], self._unowned_snapshot_space[1], self._ingested_size[1], self._fallback_ingested_size_timestamp[1]])

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
        if not isinstance(other, CapacityBreakdown):
            return False
        return super().__eq__(other) and \
               self.actual_space == other.actual_space and \
               self.unvirtualized_space == other.unvirtualized_space and \
               self.timeflow_unvirtualized_space == other.timeflow_unvirtualized_space and \
               self.active_space == other.active_space and \
               self.log_space == other.log_space and \
               self.sync_space == other.sync_space and \
               self.descendant_space == other.descendant_space and \
               self.policy_space == other.policy_space and \
               self.manual_space == other.manual_space and \
               self.unowned_snapshot_space == other.unowned_snapshot_space and \
               self.ingested_size == other.ingested_size and \
               self.fallback_ingested_size_timestamp == other.fallback_ingested_size_timestamp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def actual_space(self):
        """
        Actual space used by the container.

        :rtype: ``float``
        """
        return self._actual_space[0]

    @actual_space.setter
    def actual_space(self, value):
        self._actual_space = (value, True)

    @property
    def unvirtualized_space(self):
        """
        Unvirtualized space used by the container.

        :rtype: ``float``
        """
        return self._unvirtualized_space[0]

    @unvirtualized_space.setter
    def unvirtualized_space(self, value):
        self._unvirtualized_space = (value, True)

    @property
    def timeflow_unvirtualized_space(self):
        """
        Unvirtualized space used by the TimeFlow.

        :rtype: ``float``
        """
        return self._timeflow_unvirtualized_space[0]

    @timeflow_unvirtualized_space.setter
    def timeflow_unvirtualized_space(self, value):
        self._timeflow_unvirtualized_space = (value, True)

    @property
    def active_space(self):
        """
        Amount of space used for the active copy of the container.

        :rtype: ``float``
        """
        return self._active_space[0]

    @active_space.setter
    def active_space(self, value):
        self._active_space = (value, True)

    @property
    def log_space(self):
        """
        Amount of space used by logs.

        :rtype: ``float``
        """
        return self._log_space[0]

    @log_space.setter
    def log_space(self, value):
        self._log_space = (value, True)

    @property
    def sync_space(self):
        """
        Amount of space used by snapshots.

        :rtype: ``float``
        """
        return self._sync_space[0]

    @sync_space.setter
    def sync_space(self, value):
        self._sync_space = (value, True)

    @property
    def descendant_space(self):
        """
        Amount of space used for snapshots from which VDBs have been
        provisioned.

        :rtype: ``float``
        """
        return self._descendant_space[0]

    @descendant_space.setter
    def descendant_space(self, value):
        self._descendant_space = (value, True)

    @property
    def policy_space(self):
        """
        Amount of space used for snapshots held by policy settings.

        :rtype: ``float``
        """
        return self._policy_space[0]

    @policy_space.setter
    def policy_space(self, value):
        self._policy_space = (value, True)

    @property
    def manual_space(self):
        """
        Amount of space used for snapshots held by manual retention settings.

        :rtype: ``float``
        """
        return self._manual_space[0]

    @manual_space.setter
    def manual_space(self, value):
        self._manual_space = (value, True)

    @property
    def unowned_snapshot_space(self):
        """
        Amount of space used for snapshots part of held space.

        :rtype: ``float``
        """
        return self._unowned_snapshot_space[0]

    @unowned_snapshot_space.setter
    def unowned_snapshot_space(self, value):
        self._unowned_snapshot_space = (value, True)

    @property
    def ingested_size(self):
        """
        Amount of space ingested by the source.

        :rtype: ``float``
        """
        return self._ingested_size[0]

    @ingested_size.setter
    def ingested_size(self, value):
        self._ingested_size = (value, True)

    @property
    def fallback_ingested_size_timestamp(self):
        """
        Original time of the ingested size value used if a fallback (last known
        good) value was used. Will be null if no fallback data was used.

        :rtype: ``str`` *or* ``null``
        """
        return self._fallback_ingested_size_timestamp[0]

    @fallback_ingested_size_timestamp.setter
    def fallback_ingested_size_timestamp(self, value):
        self._fallback_ingested_size_timestamp = (value, True)

