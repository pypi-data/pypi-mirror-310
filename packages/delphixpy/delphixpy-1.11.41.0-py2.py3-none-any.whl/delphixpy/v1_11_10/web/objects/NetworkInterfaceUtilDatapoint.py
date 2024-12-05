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
#     /delphix-analytics-network-interface-util-datapoint.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_10.web.objects.Datapoint import Datapoint
from delphixpy.v1_11_10 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class NetworkInterfaceUtilDatapoint(Datapoint):
    """
    *(extends* :py:class:`v1_11_10.web.vo.Datapoint` *)* An analytics datapoint
    generated by the NETWORK_INTERFACE_UTIL statistic type.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("NetworkInterfaceUtilDatapoint", True)
        self._in_bytes = (self.__undef__, True)
        self._in_packets = (self.__undef__, True)
        self._out_bytes = (self.__undef__, True)
        self._out_packets = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._in_bytes = (data.get("inBytes", obj.__undef__), dirty)
        if obj._in_bytes[0] is not None and obj._in_bytes[0] is not obj.__undef__:
            assert isinstance(obj._in_bytes[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._in_bytes[0], type(obj._in_bytes[0])))
            common.validate_format(obj._in_bytes[0], "None", None, None)
        obj._in_packets = (data.get("inPackets", obj.__undef__), dirty)
        if obj._in_packets[0] is not None and obj._in_packets[0] is not obj.__undef__:
            assert isinstance(obj._in_packets[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._in_packets[0], type(obj._in_packets[0])))
            common.validate_format(obj._in_packets[0], "None", None, None)
        obj._out_bytes = (data.get("outBytes", obj.__undef__), dirty)
        if obj._out_bytes[0] is not None and obj._out_bytes[0] is not obj.__undef__:
            assert isinstance(obj._out_bytes[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._out_bytes[0], type(obj._out_bytes[0])))
            common.validate_format(obj._out_bytes[0], "None", None, None)
        obj._out_packets = (data.get("outPackets", obj.__undef__), dirty)
        if obj._out_packets[0] is not None and obj._out_packets[0] is not obj.__undef__:
            assert isinstance(obj._out_packets[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._out_packets[0], type(obj._out_packets[0])))
            common.validate_format(obj._out_packets[0], "None", None, None)
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
        if "in_bytes" == "type" or (self.in_bytes is not self.__undef__ and (not (dirty and not self._in_bytes[1]))):
            dct["inBytes"] = dictify(self.in_bytes)
        if "in_packets" == "type" or (self.in_packets is not self.__undef__ and (not (dirty and not self._in_packets[1]))):
            dct["inPackets"] = dictify(self.in_packets)
        if "out_bytes" == "type" or (self.out_bytes is not self.__undef__ and (not (dirty and not self._out_bytes[1]))):
            dct["outBytes"] = dictify(self.out_bytes)
        if "out_packets" == "type" or (self.out_packets is not self.__undef__ and (not (dirty and not self._out_packets[1]))):
            dct["outPackets"] = dictify(self.out_packets)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._in_bytes = (self._in_bytes[0], True)
        self._in_packets = (self._in_packets[0], True)
        self._out_bytes = (self._out_bytes[0], True)
        self._out_packets = (self._out_packets[0], True)

    def is_dirty(self):
        return any([self._in_bytes[1], self._in_packets[1], self._out_bytes[1], self._out_packets[1]])

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
        if not isinstance(other, NetworkInterfaceUtilDatapoint):
            return False
        return super().__eq__(other) and \
               self.in_bytes == other.in_bytes and \
               self.in_packets == other.in_packets and \
               self.out_bytes == other.out_bytes and \
               self.out_packets == other.out_packets

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def in_bytes(self):
        """
        Bytes received on the interface.

        :rtype: ``int``
        """
        return self._in_bytes[0]

    @in_bytes.setter
    def in_bytes(self, value):
        self._in_bytes = (value, True)

    @property
    def in_packets(self):
        """
        Packets received on the interface.

        :rtype: ``int``
        """
        return self._in_packets[0]

    @in_packets.setter
    def in_packets(self, value):
        self._in_packets = (value, True)

    @property
    def out_bytes(self):
        """
        Bytes transmitted on the interface.

        :rtype: ``int``
        """
        return self._out_bytes[0]

    @out_bytes.setter
    def out_bytes(self, value):
        self._out_bytes = (value, True)

    @property
    def out_packets(self):
        """
        Packets transmitted on the interface.

        :rtype: ``int``
        """
        return self._out_packets[0]

    @out_packets.setter
    def out_packets(self, value):
        self._out_packets = (value, True)

