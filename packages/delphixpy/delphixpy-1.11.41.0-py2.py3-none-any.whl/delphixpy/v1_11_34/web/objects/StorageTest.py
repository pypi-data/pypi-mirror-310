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
#     /delphix-storage-test.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.ReadonlyNamedUserObject import ReadonlyNamedUserObject
from delphixpy.v1_11_34 import factory
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StorageTest(ReadonlyNamedUserObject):
    """
    *(extends* :py:class:`v1_11_34.web.vo.ReadonlyNamedUserObject` *)* Test the
    performance of storage devices.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StorageTest", True)
        self._state = (self.__undef__, True)
        self._parameters = (self.__undef__, True)
        self._test_results = (self.__undef__, True)
        self._start_time = (self.__undef__, True)
        self._end_time = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._state = (data.get("state", obj.__undef__), dirty)
        if obj._state[0] is not None and obj._state[0] is not obj.__undef__:
            assert isinstance(obj._state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state[0], type(obj._state[0])))
            assert obj._state[0] in ['WAITING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELED'], "Expected enum ['WAITING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELED'] but got %s" % obj._state[0]
            common.validate_format(obj._state[0], "None", None, None)
        if "parameters" in data and data["parameters"] is not None:
            obj._parameters = (factory.create_object(data["parameters"], "StorageTestParameters"), dirty)
            factory.validate_type(obj._parameters[0], "StorageTestParameters")
        else:
            obj._parameters = (obj.__undef__, dirty)
        obj._test_results = []
        for item in data.get("testResults") or []:
            obj._test_results.append(factory.create_object(item))
            factory.validate_type(obj._test_results[-1], "StorageTestResult")
        obj._test_results = (obj._test_results, dirty)
        obj._start_time = (data.get("startTime", obj.__undef__), dirty)
        if obj._start_time[0] is not None and obj._start_time[0] is not obj.__undef__:
            assert isinstance(obj._start_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_time[0], type(obj._start_time[0])))
            common.validate_format(obj._start_time[0], "date", None, None)
        obj._end_time = (data.get("endTime", obj.__undef__), dirty)
        if obj._end_time[0] is not None and obj._end_time[0] is not obj.__undef__:
            assert isinstance(obj._end_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._end_time[0], type(obj._end_time[0])))
            common.validate_format(obj._end_time[0], "date", None, None)
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
        if "parameters" == "type" or (self.parameters is not self.__undef__ and (not (dirty and not self._parameters[1]))):
            dct["parameters"] = dictify(self.parameters)
        if "test_results" == "type" or (self.test_results is not self.__undef__ and (not (dirty and not self._test_results[1]))):
            dct["testResults"] = dictify(self.test_results)
        if "start_time" == "type" or (self.start_time is not self.__undef__ and (not (dirty and not self._start_time[1]))):
            dct["startTime"] = dictify(self.start_time)
        if "end_time" == "type" or (self.end_time is not self.__undef__ and (not (dirty and not self._end_time[1]))):
            dct["endTime"] = dictify(self.end_time)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._state = (self._state[0], True)
        self._parameters = (self._parameters[0], True)
        self._test_results = (self._test_results[0], True)
        self._start_time = (self._start_time[0], True)
        self._end_time = (self._end_time[0], True)

    def is_dirty(self):
        return any([self._state[1], self._parameters[1], self._test_results[1], self._start_time[1], self._end_time[1]])

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
        if not isinstance(other, StorageTest):
            return False
        return super().__eq__(other) and \
               self.state == other.state and \
               self.parameters == other.parameters and \
               self.test_results == other.test_results and \
               self.start_time == other.start_time and \
               self.end_time == other.end_time

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def state(self):
        """
        The state of the test. *(permitted values: WAITING, RUNNING, COMPLETED,
        FAILED, CANCELED)*

        :rtype: ``str``
        """
        return self._state[0]

    @state.setter
    def state(self, value):
        self._state = (value, True)

    @property
    def parameters(self):
        """
        The parameters used to execute the test.

        :rtype: :py:class:`v1_11_34.web.vo.StorageTestParameters`
        """
        return self._parameters[0]

    @parameters.setter
    def parameters(self, value):
        self._parameters = (value, True)

    @property
    def test_results(self):
        """
        The results assigned to various tests.

        :rtype: ``list`` of :py:class:`v1_11_34.web.vo.StorageTestResult`
        """
        return self._test_results[0]

    @test_results.setter
    def test_results(self, value):
        self._test_results = (value, True)

    @property
    def start_time(self):
        """
        Time when the test was started.

        :rtype: ``str``
        """
        return self._start_time[0]

    @start_time.setter
    def start_time(self, value):
        self._start_time = (value, True)

    @property
    def end_time(self):
        """
        Time when the test ended.

        :rtype: ``str``
        """
        return self._end_time[0]

    @end_time.setter
    def end_time(self, value):
        self._end_time = (value, True)

