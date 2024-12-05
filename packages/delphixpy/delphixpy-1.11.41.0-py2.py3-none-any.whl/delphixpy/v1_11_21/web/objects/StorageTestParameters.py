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
#     /delphix-storage-test-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StorageTestParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_21.web.vo.TypedObject` *)* Parameters used to
    execute a storage test.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StorageTestParameters", True)
        self._devices = (self.__undef__, True)
        self._duration = (self.__undef__, True)
        self._tests = (self.__undef__, True)
        self._test_region = (self.__undef__, True)
        self._initialize_devices = (self.__undef__, True)
        self._initialize_entire_device = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._devices = []
        for item in data.get("devices") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "objectReference", None, None)
            obj._devices.append(item)
        obj._devices = (obj._devices, dirty)
        obj._duration = (data.get("duration", obj.__undef__), dirty)
        if obj._duration[0] is not None and obj._duration[0] is not obj.__undef__:
            assert isinstance(obj._duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._duration[0], type(obj._duration[0])))
            common.validate_format(obj._duration[0], "None", None, None)
        obj._tests = (data.get("tests", obj.__undef__), dirty)
        if obj._tests[0] is not None and obj._tests[0] is not obj.__undef__:
            assert isinstance(obj._tests[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tests[0], type(obj._tests[0])))
            assert obj._tests[0] in ['ALL', 'MINIMAL', 'READ', 'WRITE', 'RANDREAD'], "Expected enum ['ALL', 'MINIMAL', 'READ', 'WRITE', 'RANDREAD'] but got %s" % obj._tests[0]
            common.validate_format(obj._tests[0], "None", None, None)
        obj._test_region = (data.get("testRegion", obj.__undef__), dirty)
        if obj._test_region[0] is not None and obj._test_region[0] is not obj.__undef__:
            assert isinstance(obj._test_region[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._test_region[0], type(obj._test_region[0])))
            common.validate_format(obj._test_region[0], "None", None, None)
        obj._initialize_devices = (data.get("initializeDevices", obj.__undef__), dirty)
        if obj._initialize_devices[0] is not None and obj._initialize_devices[0] is not obj.__undef__:
            assert isinstance(obj._initialize_devices[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._initialize_devices[0], type(obj._initialize_devices[0])))
            common.validate_format(obj._initialize_devices[0], "None", None, None)
        obj._initialize_entire_device = (data.get("initializeEntireDevice", obj.__undef__), dirty)
        if obj._initialize_entire_device[0] is not None and obj._initialize_entire_device[0] is not obj.__undef__:
            assert isinstance(obj._initialize_entire_device[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._initialize_entire_device[0], type(obj._initialize_entire_device[0])))
            common.validate_format(obj._initialize_entire_device[0], "None", None, None)
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
        if "devices" == "type" or (self.devices is not self.__undef__ and (not (dirty and not self._devices[1]) or self.is_dirty_list(self.devices, self._devices) or belongs_to_parent)):
            dct["devices"] = dictify(self.devices, prop_is_list_or_vo=True)
        if "duration" == "type" or (self.duration is not self.__undef__ and (not (dirty and not self._duration[1]) or self.is_dirty_list(self.duration, self._duration) or belongs_to_parent)):
            dct["duration"] = dictify(self.duration)
        elif belongs_to_parent and self.duration is self.__undef__:
            dct["duration"] = 120
        if "tests" == "type" or (self.tests is not self.__undef__ and (not (dirty and not self._tests[1]) or self.is_dirty_list(self.tests, self._tests) or belongs_to_parent)):
            dct["tests"] = dictify(self.tests)
        elif belongs_to_parent and self.tests is self.__undef__:
            dct["tests"] = "ALL"
        if "test_region" == "type" or (self.test_region is not self.__undef__ and (not (dirty and not self._test_region[1]) or self.is_dirty_list(self.test_region, self._test_region) or belongs_to_parent)):
            dct["testRegion"] = dictify(self.test_region)
        elif belongs_to_parent and self.test_region is self.__undef__:
            dct["testRegion"] = 549755813888
        if "initialize_devices" == "type" or (self.initialize_devices is not self.__undef__ and (not (dirty and not self._initialize_devices[1]) or self.is_dirty_list(self.initialize_devices, self._initialize_devices) or belongs_to_parent)):
            dct["initializeDevices"] = dictify(self.initialize_devices)
        elif belongs_to_parent and self.initialize_devices is self.__undef__:
            dct["initializeDevices"] = True
        if "initialize_entire_device" == "type" or (self.initialize_entire_device is not self.__undef__ and (not (dirty and not self._initialize_entire_device[1]) or self.is_dirty_list(self.initialize_entire_device, self._initialize_entire_device) or belongs_to_parent)):
            dct["initializeEntireDevice"] = dictify(self.initialize_entire_device)
        elif belongs_to_parent and self.initialize_entire_device is self.__undef__:
            dct["initializeEntireDevice"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._devices = (self._devices[0], True)
        self._duration = (self._duration[0], True)
        self._tests = (self._tests[0], True)
        self._test_region = (self._test_region[0], True)
        self._initialize_devices = (self._initialize_devices[0], True)
        self._initialize_entire_device = (self._initialize_entire_device[0], True)

    def is_dirty(self):
        return any([self._devices[1], self._duration[1], self._tests[1], self._test_region[1], self._initialize_devices[1], self._initialize_entire_device[1]])

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
        if not isinstance(other, StorageTestParameters):
            return False
        return super().__eq__(other) and \
               self.devices == other.devices and \
               self.duration == other.duration and \
               self.tests == other.tests and \
               self.test_region == other.test_region and \
               self.initialize_devices == other.initialize_devices and \
               self.initialize_entire_device == other.initialize_entire_device

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def devices(self):
        """
        The list of devices to be used for the test.

        :rtype: ``list`` of ``str``
        """
        return self._devices[0]

    @devices.setter
    def devices(self, value):
        self._devices = (value, True)

    @property
    def duration(self):
        """
        *(default value: 120)* Run time of each test, in seconds.

        :rtype: ``int``
        """
        return self._duration[0]

    @duration.setter
    def duration(self, value):
        self._duration = (value, True)

    @property
    def tests(self):
        """
        *(default value: ALL)* The tests that are to be run. *(permitted
        values: ALL, MINIMAL, READ, WRITE, RANDREAD)*

        :rtype: ``str``
        """
        return self._tests[0]

    @tests.setter
    def tests(self, value):
        self._tests = (value, True)

    @property
    def test_region(self):
        """
        *(default value: 549755813888)* Total disk space, spread over all
        devices, used by the test (in bytes).

        :rtype: ``float``
        """
        return self._test_region[0]

    @test_region.setter
    def test_region(self, value):
        self._test_region = (value, True)

    @property
    def initialize_devices(self):
        """
        *(default value: True)* True if the disks should be initialized prior
        to running the benchmark.

        :rtype: ``bool``
        """
        return self._initialize_devices[0]

    @initialize_devices.setter
    def initialize_devices(self, value):
        self._initialize_devices = (value, True)

    @property
    def initialize_entire_device(self):
        """
        True if the entire disk should be initialized prior to running the
        benchmark.

        :rtype: ``bool``
        """
        return self._initialize_entire_device[0]

    @initialize_entire_device.setter
    def initialize_entire_device(self, value):
        self._initialize_entire_device = (value, True)

