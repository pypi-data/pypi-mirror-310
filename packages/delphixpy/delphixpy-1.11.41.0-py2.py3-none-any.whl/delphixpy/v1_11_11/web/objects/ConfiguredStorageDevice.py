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
#     /delphix-configured-storage-device.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.StorageDevice import StorageDevice
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ConfiguredStorageDevice(StorageDevice):
    """
    *(extends* :py:class:`v1_11_11.web.vo.StorageDevice` *)* A storage device
    configured as usable storage.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ConfiguredStorageDevice", True)
        self._expandable_size = (self.__undef__, True)
        self._used_size = (self.__undef__, True)
        self._boot_device = (self.__undef__, True)
        self._fragmentation = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._expandable_size = (data.get("expandableSize", obj.__undef__), dirty)
        if obj._expandable_size[0] is not None and obj._expandable_size[0] is not obj.__undef__:
            assert isinstance(obj._expandable_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._expandable_size[0], type(obj._expandable_size[0])))
            common.validate_format(obj._expandable_size[0], "None", None, None)
        obj._used_size = (data.get("usedSize", obj.__undef__), dirty)
        if obj._used_size[0] is not None and obj._used_size[0] is not obj.__undef__:
            assert isinstance(obj._used_size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._used_size[0], type(obj._used_size[0])))
            common.validate_format(obj._used_size[0], "None", None, None)
        obj._boot_device = (data.get("bootDevice", obj.__undef__), dirty)
        if obj._boot_device[0] is not None and obj._boot_device[0] is not obj.__undef__:
            assert isinstance(obj._boot_device[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._boot_device[0], type(obj._boot_device[0])))
            common.validate_format(obj._boot_device[0], "None", None, None)
        obj._fragmentation = (data.get("fragmentation", obj.__undef__), dirty)
        if obj._fragmentation[0] is not None and obj._fragmentation[0] is not obj.__undef__:
            assert isinstance(obj._fragmentation[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._fragmentation[0], type(obj._fragmentation[0])))
            common.validate_format(obj._fragmentation[0], "None", None, None)
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
        if "expandable_size" == "type" or (self.expandable_size is not self.__undef__ and (not (dirty and not self._expandable_size[1]))):
            dct["expandableSize"] = dictify(self.expandable_size)
        if "used_size" == "type" or (self.used_size is not self.__undef__ and (not (dirty and not self._used_size[1]))):
            dct["usedSize"] = dictify(self.used_size)
        if "boot_device" == "type" or (self.boot_device is not self.__undef__ and (not (dirty and not self._boot_device[1]))):
            dct["bootDevice"] = dictify(self.boot_device)
        if "fragmentation" == "type" or (self.fragmentation is not self.__undef__ and (not (dirty and not self._fragmentation[1]))):
            dct["fragmentation"] = dictify(self.fragmentation)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._expandable_size = (self._expandable_size[0], True)
        self._used_size = (self._used_size[0], True)
        self._boot_device = (self._boot_device[0], True)
        self._fragmentation = (self._fragmentation[0], True)

    def is_dirty(self):
        return any([self._expandable_size[1], self._used_size[1], self._boot_device[1], self._fragmentation[1]])

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
        if not isinstance(other, ConfiguredStorageDevice):
            return False
        return super().__eq__(other) and \
               self.expandable_size == other.expandable_size and \
               self.used_size == other.used_size and \
               self.boot_device == other.boot_device and \
               self.fragmentation == other.fragmentation

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def expandable_size(self):
        """
        Amount of additional space that would be made available, if the device
        is expanded.

        :rtype: ``float``
        """
        return self._expandable_size[0]

    @expandable_size.setter
    def expandable_size(self, value):
        self._expandable_size = (value, True)

    @property
    def used_size(self):
        """
        Size of allocated space on the device.

        :rtype: ``float``
        """
        return self._used_size[0]

    @used_size.setter
    def used_size(self, value):
        self._used_size = (value, True)

    @property
    def boot_device(self):
        """
        Boolean value indicating if this is a boot device.

        :rtype: ``bool``
        """
        return self._boot_device[0]

    @boot_device.setter
    def boot_device(self, value):
        self._boot_device = (value, True)

    @property
    def fragmentation(self):
        """
        Percent fragmentation for this device.

        :rtype: ``str``
        """
        return self._fragmentation[0]

    @fragmentation.setter
    def fragmentation(self, value):
        self._fragmentation = (value, True)

