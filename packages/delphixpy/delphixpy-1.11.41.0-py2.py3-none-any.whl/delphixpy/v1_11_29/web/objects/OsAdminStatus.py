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
#     /delphix-osadmin-status.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_29.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_29 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OsAdminStatus(TypedObject):
    """
    *(extends* :py:class:`v1_11_29.web.vo.TypedObject` *)* Information for the
    current state of the Delphix Engine.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OsAdminStatus", True)
        self._services = (self.__undef__, True)
        self._engine_configured = (self.__undef__, True)
        self._storage_pool_state = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._services = (data.get("services", obj.__undef__), dirty)
        if obj._services[0] is not None and obj._services[0] is not obj.__undef__:
            assert isinstance(obj._services[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._services[0], type(obj._services[0])))
            common.validate_format(obj._services[0], "None", None, None)
        obj._engine_configured = (data.get("engineConfigured", obj.__undef__), dirty)
        if obj._engine_configured[0] is not None and obj._engine_configured[0] is not obj.__undef__:
            assert isinstance(obj._engine_configured[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._engine_configured[0], type(obj._engine_configured[0])))
            common.validate_format(obj._engine_configured[0], "None", None, None)
        obj._storage_pool_state = (data.get("storagePoolState", obj.__undef__), dirty)
        if obj._storage_pool_state[0] is not None and obj._storage_pool_state[0] is not obj.__undef__:
            assert isinstance(obj._storage_pool_state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._storage_pool_state[0], type(obj._storage_pool_state[0])))
            assert obj._storage_pool_state[0] in ['UNINITIALIZED', 'IMPORTED', 'FAILED'], "Expected enum ['UNINITIALIZED', 'IMPORTED', 'FAILED'] but got %s" % obj._storage_pool_state[0]
            common.validate_format(obj._storage_pool_state[0], "None", None, None)
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
        if "services" == "type" or (self.services is not self.__undef__ and (not (dirty and not self._services[1]))):
            dct["services"] = dictify(self.services)
        if "engine_configured" == "type" or (self.engine_configured is not self.__undef__ and (not (dirty and not self._engine_configured[1]))):
            dct["engineConfigured"] = dictify(self.engine_configured)
        if "storage_pool_state" == "type" or (self.storage_pool_state is not self.__undef__ and (not (dirty and not self._storage_pool_state[1]))):
            dct["storagePoolState"] = dictify(self.storage_pool_state)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._services = (self._services[0], True)
        self._engine_configured = (self._engine_configured[0], True)
        self._storage_pool_state = (self._storage_pool_state[0], True)

    def is_dirty(self):
        return any([self._services[1], self._engine_configured[1], self._storage_pool_state[1]])

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
        if not isinstance(other, OsAdminStatus):
            return False
        return super().__eq__(other) and \
               self.services == other.services and \
               self.engine_configured == other.engine_configured and \
               self.storage_pool_state == other.storage_pool_state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def services(self):
        """
        List of services and their status.

        :rtype: ``dict``
        """
        return self._services[0]

    @services.setter
    def services(self, value):
        self._services = (value, True)

    @property
    def engine_configured(self):
        """
        Engine configured.

        :rtype: ``bool``
        """
        return self._engine_configured[0]

    @engine_configured.setter
    def engine_configured(self, value):
        self._engine_configured = (value, True)

    @property
    def storage_pool_state(self):
        """
        The state of the storage pool. *(permitted values: UNINITIALIZED,
        IMPORTED, FAILED)*

        :rtype: ``str``
        """
        return self._storage_pool_state[0]

    @storage_pool_state.setter
    def storage_pool_state(self, value):
        self._storage_pool_state = (value, True)

