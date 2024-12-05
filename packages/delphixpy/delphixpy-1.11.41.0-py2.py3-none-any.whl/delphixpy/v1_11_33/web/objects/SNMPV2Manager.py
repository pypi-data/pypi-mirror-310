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
#     /delphix-snmp-v2-manager.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_33.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_33 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SNMPV2Manager(PersistentObject):
    """
    *(extends* :py:class:`v1_11_33.web.vo.PersistentObject` *)* SNMP manager
    configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SNMPV2Manager", True)
        self._address = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._community_string = (self.__undef__, True)
        self._last_send_status = (self.__undef__, True)
        self._use_inform = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._address = (data.get("address", obj.__undef__), dirty)
        if obj._address[0] is not None and obj._address[0] is not obj.__undef__:
            assert isinstance(obj._address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._address[0], type(obj._address[0])))
            common.validate_format(obj._address[0], "host", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        obj._community_string = (data.get("communityString", obj.__undef__), dirty)
        if obj._community_string[0] is not None and obj._community_string[0] is not obj.__undef__:
            assert isinstance(obj._community_string[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._community_string[0], type(obj._community_string[0])))
            common.validate_format(obj._community_string[0], "None", None, None)
        obj._last_send_status = (data.get("lastSendStatus", obj.__undef__), dirty)
        if obj._last_send_status[0] is not None and obj._last_send_status[0] is not obj.__undef__:
            assert isinstance(obj._last_send_status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_send_status[0], type(obj._last_send_status[0])))
            assert obj._last_send_status[0] in ['FAILED', 'SUCCEEDED', 'PENDING', 'UNCHECKED'], "Expected enum ['FAILED', 'SUCCEEDED', 'PENDING', 'UNCHECKED'] but got %s" % obj._last_send_status[0]
            common.validate_format(obj._last_send_status[0], "None", None, None)
        obj._use_inform = (data.get("useInform", obj.__undef__), dirty)
        if obj._use_inform[0] is not None and obj._use_inform[0] is not obj.__undef__:
            assert isinstance(obj._use_inform[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._use_inform[0], type(obj._use_inform[0])))
            common.validate_format(obj._use_inform[0], "None", None, None)
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
        if "address" == "type" or (self.address is not self.__undef__ and (not (dirty and not self._address[1]) or self.is_dirty_list(self.address, self._address) or belongs_to_parent)):
            dct["address"] = dictify(self.address)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        elif belongs_to_parent and self.port is self.__undef__:
            dct["port"] = 162
        if "community_string" == "type" or (self.community_string is not self.__undef__ and (not (dirty and not self._community_string[1]) or self.is_dirty_list(self.community_string, self._community_string) or belongs_to_parent)):
            dct["communityString"] = dictify(self.community_string)
        if "last_send_status" == "type" or (self.last_send_status is not self.__undef__ and (not (dirty and not self._last_send_status[1]))):
            dct["lastSendStatus"] = dictify(self.last_send_status)
        if dirty and "lastSendStatus" in dct:
            del dct["lastSendStatus"]
        if "use_inform" == "type" or (self.use_inform is not self.__undef__ and (not (dirty and not self._use_inform[1]) or self.is_dirty_list(self.use_inform, self._use_inform) or belongs_to_parent)):
            dct["useInform"] = dictify(self.use_inform)
        elif belongs_to_parent and self.use_inform is self.__undef__:
            dct["useInform"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._address = (self._address[0], True)
        self._port = (self._port[0], True)
        self._community_string = (self._community_string[0], True)
        self._last_send_status = (self._last_send_status[0], True)
        self._use_inform = (self._use_inform[0], True)

    def is_dirty(self):
        return any([self._address[1], self._port[1], self._community_string[1], self._last_send_status[1], self._use_inform[1]])

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
        if not isinstance(other, SNMPV2Manager):
            return False
        return super().__eq__(other) and \
               self.address == other.address and \
               self.port == other.port and \
               self.community_string == other.community_string and \
               self.last_send_status == other.last_send_status and \
               self.use_inform == other.use_inform

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def address(self):
        """
        SNMP manager host.

        :rtype: ``str``
        """
        return self._address[0]

    @address.setter
    def address(self, value):
        self._address = (value, True)

    @property
    def port(self):
        """
        *(default value: 162)* SNMP manager port number.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def community_string(self):
        """
        SNMP manager community string.

        :rtype: ``str``
        """
        return self._community_string[0]

    @community_string.setter
    def community_string(self, value):
        self._community_string = (value, True)

    @property
    def last_send_status(self):
        """
        *(default value: PENDING)* Describes if the most recent attempt to send
        a trap succeeded or failed. *(permitted values: FAILED, SUCCEEDED,
        PENDING, UNCHECKED)*

        :rtype: ``str``
        """
        return self._last_send_status[0]

    @property
    def use_inform(self):
        """
        True if INFORM messages are to be sent to this manager, false for TRAP
        messages.

        :rtype: ``bool``
        """
        return self._use_inform[0]

    @use_inform.setter
    def use_inform(self, value):
        self._use_inform = (value, True)

