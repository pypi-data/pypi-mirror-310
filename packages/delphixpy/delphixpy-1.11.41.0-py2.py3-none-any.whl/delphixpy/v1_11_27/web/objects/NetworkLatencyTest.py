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
#     /delphix-network-latency-test.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.NetworkTest import NetworkTest
from delphixpy.v1_11_27 import factory
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class NetworkLatencyTest(NetworkTest):
    """
    *(extends* :py:class:`v1_11_27.web.vo.NetworkTest` *)* Round-trip latency
    tests to a target system.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("NetworkLatencyTest", True)
        self._parameters = (self.__undef__, True)
        self._minimum = (self.__undef__, True)
        self._maximum = (self.__undef__, True)
        self._average = (self.__undef__, True)
        self._stddev = (self.__undef__, True)
        self._loss = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "parameters" in data and data["parameters"] is not None:
            obj._parameters = (factory.create_object(data["parameters"], "NetworkLatencyTestParameters"), dirty)
            factory.validate_type(obj._parameters[0], "NetworkLatencyTestParameters")
        else:
            obj._parameters = (obj.__undef__, dirty)
        obj._minimum = (data.get("minimum", obj.__undef__), dirty)
        if obj._minimum[0] is not None and obj._minimum[0] is not obj.__undef__:
            assert isinstance(obj._minimum[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._minimum[0], type(obj._minimum[0])))
            common.validate_format(obj._minimum[0], "None", None, None)
        obj._maximum = (data.get("maximum", obj.__undef__), dirty)
        if obj._maximum[0] is not None and obj._maximum[0] is not obj.__undef__:
            assert isinstance(obj._maximum[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._maximum[0], type(obj._maximum[0])))
            common.validate_format(obj._maximum[0], "None", None, None)
        obj._average = (data.get("average", obj.__undef__), dirty)
        if obj._average[0] is not None and obj._average[0] is not obj.__undef__:
            assert isinstance(obj._average[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._average[0], type(obj._average[0])))
            common.validate_format(obj._average[0], "None", None, None)
        obj._stddev = (data.get("stddev", obj.__undef__), dirty)
        if obj._stddev[0] is not None and obj._stddev[0] is not obj.__undef__:
            assert isinstance(obj._stddev[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._stddev[0], type(obj._stddev[0])))
            common.validate_format(obj._stddev[0], "None", None, None)
        obj._loss = (data.get("loss", obj.__undef__), dirty)
        if obj._loss[0] is not None and obj._loss[0] is not obj.__undef__:
            assert isinstance(obj._loss[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._loss[0], type(obj._loss[0])))
            common.validate_format(obj._loss[0], "None", None, None)
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
        if "parameters" == "type" or (self.parameters is not self.__undef__ and (not (dirty and not self._parameters[1]))):
            dct["parameters"] = dictify(self.parameters)
        if "minimum" == "type" or (self.minimum is not self.__undef__ and (not (dirty and not self._minimum[1]))):
            dct["minimum"] = dictify(self.minimum)
        if "maximum" == "type" or (self.maximum is not self.__undef__ and (not (dirty and not self._maximum[1]))):
            dct["maximum"] = dictify(self.maximum)
        if "average" == "type" or (self.average is not self.__undef__ and (not (dirty and not self._average[1]))):
            dct["average"] = dictify(self.average)
        if "stddev" == "type" or (self.stddev is not self.__undef__ and (not (dirty and not self._stddev[1]))):
            dct["stddev"] = dictify(self.stddev)
        if "loss" == "type" or (self.loss is not self.__undef__ and (not (dirty and not self._loss[1]))):
            dct["loss"] = dictify(self.loss)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._parameters = (self._parameters[0], True)
        self._minimum = (self._minimum[0], True)
        self._maximum = (self._maximum[0], True)
        self._average = (self._average[0], True)
        self._stddev = (self._stddev[0], True)
        self._loss = (self._loss[0], True)

    def is_dirty(self):
        return any([self._parameters[1], self._minimum[1], self._maximum[1], self._average[1], self._stddev[1], self._loss[1]])

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
        if not isinstance(other, NetworkLatencyTest):
            return False
        return super().__eq__(other) and \
               self.parameters == other.parameters and \
               self.minimum == other.minimum and \
               self.maximum == other.maximum and \
               self.average == other.average and \
               self.stddev == other.stddev and \
               self.loss == other.loss

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def parameters(self):
        """
        The parameters used to execute the test.

        :rtype: :py:class:`v1_11_27.web.vo.NetworkLatencyTestParameters`
        """
        return self._parameters[0]

    @parameters.setter
    def parameters(self, value):
        self._parameters = (value, True)

    @property
    def minimum(self):
        """
        Minimum measured round-trip time (usec).

        :rtype: ``int``
        """
        return self._minimum[0]

    @minimum.setter
    def minimum(self, value):
        self._minimum = (value, True)

    @property
    def maximum(self):
        """
        Maximum measured round-trip time (usec).

        :rtype: ``int``
        """
        return self._maximum[0]

    @maximum.setter
    def maximum(self, value):
        self._maximum = (value, True)

    @property
    def average(self):
        """
        Average measured round-trip time (usec).

        :rtype: ``int``
        """
        return self._average[0]

    @average.setter
    def average(self, value):
        self._average = (value, True)

    @property
    def stddev(self):
        """
        Standard deviation (usec).

        :rtype: ``int``
        """
        return self._stddev[0]

    @stddev.setter
    def stddev(self, value):
        self._stddev = (value, True)

    @property
    def loss(self):
        """
        Percentage of requests or replies lost.

        :rtype: ``int``
        """
        return self._loss[0]

    @loss.setter
    def loss(self, value):
        self._loss = (value, True)

