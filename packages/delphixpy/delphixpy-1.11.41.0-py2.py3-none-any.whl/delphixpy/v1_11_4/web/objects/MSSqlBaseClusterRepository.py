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
#     /delphix-mssql-base-cluster-repository.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_4.web.objects.MSSqlRepository import MSSqlRepository
from delphixpy.v1_11_4 import factory
from delphixpy.v1_11_4 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlBaseClusterRepository(MSSqlRepository):
    """
    *(extends* :py:class:`v1_11_4.web.vo.MSSqlRepository` *)* The
    representation of a SQL Server Cluster repository.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlBaseClusterRepository", True)
        self._instances = (self.__undef__, True)
        self._listeners = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._instances = []
        for item in data.get("instances") or []:
            obj._instances.append(factory.create_object(item))
            factory.validate_type(obj._instances[-1], "MSSqlBaseClusterInstance")
        obj._instances = (obj._instances, dirty)
        obj._listeners = []
        for item in data.get("listeners") or []:
            obj._listeners.append(factory.create_object(item))
            factory.validate_type(obj._listeners[-1], "MSSqlBaseClusterListener")
        obj._listeners = (obj._listeners, dirty)
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
        if "instances" == "type" or (self.instances is not self.__undef__ and (not (dirty and not self._instances[1]))):
            dct["instances"] = dictify(self.instances)
        if "listeners" == "type" or (self.listeners is not self.__undef__ and (not (dirty and not self._listeners[1]))):
            dct["listeners"] = dictify(self.listeners)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._instances = (self._instances[0], True)
        self._listeners = (self._listeners[0], True)

    def is_dirty(self):
        return any([self._instances[1], self._listeners[1]])

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
        if not isinstance(other, MSSqlBaseClusterRepository):
            return False
        return super().__eq__(other) and \
               self.instances == other.instances and \
               self.listeners == other.listeners

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def instances(self):
        """
        The list of MSSQL Cluster instances belonging to this repository.

        :rtype: ``list`` of :py:class:`v1_11_4.web.vo.MSSqlBaseClusterInstance`
        """
        return self._instances[0]

    @instances.setter
    def instances(self, value):
        self._instances = (value, True)

    @property
    def listeners(self):
        """
        The list of listeners belonging to this repository.

        :rtype: ``list`` of :py:class:`v1_11_4.web.vo.MSSqlBaseClusterListener`
        """
        return self._listeners[0]

    @listeners.setter
    def listeners(self, value):
        self._listeners = (value, True)

