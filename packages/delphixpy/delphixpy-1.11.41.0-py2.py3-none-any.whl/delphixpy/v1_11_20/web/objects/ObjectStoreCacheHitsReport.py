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
#     /delphix-object-store-cache-hits-report.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ObjectStoreCacheHitsReport(TypedObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.TypedObject` *)* A cache hits report
    for an object store.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ObjectStoreCacheHitsReport", True)
        self._start_time = (self.__undef__, True)
        self._end_time = (self.__undef__, True)
        self._cache_hits = (self.__undef__, True)
        self._cache_lookups = (self.__undef__, True)
        self._cache_capacity = (self.__undef__, True)
        self._bucket_size = (self.__undef__, True)
        self._hits_report = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._start_time = (data.get("startTime", obj.__undef__), dirty)
        if obj._start_time[0] is not None and obj._start_time[0] is not obj.__undef__:
            assert isinstance(obj._start_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_time[0], type(obj._start_time[0])))
            common.validate_format(obj._start_time[0], "None", None, None)
        obj._end_time = (data.get("endTime", obj.__undef__), dirty)
        if obj._end_time[0] is not None and obj._end_time[0] is not obj.__undef__:
            assert isinstance(obj._end_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._end_time[0], type(obj._end_time[0])))
            common.validate_format(obj._end_time[0], "None", None, None)
        obj._cache_hits = (data.get("cacheHits", obj.__undef__), dirty)
        if obj._cache_hits[0] is not None and obj._cache_hits[0] is not obj.__undef__:
            assert isinstance(obj._cache_hits[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._cache_hits[0], type(obj._cache_hits[0])))
            common.validate_format(obj._cache_hits[0], "None", None, None)
        obj._cache_lookups = (data.get("cacheLookups", obj.__undef__), dirty)
        if obj._cache_lookups[0] is not None and obj._cache_lookups[0] is not obj.__undef__:
            assert isinstance(obj._cache_lookups[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._cache_lookups[0], type(obj._cache_lookups[0])))
            common.validate_format(obj._cache_lookups[0], "None", None, None)
        obj._cache_capacity = (data.get("cacheCapacity", obj.__undef__), dirty)
        if obj._cache_capacity[0] is not None and obj._cache_capacity[0] is not obj.__undef__:
            assert isinstance(obj._cache_capacity[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._cache_capacity[0], type(obj._cache_capacity[0])))
            common.validate_format(obj._cache_capacity[0], "None", None, None)
        obj._bucket_size = (data.get("bucketSize", obj.__undef__), dirty)
        if obj._bucket_size[0] is not None and obj._bucket_size[0] is not obj.__undef__:
            assert isinstance(obj._bucket_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._bucket_size[0], type(obj._bucket_size[0])))
            common.validate_format(obj._bucket_size[0], "None", None, None)
        obj._hits_report = []
        for item in data.get("hitsReport") or []:
            assert isinstance(item, float), ("Expected one of ['number'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._hits_report.append(item)
        obj._hits_report = (obj._hits_report, dirty)
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
        if "start_time" == "type" or (self.start_time is not self.__undef__ and (not (dirty and not self._start_time[1]))):
            dct["startTime"] = dictify(self.start_time)
        if "end_time" == "type" or (self.end_time is not self.__undef__ and (not (dirty and not self._end_time[1]))):
            dct["endTime"] = dictify(self.end_time)
        if "cache_hits" == "type" or (self.cache_hits is not self.__undef__ and (not (dirty and not self._cache_hits[1]))):
            dct["cacheHits"] = dictify(self.cache_hits)
        if "cache_lookups" == "type" or (self.cache_lookups is not self.__undef__ and (not (dirty and not self._cache_lookups[1]))):
            dct["cacheLookups"] = dictify(self.cache_lookups)
        if "cache_capacity" == "type" or (self.cache_capacity is not self.__undef__ and (not (dirty and not self._cache_capacity[1]))):
            dct["cacheCapacity"] = dictify(self.cache_capacity)
        if "bucket_size" == "type" or (self.bucket_size is not self.__undef__ and (not (dirty and not self._bucket_size[1]))):
            dct["bucketSize"] = dictify(self.bucket_size)
        if "hits_report" == "type" or (self.hits_report is not self.__undef__ and (not (dirty and not self._hits_report[1]))):
            dct["hitsReport"] = dictify(self.hits_report)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._start_time = (self._start_time[0], True)
        self._end_time = (self._end_time[0], True)
        self._cache_hits = (self._cache_hits[0], True)
        self._cache_lookups = (self._cache_lookups[0], True)
        self._cache_capacity = (self._cache_capacity[0], True)
        self._bucket_size = (self._bucket_size[0], True)
        self._hits_report = (self._hits_report[0], True)

    def is_dirty(self):
        return any([self._start_time[1], self._end_time[1], self._cache_hits[1], self._cache_lookups[1], self._cache_capacity[1], self._bucket_size[1], self._hits_report[1]])

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
        if not isinstance(other, ObjectStoreCacheHitsReport):
            return False
        return super().__eq__(other) and \
               self.start_time == other.start_time and \
               self.end_time == other.end_time and \
               self.cache_hits == other.cache_hits and \
               self.cache_lookups == other.cache_lookups and \
               self.cache_capacity == other.cache_capacity and \
               self.bucket_size == other.bucket_size and \
               self.hits_report == other.hits_report

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def start_time(self):
        """
        Time when cache hits data was first recorded by the report.

        :rtype: ``str``
        """
        return self._start_time[0]

    @start_time.setter
    def start_time(self, value):
        self._start_time = (value, True)

    @property
    def end_time(self):
        """
        Time when the cache hits report was generated.

        :rtype: ``str``
        """
        return self._end_time[0]

    @end_time.setter
    def end_time(self, value):
        self._end_time = (value, True)

    @property
    def cache_hits(self):
        """
        The number of cache hits.

        :rtype: ``float``
        """
        return self._cache_hits[0]

    @cache_hits.setter
    def cache_hits(self, value):
        self._cache_hits = (value, True)

    @property
    def cache_lookups(self):
        """
        The total number of cache lookups.

        :rtype: ``float``
        """
        return self._cache_lookups[0]

    @cache_lookups.setter
    def cache_lookups(self, value):
        self._cache_lookups = (value, True)

    @property
    def cache_capacity(self):
        """
        The size of the ZettaCache, in bytes.

        :rtype: ``float``
        """
        return self._cache_capacity[0]

    @cache_capacity.setter
    def cache_capacity(self, value):
        self._cache_capacity = (value, True)

    @property
    def bucket_size(self):
        """
        The size of each bucket in the hits report, in bytes.

        :rtype: ``float``
        """
        return self._bucket_size[0]

    @bucket_size.setter
    def bucket_size(self, value):
        self._bucket_size = (value, True)

    @property
    def hits_report(self):
        """
        The cumulative number of hits occurring in each bucket as cache size
        increases.

        :rtype: ``list`` of ``float``
        """
        return self._hits_report[0]

    @hits_report.setter
    def hits_report(self, value):
        self._hits_report = (value, True)

