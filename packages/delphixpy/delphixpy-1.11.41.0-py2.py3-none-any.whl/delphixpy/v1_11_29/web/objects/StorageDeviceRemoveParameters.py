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
#     /delphix-storage-device-remove-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_29.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_29 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StorageDeviceRemoveParameters(PersistentObject):
    """
    *(extends* :py:class:`v1_11_29.web.vo.PersistentObject` *)* The parameters
    to use as input when removing devices.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StorageDeviceRemoveParameters", True)
        self._devices = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "devices" not in data:
            raise ValueError("Missing required property \"devices\".")
        obj._devices = []
        for item in data.get("devices") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "objectReference", None, None)
            obj._devices.append(item)
        obj._devices = (obj._devices, dirty)
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
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._devices = (self._devices[0], True)

    def is_dirty(self):
        return any([self._devices[1]])

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
        if not isinstance(other, StorageDeviceRemoveParameters):
            return False
        return super().__eq__(other) and \
               self.devices == other.devices

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def devices(self):
        """
        List of storage devices to be removed.

        :rtype: ``list`` of ``str``
        """
        return self._devices[0]

    @devices.setter
    def devices(self, value):
        self._devices = (value, True)

