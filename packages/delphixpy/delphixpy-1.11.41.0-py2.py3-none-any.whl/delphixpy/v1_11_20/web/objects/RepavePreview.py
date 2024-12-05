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
#     /delphix-repave-preview.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_20 import factory
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RepavePreview(TypedObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.TypedObject` *)* Preview engine
    summary and metadata of source engine.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RepavePreview", True)
        self._state = (self.__undef__, True)
        self._state_detail = (self.__undef__, True)
        self._source_engine_summary = (self.__undef__, True)
        self._source_engine_configurable_metadata = (self.__undef__, True)
        self._source_engine_snapshot_based_metadata = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._state = (data.get("state", obj.__undef__), dirty)
        if obj._state[0] is not None and obj._state[0] is not obj.__undef__:
            assert isinstance(obj._state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state[0], type(obj._state[0])))
            assert obj._state[0] in ['UNSET', 'PREPARING', 'PREPARE_SUCCESSFUL', 'PREPARE_FAILED', 'APPLYING', 'APPLY_SUCCESSFUL', 'APPLY_FAILED'], "Expected enum ['UNSET', 'PREPARING', 'PREPARE_SUCCESSFUL', 'PREPARE_FAILED', 'APPLYING', 'APPLY_SUCCESSFUL', 'APPLY_FAILED'] but got %s" % obj._state[0]
            common.validate_format(obj._state[0], "None", None, None)
        obj._state_detail = (data.get("stateDetail", obj.__undef__), dirty)
        if obj._state_detail[0] is not None and obj._state_detail[0] is not obj.__undef__:
            assert isinstance(obj._state_detail[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state_detail[0], type(obj._state_detail[0])))
            common.validate_format(obj._state_detail[0], "None", None, None)
        if "sourceEngineSummary" in data and data["sourceEngineSummary"] is not None:
            obj._source_engine_summary = (factory.create_object(data["sourceEngineSummary"], "RepaveEngineSummary"), dirty)
            factory.validate_type(obj._source_engine_summary[0], "RepaveEngineSummary")
        else:
            obj._source_engine_summary = (obj.__undef__, dirty)
        if "sourceEngineConfigurableMetadata" in data and data["sourceEngineConfigurableMetadata"] is not None:
            obj._source_engine_configurable_metadata = (factory.create_object(data["sourceEngineConfigurableMetadata"], "RepaveConfigurableMetadata"), dirty)
            factory.validate_type(obj._source_engine_configurable_metadata[0], "RepaveConfigurableMetadata")
        else:
            obj._source_engine_configurable_metadata = (obj.__undef__, dirty)
        obj._source_engine_snapshot_based_metadata = []
        for item in data.get("sourceEngineSnapshotBasedMetadata") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._source_engine_snapshot_based_metadata.append(item)
        obj._source_engine_snapshot_based_metadata = (obj._source_engine_snapshot_based_metadata, dirty)
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
        if "state" == "type" or (self.state is not self.__undef__ and (not (dirty and not self._state[1]))):
            dct["state"] = dictify(self.state)
        if dirty and "state" in dct:
            del dct["state"]
        if "state_detail" == "type" or (self.state_detail is not self.__undef__ and (not (dirty and not self._state_detail[1]))):
            dct["stateDetail"] = dictify(self.state_detail)
        if dirty and "stateDetail" in dct:
            del dct["stateDetail"]
        if "source_engine_summary" == "type" or (self.source_engine_summary is not self.__undef__ and (not (dirty and not self._source_engine_summary[1]))):
            dct["sourceEngineSummary"] = dictify(self.source_engine_summary)
        if dirty and "sourceEngineSummary" in dct:
            del dct["sourceEngineSummary"]
        if "source_engine_configurable_metadata" == "type" or (self.source_engine_configurable_metadata is not self.__undef__ and (not (dirty and not self._source_engine_configurable_metadata[1]))):
            dct["sourceEngineConfigurableMetadata"] = dictify(self.source_engine_configurable_metadata)
        if dirty and "sourceEngineConfigurableMetadata" in dct:
            del dct["sourceEngineConfigurableMetadata"]
        if "source_engine_snapshot_based_metadata" == "type" or (self.source_engine_snapshot_based_metadata is not self.__undef__ and (not (dirty and not self._source_engine_snapshot_based_metadata[1]))):
            dct["sourceEngineSnapshotBasedMetadata"] = dictify(self.source_engine_snapshot_based_metadata)
        if dirty and "sourceEngineSnapshotBasedMetadata" in dct:
            del dct["sourceEngineSnapshotBasedMetadata"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._state = (self._state[0], True)
        self._state_detail = (self._state_detail[0], True)
        self._source_engine_summary = (self._source_engine_summary[0], True)
        self._source_engine_configurable_metadata = (self._source_engine_configurable_metadata[0], True)
        self._source_engine_snapshot_based_metadata = (self._source_engine_snapshot_based_metadata[0], True)

    def is_dirty(self):
        return any([self._state[1], self._state_detail[1], self._source_engine_summary[1], self._source_engine_configurable_metadata[1], self._source_engine_snapshot_based_metadata[1]])

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
        if not isinstance(other, RepavePreview):
            return False
        return super().__eq__(other) and \
               self.state == other.state and \
               self.state_detail == other.state_detail and \
               self.source_engine_summary == other.source_engine_summary and \
               self.source_engine_configurable_metadata == other.source_engine_configurable_metadata and \
               self.source_engine_snapshot_based_metadata == other.source_engine_snapshot_based_metadata

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.state,
            self.state_detail,
            self.source_engine_summary,
            self.source_engine_configurable_metadata,
            self.source_engine_snapshot_based_metadata,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def state(self):
        """
        *(default value: NONE)* Repave state. *(permitted values: UNSET,
        PREPARING, PREPARE_SUCCESSFUL, PREPARE_FAILED, APPLYING,
        APPLY_SUCCESSFUL, APPLY_FAILED)*

        :rtype: ``str``
        """
        return self._state[0]

    @property
    def state_detail(self):
        """
        Detail for repave state.

        :rtype: ``str``
        """
        return self._state_detail[0]

    @property
    def source_engine_summary(self):
        """
        Summary of source engine.

        :rtype: :py:class:`v1_11_20.web.vo.RepaveEngineSummary`
        """
        return self._source_engine_summary[0]

    @property
    def source_engine_configurable_metadata(self):
        """
        Configurable metadata of source engine.

        :rtype: :py:class:`v1_11_20.web.vo.RepaveConfigurableMetadata`
        """
        return self._source_engine_configurable_metadata[0]

    @property
    def source_engine_snapshot_based_metadata(self):
        """
        Snapshot-based metadata list of source engine.

        :rtype: ``list`` of ``str``
        """
        return self._source_engine_snapshot_based_metadata[0]

