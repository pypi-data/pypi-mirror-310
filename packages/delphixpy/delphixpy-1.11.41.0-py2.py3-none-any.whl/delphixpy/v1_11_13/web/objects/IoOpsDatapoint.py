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
#     /delphix-analytics-io-ops-datapoint.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_13.web.objects.Datapoint import Datapoint
from delphixpy.v1_11_13 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class IoOpsDatapoint(Datapoint):
    """
    *(extends* :py:class:`v1_11_13.web.vo.Datapoint` *)* An analytics datapoint
    generated by the DISK_OPS, DxFS_OPS, DxFS_IO_QUEUE_OPS, iSCSI_OPS, NFS_OPS,
    or VFS_OPS statistic types.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("IoOpsDatapoint", True)
        self._latency = (self.__undef__, True)
        self._avg_latency = (self.__undef__, True)
        self._size = (self.__undef__, True)
        self._throughput = (self.__undef__, True)
        self._count = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._latency = (data.get("latency", obj.__undef__), dirty)
        if obj._latency[0] is not None and obj._latency[0] is not obj.__undef__:
            assert isinstance(obj._latency[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._latency[0], type(obj._latency[0])))
            common.validate_format(obj._latency[0], "None", None, None)
        obj._avg_latency = (data.get("avgLatency", obj.__undef__), dirty)
        if obj._avg_latency[0] is not None and obj._avg_latency[0] is not obj.__undef__:
            assert isinstance(obj._avg_latency[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._avg_latency[0], type(obj._avg_latency[0])))
            common.validate_format(obj._avg_latency[0], "None", None, None)
        obj._size = (data.get("size", obj.__undef__), dirty)
        if obj._size[0] is not None and obj._size[0] is not obj.__undef__:
            assert isinstance(obj._size[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._size[0], type(obj._size[0])))
            common.validate_format(obj._size[0], "None", None, None)
        obj._throughput = (data.get("throughput", obj.__undef__), dirty)
        if obj._throughput[0] is not None and obj._throughput[0] is not obj.__undef__:
            assert isinstance(obj._throughput[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._throughput[0], type(obj._throughput[0])))
            common.validate_format(obj._throughput[0], "None", None, None)
        obj._count = (data.get("count", obj.__undef__), dirty)
        if obj._count[0] is not None and obj._count[0] is not obj.__undef__:
            assert isinstance(obj._count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._count[0], type(obj._count[0])))
            common.validate_format(obj._count[0], "None", None, None)
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
        if "latency" == "type" or (self.latency is not self.__undef__ and (not (dirty and not self._latency[1]))):
            dct["latency"] = dictify(self.latency)
        if "avg_latency" == "type" or (self.avg_latency is not self.__undef__ and (not (dirty and not self._avg_latency[1]))):
            dct["avgLatency"] = dictify(self.avg_latency)
        if "size" == "type" or (self.size is not self.__undef__ and (not (dirty and not self._size[1]))):
            dct["size"] = dictify(self.size)
        if "throughput" == "type" or (self.throughput is not self.__undef__ and (not (dirty and not self._throughput[1]))):
            dct["throughput"] = dictify(self.throughput)
        if "count" == "type" or (self.count is not self.__undef__ and (not (dirty and not self._count[1]))):
            dct["count"] = dictify(self.count)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._latency = (self._latency[0], True)
        self._avg_latency = (self._avg_latency[0], True)
        self._size = (self._size[0], True)
        self._throughput = (self._throughput[0], True)
        self._count = (self._count[0], True)

    def is_dirty(self):
        return any([self._latency[1], self._avg_latency[1], self._size[1], self._throughput[1], self._count[1]])

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
        if not isinstance(other, IoOpsDatapoint):
            return False
        return super().__eq__(other) and \
               self.latency == other.latency and \
               self.avg_latency == other.avg_latency and \
               self.size == other.size and \
               self.throughput == other.throughput and \
               self.count == other.count

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def latency(self):
        """
        I/O latencies in nanoseconds.

        :rtype: ``dict``
        """
        return self._latency[0]

    @latency.setter
    def latency(self, value):
        self._latency = (value, True)

    @property
    def avg_latency(self):
        """
        Average I/O latency in nanoseconds.

        :rtype: ``int``
        """
        return self._avg_latency[0]

    @avg_latency.setter
    def avg_latency(self, value):
        self._avg_latency = (value, True)

    @property
    def size(self):
        """
        I/O sizes in bytes.

        :rtype: ``dict``
        """
        return self._size[0]

    @size.setter
    def size(self, value):
        self._size = (value, True)

    @property
    def throughput(self):
        """
        I/O throughput in bytes.

        :rtype: ``int``
        """
        return self._throughput[0]

    @throughput.setter
    def throughput(self, value):
        self._throughput = (value, True)

    @property
    def count(self):
        """
        Number of I/O operations.

        :rtype: ``int``
        """
        return self._count[0]

    @count.setter
    def count(self, value):
        self._count = (value, True)

