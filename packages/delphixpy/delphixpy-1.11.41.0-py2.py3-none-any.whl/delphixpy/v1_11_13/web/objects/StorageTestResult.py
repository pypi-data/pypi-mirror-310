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
#     /delphix-storage-test-result.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_13.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_13 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StorageTestResult(TypedObject):
    """
    *(extends* :py:class:`v1_11_13.web.vo.TypedObject` *)* The test results of
    one storage test.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StorageTestResult", True)
        self._test_name = (self.__undef__, True)
        self._test_type = (self.__undef__, True)
        self._jobs = (self.__undef__, True)
        self._block_size = (self.__undef__, True)
        self._iops = (self.__undef__, True)
        self._throughput = (self.__undef__, True)
        self._average_latency = (self.__undef__, True)
        self._min_latency = (self.__undef__, True)
        self._max_latency = (self.__undef__, True)
        self._stddev_latency = (self.__undef__, True)
        self._latency95th_percentile = (self.__undef__, True)
        self._load_scaling = (self.__undef__, True)
        self._latency_grade = (self.__undef__, True)
        self._load_scaling_grade = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._test_name = (data.get("testName", obj.__undef__), dirty)
        if obj._test_name[0] is not None and obj._test_name[0] is not obj.__undef__:
            assert isinstance(obj._test_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._test_name[0], type(obj._test_name[0])))
            common.validate_format(obj._test_name[0], "None", None, None)
        obj._test_type = (data.get("testType", obj.__undef__), dirty)
        if obj._test_type[0] is not None and obj._test_type[0] is not obj.__undef__:
            assert isinstance(obj._test_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._test_type[0], type(obj._test_type[0])))
            assert obj._test_type[0] in ['READ', 'WRITE', 'RANDREAD', 'RANDWRITE'], "Expected enum ['READ', 'WRITE', 'RANDREAD', 'RANDWRITE'] but got %s" % obj._test_type[0]
            common.validate_format(obj._test_type[0], "None", None, None)
        obj._jobs = (data.get("jobs", obj.__undef__), dirty)
        if obj._jobs[0] is not None and obj._jobs[0] is not obj.__undef__:
            assert isinstance(obj._jobs[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._jobs[0], type(obj._jobs[0])))
            common.validate_format(obj._jobs[0], "None", None, None)
        obj._block_size = (data.get("blockSize", obj.__undef__), dirty)
        if obj._block_size[0] is not None and obj._block_size[0] is not obj.__undef__:
            assert isinstance(obj._block_size[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._block_size[0], type(obj._block_size[0])))
            common.validate_format(obj._block_size[0], "None", None, None)
        obj._iops = (data.get("iops", obj.__undef__), dirty)
        if obj._iops[0] is not None and obj._iops[0] is not obj.__undef__:
            assert isinstance(obj._iops[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._iops[0], type(obj._iops[0])))
            common.validate_format(obj._iops[0], "None", None, None)
        obj._throughput = (data.get("throughput", obj.__undef__), dirty)
        if obj._throughput[0] is not None and obj._throughput[0] is not obj.__undef__:
            assert isinstance(obj._throughput[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._throughput[0], type(obj._throughput[0])))
            common.validate_format(obj._throughput[0], "None", None, None)
        obj._average_latency = (data.get("averageLatency", obj.__undef__), dirty)
        if obj._average_latency[0] is not None and obj._average_latency[0] is not obj.__undef__:
            assert isinstance(obj._average_latency[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._average_latency[0], type(obj._average_latency[0])))
            common.validate_format(obj._average_latency[0], "None", None, None)
        obj._min_latency = (data.get("minLatency", obj.__undef__), dirty)
        if obj._min_latency[0] is not None and obj._min_latency[0] is not obj.__undef__:
            assert isinstance(obj._min_latency[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._min_latency[0], type(obj._min_latency[0])))
            common.validate_format(obj._min_latency[0], "None", None, None)
        obj._max_latency = (data.get("maxLatency", obj.__undef__), dirty)
        if obj._max_latency[0] is not None and obj._max_latency[0] is not obj.__undef__:
            assert isinstance(obj._max_latency[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._max_latency[0], type(obj._max_latency[0])))
            common.validate_format(obj._max_latency[0], "None", None, None)
        obj._stddev_latency = (data.get("stddevLatency", obj.__undef__), dirty)
        if obj._stddev_latency[0] is not None and obj._stddev_latency[0] is not obj.__undef__:
            assert isinstance(obj._stddev_latency[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._stddev_latency[0], type(obj._stddev_latency[0])))
            common.validate_format(obj._stddev_latency[0], "None", None, None)
        obj._latency95th_percentile = (data.get("latency95thPercentile", obj.__undef__), dirty)
        if obj._latency95th_percentile[0] is not None and obj._latency95th_percentile[0] is not obj.__undef__:
            assert isinstance(obj._latency95th_percentile[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._latency95th_percentile[0], type(obj._latency95th_percentile[0])))
            common.validate_format(obj._latency95th_percentile[0], "None", None, None)
        obj._load_scaling = (data.get("loadScaling", obj.__undef__), dirty)
        if obj._load_scaling[0] is not None and obj._load_scaling[0] is not obj.__undef__:
            assert isinstance(obj._load_scaling[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._load_scaling[0], type(obj._load_scaling[0])))
            common.validate_format(obj._load_scaling[0], "None", None, None)
        obj._latency_grade = (data.get("latencyGrade", obj.__undef__), dirty)
        if obj._latency_grade[0] is not None and obj._latency_grade[0] is not obj.__undef__:
            assert isinstance(obj._latency_grade[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._latency_grade[0], type(obj._latency_grade[0])))
            common.validate_format(obj._latency_grade[0], "None", None, None)
        obj._load_scaling_grade = (data.get("loadScalingGrade", obj.__undef__), dirty)
        if obj._load_scaling_grade[0] is not None and obj._load_scaling_grade[0] is not obj.__undef__:
            assert isinstance(obj._load_scaling_grade[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._load_scaling_grade[0], type(obj._load_scaling_grade[0])))
            common.validate_format(obj._load_scaling_grade[0], "None", None, None)
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
        if "test_name" == "type" or (self.test_name is not self.__undef__ and (not (dirty and not self._test_name[1]))):
            dct["testName"] = dictify(self.test_name)
        if "test_type" == "type" or (self.test_type is not self.__undef__ and (not (dirty and not self._test_type[1]))):
            dct["testType"] = dictify(self.test_type)
        if "jobs" == "type" or (self.jobs is not self.__undef__ and (not (dirty and not self._jobs[1]))):
            dct["jobs"] = dictify(self.jobs)
        if "block_size" == "type" or (self.block_size is not self.__undef__ and (not (dirty and not self._block_size[1]))):
            dct["blockSize"] = dictify(self.block_size)
        if "iops" == "type" or (self.iops is not self.__undef__ and (not (dirty and not self._iops[1]))):
            dct["iops"] = dictify(self.iops)
        if "throughput" == "type" or (self.throughput is not self.__undef__ and (not (dirty and not self._throughput[1]))):
            dct["throughput"] = dictify(self.throughput)
        if "average_latency" == "type" or (self.average_latency is not self.__undef__ and (not (dirty and not self._average_latency[1]))):
            dct["averageLatency"] = dictify(self.average_latency)
        if "min_latency" == "type" or (self.min_latency is not self.__undef__ and (not (dirty and not self._min_latency[1]))):
            dct["minLatency"] = dictify(self.min_latency)
        if "max_latency" == "type" or (self.max_latency is not self.__undef__ and (not (dirty and not self._max_latency[1]))):
            dct["maxLatency"] = dictify(self.max_latency)
        if "stddev_latency" == "type" or (self.stddev_latency is not self.__undef__ and (not (dirty and not self._stddev_latency[1]))):
            dct["stddevLatency"] = dictify(self.stddev_latency)
        if "latency95th_percentile" == "type" or (self.latency95th_percentile is not self.__undef__ and (not (dirty and not self._latency95th_percentile[1]))):
            dct["latency95thPercentile"] = dictify(self.latency95th_percentile)
        if "load_scaling" == "type" or (self.load_scaling is not self.__undef__ and (not (dirty and not self._load_scaling[1]))):
            dct["loadScaling"] = dictify(self.load_scaling)
        if "latency_grade" == "type" or (self.latency_grade is not self.__undef__ and (not (dirty and not self._latency_grade[1]))):
            dct["latencyGrade"] = dictify(self.latency_grade)
        if "load_scaling_grade" == "type" or (self.load_scaling_grade is not self.__undef__ and (not (dirty and not self._load_scaling_grade[1]))):
            dct["loadScalingGrade"] = dictify(self.load_scaling_grade)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._test_name = (self._test_name[0], True)
        self._test_type = (self._test_type[0], True)
        self._jobs = (self._jobs[0], True)
        self._block_size = (self._block_size[0], True)
        self._iops = (self._iops[0], True)
        self._throughput = (self._throughput[0], True)
        self._average_latency = (self._average_latency[0], True)
        self._min_latency = (self._min_latency[0], True)
        self._max_latency = (self._max_latency[0], True)
        self._stddev_latency = (self._stddev_latency[0], True)
        self._latency95th_percentile = (self._latency95th_percentile[0], True)
        self._load_scaling = (self._load_scaling[0], True)
        self._latency_grade = (self._latency_grade[0], True)
        self._load_scaling_grade = (self._load_scaling_grade[0], True)

    def is_dirty(self):
        return any([self._test_name[1], self._test_type[1], self._jobs[1], self._block_size[1], self._iops[1], self._throughput[1], self._average_latency[1], self._min_latency[1], self._max_latency[1], self._stddev_latency[1], self._latency95th_percentile[1], self._load_scaling[1], self._latency_grade[1], self._load_scaling_grade[1]])

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
        if not isinstance(other, StorageTestResult):
            return False
        return super().__eq__(other) and \
               self.test_name == other.test_name and \
               self.test_type == other.test_type and \
               self.jobs == other.jobs and \
               self.block_size == other.block_size and \
               self.iops == other.iops and \
               self.throughput == other.throughput and \
               self.average_latency == other.average_latency and \
               self.min_latency == other.min_latency and \
               self.max_latency == other.max_latency and \
               self.stddev_latency == other.stddev_latency and \
               self.latency95th_percentile == other.latency95th_percentile and \
               self.load_scaling == other.load_scaling and \
               self.latency_grade == other.latency_grade and \
               self.load_scaling_grade == other.load_scaling_grade

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def test_name(self):
        """
        Name of the test for which the grade is assigned.

        :rtype: ``str``
        """
        return self._test_name[0]

    @test_name.setter
    def test_name(self, value):
        self._test_name = (value, True)

    @property
    def test_type(self):
        """
        The test type. *(permitted values: READ, WRITE, RANDREAD, RANDWRITE)*

        :rtype: ``str``
        """
        return self._test_type[0]

    @test_type.setter
    def test_type(self, value):
        self._test_type = (value, True)

    @property
    def jobs(self):
        """
        No of jobs/threads used.

        :rtype: ``int``
        """
        return self._jobs[0]

    @jobs.setter
    def jobs(self, value):
        self._jobs = (value, True)

    @property
    def block_size(self):
        """
        Block size used for the test.

        :rtype: ``int``
        """
        return self._block_size[0]

    @block_size.setter
    def block_size(self, value):
        self._block_size = (value, True)

    @property
    def iops(self):
        """
        IO operations per second.

        :rtype: ``int``
        """
        return self._iops[0]

    @iops.setter
    def iops(self, value):
        self._iops = (value, True)

    @property
    def throughput(self):
        """
        Throughput.

        :rtype: ``float``
        """
        return self._throughput[0]

    @throughput.setter
    def throughput(self, value):
        self._throughput = (value, True)

    @property
    def average_latency(self):
        """
        Average latency in milliseconds.

        :rtype: ``float``
        """
        return self._average_latency[0]

    @average_latency.setter
    def average_latency(self, value):
        self._average_latency = (value, True)

    @property
    def min_latency(self):
        """
        Minimum latency in milliseconds.

        :rtype: ``float``
        """
        return self._min_latency[0]

    @min_latency.setter
    def min_latency(self, value):
        self._min_latency = (value, True)

    @property
    def max_latency(self):
        """
        Maximum latency in milliseconds.

        :rtype: ``float``
        """
        return self._max_latency[0]

    @max_latency.setter
    def max_latency(self, value):
        self._max_latency = (value, True)

    @property
    def stddev_latency(self):
        """
        Standard deviation of latency in milliseconds.

        :rtype: ``float``
        """
        return self._stddev_latency[0]

    @stddev_latency.setter
    def stddev_latency(self, value):
        self._stddev_latency = (value, True)

    @property
    def latency95th_percentile(self):
        """
        95th percentile latency in milliseconds.

        :rtype: ``float``
        """
        return self._latency95th_percentile[0]

    @latency95th_percentile.setter
    def latency95th_percentile(self, value):
        self._latency95th_percentile = (value, True)

    @property
    def load_scaling(self):
        """
        Load scaling.

        :rtype: ``float``
        """
        return self._load_scaling[0]

    @load_scaling.setter
    def load_scaling(self, value):
        self._load_scaling = (value, True)

    @property
    def latency_grade(self):
        """
        Grade assigned to the test for latency.

        :rtype: ``str``
        """
        return self._latency_grade[0]

    @latency_grade.setter
    def latency_grade(self, value):
        self._latency_grade = (value, True)

    @property
    def load_scaling_grade(self):
        """
        Grade assigned to the test for load scaling.

        :rtype: ``str``
        """
        return self._load_scaling_grade[0]

    @load_scaling_grade.setter
    def load_scaling_grade(self, value):
        self._load_scaling_grade = (value, True)

