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
#     /delphix-analytics-tcp-stats-datapoint-stream.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_4.web.objects.DatapointStream import DatapointStream
from delphixpy.v1_11_4 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TCPStatsDatapointStream(DatapointStream):
    """
    *(extends* :py:class:`v1_11_4.web.vo.DatapointStream` *)* A stream of
    datapoints from a TCP_STATS analytics slice.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TCPStatsDatapointStream", True)
        self._local_address = (self.__undef__, True)
        self._remote_address = (self.__undef__, True)
        self._local_port = (self.__undef__, True)
        self._remote_port = (self.__undef__, True)
        self._service = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._local_address = (data.get("localAddress", obj.__undef__), dirty)
        if obj._local_address[0] is not None and obj._local_address[0] is not obj.__undef__:
            assert isinstance(obj._local_address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._local_address[0], type(obj._local_address[0])))
            common.validate_format(obj._local_address[0], "ipAddress", None, None)
        obj._remote_address = (data.get("remoteAddress", obj.__undef__), dirty)
        if obj._remote_address[0] is not None and obj._remote_address[0] is not obj.__undef__:
            assert isinstance(obj._remote_address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._remote_address[0], type(obj._remote_address[0])))
            common.validate_format(obj._remote_address[0], "ipAddress", None, None)
        obj._local_port = (data.get("localPort", obj.__undef__), dirty)
        if obj._local_port[0] is not None and obj._local_port[0] is not obj.__undef__:
            assert isinstance(obj._local_port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._local_port[0], type(obj._local_port[0])))
            common.validate_format(obj._local_port[0], "None", None, None)
        obj._remote_port = (data.get("remotePort", obj.__undef__), dirty)
        if obj._remote_port[0] is not None and obj._remote_port[0] is not obj.__undef__:
            assert isinstance(obj._remote_port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._remote_port[0], type(obj._remote_port[0])))
            common.validate_format(obj._remote_port[0], "None", None, None)
        obj._service = (data.get("service", obj.__undef__), dirty)
        if obj._service[0] is not None and obj._service[0] is not obj.__undef__:
            assert isinstance(obj._service[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._service[0], type(obj._service[0])))
            common.validate_format(obj._service[0], "None", None, None)
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
        if "local_address" == "type" or (self.local_address is not self.__undef__ and (not (dirty and not self._local_address[1]))):
            dct["localAddress"] = dictify(self.local_address)
        if "remote_address" == "type" or (self.remote_address is not self.__undef__ and (not (dirty and not self._remote_address[1]))):
            dct["remoteAddress"] = dictify(self.remote_address)
        if "local_port" == "type" or (self.local_port is not self.__undef__ and (not (dirty and not self._local_port[1]))):
            dct["localPort"] = dictify(self.local_port)
        if "remote_port" == "type" or (self.remote_port is not self.__undef__ and (not (dirty and not self._remote_port[1]))):
            dct["remotePort"] = dictify(self.remote_port)
        if "service" == "type" or (self.service is not self.__undef__ and (not (dirty and not self._service[1]))):
            dct["service"] = dictify(self.service)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._local_address = (self._local_address[0], True)
        self._remote_address = (self._remote_address[0], True)
        self._local_port = (self._local_port[0], True)
        self._remote_port = (self._remote_port[0], True)
        self._service = (self._service[0], True)

    def is_dirty(self):
        return any([self._local_address[1], self._remote_address[1], self._local_port[1], self._remote_port[1], self._service[1]])

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
        if not isinstance(other, TCPStatsDatapointStream):
            return False
        return super().__eq__(other) and \
               self.local_address == other.local_address and \
               self.remote_address == other.remote_address and \
               self.local_port == other.local_port and \
               self.remote_port == other.remote_port and \
               self.service == other.service

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def local_address(self):
        """
        The local Delphix Engine IP address.

        :rtype: ``str``
        """
        return self._local_address[0]

    @local_address.setter
    def local_address(self, value):
        self._local_address = (value, True)

    @property
    def remote_address(self):
        """
        The remote IP address.

        :rtype: ``str``
        """
        return self._remote_address[0]

    @remote_address.setter
    def remote_address(self, value):
        self._remote_address = (value, True)

    @property
    def local_port(self):
        """
        The local TCP port number.

        :rtype: ``int``
        """
        return self._local_port[0]

    @local_port.setter
    def local_port(self, value):
        self._local_port = (value, True)

    @property
    def remote_port(self):
        """
        The remote TCP port number.

        :rtype: ``int``
        """
        return self._remote_port[0]

    @remote_port.setter
    def remote_port(self, value):
        self._remote_port = (value, True)

    @property
    def service(self):
        """
        The network service.

        :rtype: ``str``
        """
        return self._service[0]

    @service.setter
    def service(self, value):
        self._service = (value, True)

