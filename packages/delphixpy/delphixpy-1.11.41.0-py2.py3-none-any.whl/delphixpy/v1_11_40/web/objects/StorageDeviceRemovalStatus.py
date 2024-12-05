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
#     /delphix-storage-device-removal-status.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StorageDeviceRemovalStatus(TypedObject):
    """
    *(extends* :py:class:`v1_11_40.web.vo.TypedObject` *)* Remove storage
    devices and view the status of device removal operations.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StorageDeviceRemovalStatus", True)
        self._state = (self.__undef__, True)
        self._copied = (self.__undef__, True)
        self._total = (self.__undef__, True)
        self._start_time = (self.__undef__, True)
        self._mapping_memory = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._state = (data.get("state", obj.__undef__), dirty)
        if obj._state[0] is not None and obj._state[0] is not obj.__undef__:
            assert isinstance(obj._state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state[0], type(obj._state[0])))
            assert obj._state[0] in ['NONE', 'ACTIVE', 'COMPLETED', 'CANCELED'], "Expected enum ['NONE', 'ACTIVE', 'COMPLETED', 'CANCELED'] but got %s" % obj._state[0]
            common.validate_format(obj._state[0], "None", None, None)
        obj._copied = (data.get("copied", obj.__undef__), dirty)
        if obj._copied[0] is not None and obj._copied[0] is not obj.__undef__:
            assert isinstance(obj._copied[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._copied[0], type(obj._copied[0])))
            common.validate_format(obj._copied[0], "None", None, None)
        obj._total = (data.get("total", obj.__undef__), dirty)
        if obj._total[0] is not None and obj._total[0] is not obj.__undef__:
            assert isinstance(obj._total[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._total[0], type(obj._total[0])))
            common.validate_format(obj._total[0], "None", None, None)
        obj._start_time = (data.get("startTime", obj.__undef__), dirty)
        if obj._start_time[0] is not None and obj._start_time[0] is not obj.__undef__:
            assert isinstance(obj._start_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_time[0], type(obj._start_time[0])))
            common.validate_format(obj._start_time[0], "date", None, None)
        obj._mapping_memory = (data.get("mappingMemory", obj.__undef__), dirty)
        if obj._mapping_memory[0] is not None and obj._mapping_memory[0] is not obj.__undef__:
            assert isinstance(obj._mapping_memory[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._mapping_memory[0], type(obj._mapping_memory[0])))
            common.validate_format(obj._mapping_memory[0], "None", None, None)
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
        if "copied" == "type" or (self.copied is not self.__undef__ and (not (dirty and not self._copied[1]))):
            dct["copied"] = dictify(self.copied)
        if "total" == "type" or (self.total is not self.__undef__ and (not (dirty and not self._total[1]))):
            dct["total"] = dictify(self.total)
        if "start_time" == "type" or (self.start_time is not self.__undef__ and (not (dirty and not self._start_time[1]))):
            dct["startTime"] = dictify(self.start_time)
        if "mapping_memory" == "type" or (self.mapping_memory is not self.__undef__ and (not (dirty and not self._mapping_memory[1]))):
            dct["mappingMemory"] = dictify(self.mapping_memory)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._state = (self._state[0], True)
        self._copied = (self._copied[0], True)
        self._total = (self._total[0], True)
        self._start_time = (self._start_time[0], True)
        self._mapping_memory = (self._mapping_memory[0], True)

    def is_dirty(self):
        return any([self._state[1], self._copied[1], self._total[1], self._start_time[1], self._mapping_memory[1]])

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
        if not isinstance(other, StorageDeviceRemovalStatus):
            return False
        return super().__eq__(other) and \
               self.state == other.state and \
               self.copied == other.copied and \
               self.total == other.total and \
               self.start_time == other.start_time and \
               self.mapping_memory == other.mapping_memory

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def state(self):
        """
        Removal state. *(permitted values: NONE, ACTIVE, COMPLETED, CANCELED)*

        :rtype: ``str``
        """
        return self._state[0]

    @state.setter
    def state(self, value):
        self._state = (value, True)

    @property
    def copied(self):
        """
        Amount of data removed, in bytes.

        :rtype: ``float``
        """
        return self._copied[0]

    @copied.setter
    def copied(self, value):
        self._copied = (value, True)

    @property
    def total(self):
        """
        Total amount of data to remove (including completed), in bytes.

        :rtype: ``float``
        """
        return self._total[0]

    @total.setter
    def total(self, value):
        self._total = (value, True)

    @property
    def start_time(self):
        """
        Time removal was started.

        :rtype: ``str``
        """
        return self._start_time[0]

    @start_time.setter
    def start_time(self, value):
        self._start_time = (value, True)

    @property
    def mapping_memory(self):
        """
        Memory used to account for removed devices, in bytes.

        :rtype: ``float``
        """
        return self._mapping_memory[0]

    @mapping_memory.setter
    def mapping_memory(self, value):
        self._mapping_memory = (value, True)

