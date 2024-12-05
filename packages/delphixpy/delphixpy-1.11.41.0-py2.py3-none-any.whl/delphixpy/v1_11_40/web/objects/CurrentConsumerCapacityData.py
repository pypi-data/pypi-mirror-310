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
#     /delphix-capacity-current-consumer-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.BaseConsumerCapacityData import BaseConsumerCapacityData
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CurrentConsumerCapacityData(BaseConsumerCapacityData):
    """
    *(extends* :py:class:`v1_11_40.web.vo.BaseConsumerCapacityData` *)* Current
    data about a particular capacity consumer.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CurrentConsumerCapacityData", True)
        self._storage_container = (self.__undef__, True)
        self._multi_owner = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._storage_container = (data.get("storageContainer", obj.__undef__), dirty)
        if obj._storage_container[0] is not None and obj._storage_container[0] is not obj.__undef__:
            assert isinstance(obj._storage_container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._storage_container[0], type(obj._storage_container[0])))
            common.validate_format(obj._storage_container[0], "None", None, None)
        obj._multi_owner = (data.get("multiOwner", obj.__undef__), dirty)
        if obj._multi_owner[0] is not None and obj._multi_owner[0] is not obj.__undef__:
            assert isinstance(obj._multi_owner[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._multi_owner[0], type(obj._multi_owner[0])))
            common.validate_format(obj._multi_owner[0], "None", None, None)
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
        if "storage_container" == "type" or (self.storage_container is not self.__undef__ and (not (dirty and not self._storage_container[1]))):
            dct["storageContainer"] = dictify(self.storage_container)
        if "multi_owner" == "type" or (self.multi_owner is not self.__undef__ and (not (dirty and not self._multi_owner[1]))):
            dct["multiOwner"] = dictify(self.multi_owner)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._storage_container = (self._storage_container[0], True)
        self._multi_owner = (self._multi_owner[0], True)

    def is_dirty(self):
        return any([self._storage_container[1], self._multi_owner[1]])

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
        if not isinstance(other, CurrentConsumerCapacityData):
            return False
        return super().__eq__(other) and \
               self.storage_container == other.storage_container and \
               self.multi_owner == other.multi_owner

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def storage_container(self):
        """
        Internal unique identifier for this consumer.

        :rtype: ``str``
        """
        return self._storage_container[0]

    @storage_container.setter
    def storage_container(self, value):
        self._storage_container = (value, True)

    @property
    def multi_owner(self):
        """
        Flag indicating whether this consumer is sharing filesystem with
        another consumer.

        :rtype: ``bool``
        """
        return self._multi_owner[0]

    @multi_owner.setter
    def multi_owner(self, value):
        self._multi_owner = (value, True)

