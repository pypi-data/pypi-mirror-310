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
#     /delphix-preprovisioning-runtime.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PreProvisioningRuntime(TypedObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TypedObject` *)* Runtime properties
    for pre-provisioning of a MSSQL database container.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PreProvisioningRuntime", True)
        self._pre_provisioning_state = (self.__undef__, True)
        self._last_update_timestamp = (self.__undef__, True)
        self._status = (self.__undef__, True)
        self._response = (self.__undef__, True)
        self._pending_action = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._pre_provisioning_state = (data.get("preProvisioningState", obj.__undef__), dirty)
        if obj._pre_provisioning_state[0] is not None and obj._pre_provisioning_state[0] is not obj.__undef__:
            assert isinstance(obj._pre_provisioning_state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pre_provisioning_state[0], type(obj._pre_provisioning_state[0])))
            assert obj._pre_provisioning_state[0] in ['ACTIVE', 'INACTIVE', 'FAULTED', 'UNKNOWN'], "Expected enum ['ACTIVE', 'INACTIVE', 'FAULTED', 'UNKNOWN'] but got %s" % obj._pre_provisioning_state[0]
            common.validate_format(obj._pre_provisioning_state[0], "None", None, None)
        obj._last_update_timestamp = (data.get("lastUpdateTimestamp", obj.__undef__), dirty)
        if obj._last_update_timestamp[0] is not None and obj._last_update_timestamp[0] is not obj.__undef__:
            assert isinstance(obj._last_update_timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_update_timestamp[0], type(obj._last_update_timestamp[0])))
            common.validate_format(obj._last_update_timestamp[0], "None", None, None)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            common.validate_format(obj._status[0], "None", None, None)
        obj._response = (data.get("response", obj.__undef__), dirty)
        if obj._response[0] is not None and obj._response[0] is not obj.__undef__:
            assert isinstance(obj._response[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._response[0], type(obj._response[0])))
            common.validate_format(obj._response[0], "None", None, None)
        obj._pending_action = (data.get("pendingAction", obj.__undef__), dirty)
        if obj._pending_action[0] is not None and obj._pending_action[0] is not obj.__undef__:
            assert isinstance(obj._pending_action[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pending_action[0], type(obj._pending_action[0])))
            common.validate_format(obj._pending_action[0], "None", None, None)
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
        if "pre_provisioning_state" == "type" or (self.pre_provisioning_state is not self.__undef__ and (not (dirty and not self._pre_provisioning_state[1]))):
            dct["preProvisioningState"] = dictify(self.pre_provisioning_state)
        if "last_update_timestamp" == "type" or (self.last_update_timestamp is not self.__undef__ and (not (dirty and not self._last_update_timestamp[1]))):
            dct["lastUpdateTimestamp"] = dictify(self.last_update_timestamp)
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        if "response" == "type" or (self.response is not self.__undef__ and (not (dirty and not self._response[1]))):
            dct["response"] = dictify(self.response)
        if "pending_action" == "type" or (self.pending_action is not self.__undef__ and (not (dirty and not self._pending_action[1]))):
            dct["pendingAction"] = dictify(self.pending_action)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._pre_provisioning_state = (self._pre_provisioning_state[0], True)
        self._last_update_timestamp = (self._last_update_timestamp[0], True)
        self._status = (self._status[0], True)
        self._response = (self._response[0], True)
        self._pending_action = (self._pending_action[0], True)

    def is_dirty(self):
        return any([self._pre_provisioning_state[1], self._last_update_timestamp[1], self._status[1], self._response[1], self._pending_action[1]])

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
        if not isinstance(other, PreProvisioningRuntime):
            return False
        return super().__eq__(other) and \
               self.pre_provisioning_state == other.pre_provisioning_state and \
               self.last_update_timestamp == other.last_update_timestamp and \
               self.status == other.status and \
               self.response == other.response and \
               self.pending_action == other.pending_action

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def pre_provisioning_state(self):
        """
        Indicates the current state of pre-provisioning for the database.
        *(permitted values: ACTIVE, INACTIVE, FAULTED, UNKNOWN)*

        :rtype: ``str``
        """
        return self._pre_provisioning_state[0]

    @pre_provisioning_state.setter
    def pre_provisioning_state(self, value):
        self._pre_provisioning_state = (value, True)

    @property
    def last_update_timestamp(self):
        """
        Timestamp of the last update to the status.

        :rtype: ``str``
        """
        return self._last_update_timestamp[0]

    @last_update_timestamp.setter
    def last_update_timestamp(self, value):
        self._last_update_timestamp = (value, True)

    @property
    def status(self):
        """
        The status of the pre-provisioning run.

        :rtype: ``str``
        """
        return self._status[0]

    @status.setter
    def status(self, value):
        self._status = (value, True)

    @property
    def response(self):
        """
        Response taken based on the status of the pre-provisioning run.

        :rtype: ``str``
        """
        return self._response[0]

    @response.setter
    def response(self, value):
        self._response = (value, True)

    @property
    def pending_action(self):
        """
        User action required to resolve any error that the pre-provisioning run
        encountered.

        :rtype: ``str``
        """
        return self._pending_action[0]

    @pending_action.setter
    def pending_action(self, value):
        self._pending_action = (value, True)

