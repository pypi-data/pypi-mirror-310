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
#     /delphix-container-utilization-interval.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_2.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_2 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ContainerUtilizationInterval(TypedObject):
    """
    *(extends* :py:class:`v1_11_2.web.vo.TypedObject` *)* Represents a
    represents an interval of time with which container utilization statistics
    are associated.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ContainerUtilizationInterval", True)
        self._timestamp = (self.__undef__, True)
        self._average_throughput = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._timestamp = (data.get("timestamp", obj.__undef__), dirty)
        if obj._timestamp[0] is not None and obj._timestamp[0] is not obj.__undef__:
            assert isinstance(obj._timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._timestamp[0], type(obj._timestamp[0])))
            common.validate_format(obj._timestamp[0], "date", None, None)
        obj._average_throughput = (data.get("averageThroughput", obj.__undef__), dirty)
        if obj._average_throughput[0] is not None and obj._average_throughput[0] is not obj.__undef__:
            assert isinstance(obj._average_throughput[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._average_throughput[0], type(obj._average_throughput[0])))
            common.validate_format(obj._average_throughput[0], "None", None, None)
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
        if "timestamp" == "type" or (self.timestamp is not self.__undef__ and (not (dirty and not self._timestamp[1]))):
            dct["timestamp"] = dictify(self.timestamp)
        if "average_throughput" == "type" or (self.average_throughput is not self.__undef__ and (not (dirty and not self._average_throughput[1]))):
            dct["averageThroughput"] = dictify(self.average_throughput)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._timestamp = (self._timestamp[0], True)
        self._average_throughput = (self._average_throughput[0], True)

    def is_dirty(self):
        return any([self._timestamp[1], self._average_throughput[1]])

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
        if not isinstance(other, ContainerUtilizationInterval):
            return False
        return super().__eq__(other) and \
               self.timestamp == other.timestamp and \
               self.average_throughput == other.average_throughput

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def timestamp(self):
        """
        The start time of the interval.

        :rtype: ``str``
        """
        return self._timestamp[0]

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = (value, True)

    @property
    def average_throughput(self):
        """
        The average throughput for the container throughout the duration of the
        sampling interval, measured in kilobits per second.

        :rtype: ``float``
        """
        return self._average_throughput[0]

    @average_throughput.setter
    def average_throughput(self, value):
        self._average_throughput = (value, True)

