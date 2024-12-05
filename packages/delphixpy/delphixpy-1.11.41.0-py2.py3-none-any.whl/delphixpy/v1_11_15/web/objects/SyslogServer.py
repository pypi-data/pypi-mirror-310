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
#     /delphix-syslog-server.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_15.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_15 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SyslogServer(TypedObject):
    """
    *(extends* :py:class:`v1_11_15.web.vo.TypedObject` *)* Syslog server
    configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SyslogServer", True)
        self._protocol = (self.__undef__, True)
        self._address = (self.__undef__, True)
        self._port = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "protocol" not in data:
            raise ValueError("Missing required property \"protocol\".")
        obj._protocol = (data.get("protocol", obj.__undef__), dirty)
        if obj._protocol[0] is not None and obj._protocol[0] is not obj.__undef__:
            assert isinstance(obj._protocol[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._protocol[0], type(obj._protocol[0])))
            assert obj._protocol[0] in ['udp', 'tcp'], "Expected enum ['udp', 'tcp'] but got %s" % obj._protocol[0]
            common.validate_format(obj._protocol[0], "None", None, None)
        if "address" not in data:
            raise ValueError("Missing required property \"address\".")
        obj._address = (data.get("address", obj.__undef__), dirty)
        if obj._address[0] is not None and obj._address[0] is not obj.__undef__:
            assert isinstance(obj._address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._address[0], type(obj._address[0])))
            common.validate_format(obj._address[0], "host", None, None)
        if "port" not in data:
            raise ValueError("Missing required property \"port\".")
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
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
        if "protocol" == "type" or (self.protocol is not self.__undef__ and (not (dirty and not self._protocol[1]) or self.is_dirty_list(self.protocol, self._protocol) or belongs_to_parent)):
            dct["protocol"] = dictify(self.protocol)
        if "address" == "type" or (self.address is not self.__undef__ and (not (dirty and not self._address[1]) or self.is_dirty_list(self.address, self._address) or belongs_to_parent)):
            dct["address"] = dictify(self.address)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._protocol = (self._protocol[0], True)
        self._address = (self._address[0], True)
        self._port = (self._port[0], True)

    def is_dirty(self):
        return any([self._protocol[1], self._address[1], self._port[1]])

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
        if not isinstance(other, SyslogServer):
            return False
        return super().__eq__(other) and \
               self.protocol == other.protocol and \
               self.address == other.address and \
               self.port == other.port

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def protocol(self):
        """
        *(default value: udp)* Syslog transport protocol. *(permitted values:
        udp, tcp)*

        :rtype: ``str``
        """
        return self._protocol[0]

    @protocol.setter
    def protocol(self, value):
        self._protocol = (value, True)

    @property
    def address(self):
        """
        Syslog host name or IP address.

        :rtype: ``str``
        """
        return self._address[0]

    @address.setter
    def address(self, value):
        self._address = (value, True)

    @property
    def port(self):
        """
        *(default value: 514)* Syslog port number.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

