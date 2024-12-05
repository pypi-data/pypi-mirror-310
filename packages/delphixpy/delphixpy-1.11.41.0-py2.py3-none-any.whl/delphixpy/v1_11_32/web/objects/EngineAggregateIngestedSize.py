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
#     /delphix-engine-aggregate-ingested-size.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_32 import factory
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class EngineAggregateIngestedSize(TypedObject):
    """
    *(extends* :py:class:`v1_11_32.web.vo.TypedObject` *)* Object which holds
    information regarding how much data was ingested, of all source types,
    within an engine.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("EngineAggregateIngestedSize", True)
        self._aggregate_ingested_size = (self.__undef__, True)
        self._aggregates = (self.__undef__, True)
        self._source_ingestion_data = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._aggregate_ingested_size = (data.get("aggregateIngestedSize", obj.__undef__), dirty)
        if obj._aggregate_ingested_size[0] is not None and obj._aggregate_ingested_size[0] is not obj.__undef__:
            assert isinstance(obj._aggregate_ingested_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._aggregate_ingested_size[0], type(obj._aggregate_ingested_size[0])))
            common.validate_format(obj._aggregate_ingested_size[0], "None", None, None)
        obj._aggregates = []
        for item in data.get("aggregates") or []:
            obj._aggregates.append(factory.create_object(item))
            factory.validate_type(obj._aggregates[-1], "SourceTypeAggregateIngestedSize")
        obj._aggregates = (obj._aggregates, dirty)
        obj._source_ingestion_data = []
        for item in data.get("sourceIngestionData") or []:
            obj._source_ingestion_data.append(factory.create_object(item))
            factory.validate_type(obj._source_ingestion_data[-1], "SourceIngestionData")
        obj._source_ingestion_data = (obj._source_ingestion_data, dirty)
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
        if "aggregate_ingested_size" == "type" or (self.aggregate_ingested_size is not self.__undef__ and (not (dirty and not self._aggregate_ingested_size[1]))):
            dct["aggregateIngestedSize"] = dictify(self.aggregate_ingested_size)
        if dirty and "aggregateIngestedSize" in dct:
            del dct["aggregateIngestedSize"]
        if "aggregates" == "type" or (self.aggregates is not self.__undef__ and (not (dirty and not self._aggregates[1]))):
            dct["aggregates"] = dictify(self.aggregates)
        if dirty and "aggregates" in dct:
            del dct["aggregates"]
        if "source_ingestion_data" == "type" or (self.source_ingestion_data is not self.__undef__ and (not (dirty and not self._source_ingestion_data[1]))):
            dct["sourceIngestionData"] = dictify(self.source_ingestion_data)
        if dirty and "sourceIngestionData" in dct:
            del dct["sourceIngestionData"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._aggregate_ingested_size = (self._aggregate_ingested_size[0], True)
        self._aggregates = (self._aggregates[0], True)
        self._source_ingestion_data = (self._source_ingestion_data[0], True)

    def is_dirty(self):
        return any([self._aggregate_ingested_size[1], self._aggregates[1], self._source_ingestion_data[1]])

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
        if not isinstance(other, EngineAggregateIngestedSize):
            return False
        return super().__eq__(other) and \
               self.aggregate_ingested_size == other.aggregate_ingested_size and \
               self.aggregates == other.aggregates and \
               self.source_ingestion_data == other.source_ingestion_data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.aggregate_ingested_size,
            self.aggregates,
            self.source_ingestion_data,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def aggregate_ingested_size(self):
        """
        The aggregate ingested source size for an engine.

        :rtype: ``float``
        """
        return self._aggregate_ingested_size[0]

    @property
    def aggregates(self):
        """
        Aggregates per type of source.

        :rtype: ``list`` of
            :py:class:`v1_11_32.web.vo.SourceTypeAggregateIngestedSize`
        """
        return self._aggregates[0]

    @property
    def source_ingestion_data(self):
        """
        Objects that specify what data was included in the aggregated ingested
        size (aggregateIngestedSize field) for the engine. The individual
        objects contribute to their respective SourceTypeAggregateIngestedSize
        in the aggregates field.

        :rtype: ``list`` of :py:class:`v1_11_32.web.vo.SourceIngestionData`
        """
        return self._source_ingestion_data[0]

