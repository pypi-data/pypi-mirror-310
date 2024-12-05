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
#     /delphix-ase-staging-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_22.web.objects.ASESource import ASESource
from delphixpy.v1_11_22 import factory
from delphixpy.v1_11_22 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ASEStagingSource(ASESource):
    """
    *(extends* :py:class:`v1_11_22.web.vo.ASESource` *)* An SAP ASE staging
    source used for validated sync..
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ASEStagingSource", True)
        self._mount_base = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._runtime_mount_information = (self.__undef__, True)
        self._locked = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._mount_base = (data.get("mountBase", obj.__undef__), dirty)
        if obj._mount_base[0] is not None and obj._mount_base[0] is not obj.__undef__:
            assert isinstance(obj._mount_base[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_base[0], type(obj._mount_base[0])))
            common.validate_format(obj._mount_base[0], "None", None, 87)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "StagingSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "StagingSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        if "runtimeMountInformation" in data and data["runtimeMountInformation"] is not None:
            obj._runtime_mount_information = (factory.create_object(data["runtimeMountInformation"], "RuntimeMountInformation"), dirty)
            factory.validate_type(obj._runtime_mount_information[0], "RuntimeMountInformation")
        else:
            obj._runtime_mount_information = (obj.__undef__, dirty)
        obj._locked = (data.get("locked", obj.__undef__), dirty)
        if obj._locked[0] is not None and obj._locked[0] is not obj.__undef__:
            assert isinstance(obj._locked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._locked[0], type(obj._locked[0])))
            common.validate_format(obj._locked[0], "None", None, None)
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
        if "mount_base" == "type" or (self.mount_base is not self.__undef__ and (not (dirty and not self._mount_base[1]) or self.is_dirty_list(self.mount_base, self._mount_base) or belongs_to_parent)):
            dct["mountBase"] = dictify(self.mount_base)
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "runtime_mount_information" == "type" or (self.runtime_mount_information is not self.__undef__ and (not (dirty and not self._runtime_mount_information[1]))):
            dct["runtimeMountInformation"] = dictify(self.runtime_mount_information)
        if dirty and "runtimeMountInformation" in dct:
            del dct["runtimeMountInformation"]
        if "locked" == "type" or (self.locked is not self.__undef__ and (not (dirty and not self._locked[1]))):
            dct["locked"] = dictify(self.locked)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._mount_base = (self._mount_base[0], True)
        self._operations = (self._operations[0], True)
        self._runtime_mount_information = (self._runtime_mount_information[0], True)
        self._locked = (self._locked[0], True)

    def is_dirty(self):
        return any([self._mount_base[1], self._operations[1], self._runtime_mount_information[1], self._locked[1]])

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
        if not isinstance(other, ASEStagingSource):
            return False
        return super().__eq__(other) and \
               self.mount_base == other.mount_base and \
               self.operations == other.operations and \
               self.runtime_mount_information == other.runtime_mount_information and \
               self.locked == other.locked

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def mount_base(self):
        """
        The base mount point for the NFS mounts.

        :rtype: ``str``
        """
        return self._mount_base[0]

    @mount_base.setter
    def mount_base(self, value):
        self._mount_base = (value, True)

    @property
    def operations(self):
        """
        User-specified hook operations for this staging source.

        :rtype: :py:class:`v1_11_22.web.vo.StagingSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

    @property
    def runtime_mount_information(self):
        """
        The representation of runtime mount information.

        :rtype: :py:class:`v1_11_22.web.vo.RuntimeMountInformation`
        """
        return self._runtime_mount_information[0]

    @property
    def locked(self):
        """
        Whether the source is protected from deletion and other data-losing
        actions.

        :rtype: ``bool``
        """
        return self._locked[0]

    @locked.setter
    def locked(self, value):
        self._locked = (value, True)

