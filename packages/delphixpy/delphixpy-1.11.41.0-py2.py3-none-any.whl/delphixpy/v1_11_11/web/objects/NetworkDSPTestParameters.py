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
#     /delphix-network-dsp-test-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.NetworkThroughputTestBaseParameters import NetworkThroughputTestBaseParameters
from delphixpy.v1_11_11 import factory
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class NetworkDSPTestParameters(NetworkThroughputTestBaseParameters):
    """
    *(extends* :py:class:`v1_11_11.web.vo.NetworkThroughputTestBaseParameters`
    *)* Parameters used to execute a network throughput test using the Delphix
    Session Protocol.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("NetworkDSPTestParameters", True)
        self._destination_type = (self.__undef__, True)
        self._remote_delphix_engine_info = (self.__undef__, True)
        self._compression = (self.__undef__, True)
        self._encryption = (self.__undef__, True)
        self._queue_depth = (self.__undef__, True)
        self._block_size = (self.__undef__, True)
        self._send_socket_buffer = (self.__undef__, True)
        self._receive_socket_buffer = (self.__undef__, True)
        self._xport_scheduler = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._destination_type = (data.get("destinationType", obj.__undef__), dirty)
        if obj._destination_type[0] is not None and obj._destination_type[0] is not obj.__undef__:
            assert isinstance(obj._destination_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._destination_type[0], type(obj._destination_type[0])))
            assert obj._destination_type[0] in ['REMOTE_HOST', 'DELPHIX_ENGINE'], "Expected enum ['REMOTE_HOST', 'DELPHIX_ENGINE'] but got %s" % obj._destination_type[0]
            common.validate_format(obj._destination_type[0], "None", None, None)
        if "remoteDelphixEngineInfo" in data and data["remoteDelphixEngineInfo"] is not None:
            obj._remote_delphix_engine_info = (factory.create_object(data["remoteDelphixEngineInfo"], "RemoteDelphixEngineInfo"), dirty)
            factory.validate_type(obj._remote_delphix_engine_info[0], "RemoteDelphixEngineInfo")
        else:
            obj._remote_delphix_engine_info = (obj.__undef__, dirty)
        obj._compression = (data.get("compression", obj.__undef__), dirty)
        if obj._compression[0] is not None and obj._compression[0] is not obj.__undef__:
            assert isinstance(obj._compression[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._compression[0], type(obj._compression[0])))
            common.validate_format(obj._compression[0], "None", None, None)
        obj._encryption = (data.get("encryption", obj.__undef__), dirty)
        if obj._encryption[0] is not None and obj._encryption[0] is not obj.__undef__:
            assert isinstance(obj._encryption[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._encryption[0], type(obj._encryption[0])))
            common.validate_format(obj._encryption[0], "None", None, None)
        obj._queue_depth = (data.get("queueDepth", obj.__undef__), dirty)
        if obj._queue_depth[0] is not None and obj._queue_depth[0] is not obj.__undef__:
            assert isinstance(obj._queue_depth[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._queue_depth[0], type(obj._queue_depth[0])))
            common.validate_format(obj._queue_depth[0], "None", None, None)
        obj._block_size = (data.get("blockSize", obj.__undef__), dirty)
        if obj._block_size[0] is not None and obj._block_size[0] is not obj.__undef__:
            assert isinstance(obj._block_size[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._block_size[0], type(obj._block_size[0])))
            common.validate_format(obj._block_size[0], "None", None, None)
        obj._send_socket_buffer = (data.get("sendSocketBuffer", obj.__undef__), dirty)
        if obj._send_socket_buffer[0] is not None and obj._send_socket_buffer[0] is not obj.__undef__:
            assert isinstance(obj._send_socket_buffer[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._send_socket_buffer[0], type(obj._send_socket_buffer[0])))
            common.validate_format(obj._send_socket_buffer[0], "None", None, None)
        obj._receive_socket_buffer = (data.get("receiveSocketBuffer", obj.__undef__), dirty)
        if obj._receive_socket_buffer[0] is not None and obj._receive_socket_buffer[0] is not obj.__undef__:
            assert isinstance(obj._receive_socket_buffer[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._receive_socket_buffer[0], type(obj._receive_socket_buffer[0])))
            common.validate_format(obj._receive_socket_buffer[0], "None", None, None)
        obj._xport_scheduler = (data.get("xportScheduler", obj.__undef__), dirty)
        if obj._xport_scheduler[0] is not None and obj._xport_scheduler[0] is not obj.__undef__:
            assert isinstance(obj._xport_scheduler[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._xport_scheduler[0], type(obj._xport_scheduler[0])))
            assert obj._xport_scheduler[0] in ['ROUND_ROBIN', 'LEAST_QUEUE'], "Expected enum ['ROUND_ROBIN', 'LEAST_QUEUE'] but got %s" % obj._xport_scheduler[0]
            common.validate_format(obj._xport_scheduler[0], "None", None, None)
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
        if "destination_type" == "type" or (self.destination_type is not self.__undef__ and (not (dirty and not self._destination_type[1]) or self.is_dirty_list(self.destination_type, self._destination_type) or belongs_to_parent)):
            dct["destinationType"] = dictify(self.destination_type)
        elif belongs_to_parent and self.destination_type is self.__undef__:
            dct["destinationType"] = "REMOTE_HOST"
        if "remote_delphix_engine_info" == "type" or (self.remote_delphix_engine_info is not self.__undef__ and (not (dirty and not self._remote_delphix_engine_info[1]) or self.is_dirty_list(self.remote_delphix_engine_info, self._remote_delphix_engine_info) or belongs_to_parent)):
            dct["remoteDelphixEngineInfo"] = dictify(self.remote_delphix_engine_info, prop_is_list_or_vo=True)
        if "compression" == "type" or (self.compression is not self.__undef__ and (not (dirty and not self._compression[1]) or self.is_dirty_list(self.compression, self._compression) or belongs_to_parent)):
            dct["compression"] = dictify(self.compression)
        elif belongs_to_parent and self.compression is self.__undef__:
            dct["compression"] = False
        if "encryption" == "type" or (self.encryption is not self.__undef__ and (not (dirty and not self._encryption[1]) or self.is_dirty_list(self.encryption, self._encryption) or belongs_to_parent)):
            dct["encryption"] = dictify(self.encryption)
        elif belongs_to_parent and self.encryption is self.__undef__:
            dct["encryption"] = False
        if "queue_depth" == "type" or (self.queue_depth is not self.__undef__ and (not (dirty and not self._queue_depth[1]) or self.is_dirty_list(self.queue_depth, self._queue_depth) or belongs_to_parent)):
            dct["queueDepth"] = dictify(self.queue_depth)
        elif belongs_to_parent and self.queue_depth is self.__undef__:
            dct["queueDepth"] = 32
        if "block_size" == "type" or (self.block_size is not self.__undef__ and (not (dirty and not self._block_size[1]) or self.is_dirty_list(self.block_size, self._block_size) or belongs_to_parent)):
            dct["blockSize"] = dictify(self.block_size)
        elif belongs_to_parent and self.block_size is self.__undef__:
            dct["blockSize"] = 65536
        if "send_socket_buffer" == "type" or (self.send_socket_buffer is not self.__undef__ and (not (dirty and not self._send_socket_buffer[1]) or self.is_dirty_list(self.send_socket_buffer, self._send_socket_buffer) or belongs_to_parent)):
            dct["sendSocketBuffer"] = dictify(self.send_socket_buffer)
        elif belongs_to_parent and self.send_socket_buffer is self.__undef__:
            dct["sendSocketBuffer"] = 262144
        if "receive_socket_buffer" == "type" or (self.receive_socket_buffer is not self.__undef__ and (not (dirty and not self._receive_socket_buffer[1]) or self.is_dirty_list(self.receive_socket_buffer, self._receive_socket_buffer) or belongs_to_parent)):
            dct["receiveSocketBuffer"] = dictify(self.receive_socket_buffer)
        elif belongs_to_parent and self.receive_socket_buffer is self.__undef__:
            dct["receiveSocketBuffer"] = 262144
        if "xport_scheduler" == "type" or (self.xport_scheduler is not self.__undef__ and (not (dirty and not self._xport_scheduler[1]) or self.is_dirty_list(self.xport_scheduler, self._xport_scheduler) or belongs_to_parent)):
            dct["xportScheduler"] = dictify(self.xport_scheduler)
        elif belongs_to_parent and self.xport_scheduler is self.__undef__:
            dct["xportScheduler"] = "ROUND_ROBIN"
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._destination_type = (self._destination_type[0], True)
        self._remote_delphix_engine_info = (self._remote_delphix_engine_info[0], True)
        self._compression = (self._compression[0], True)
        self._encryption = (self._encryption[0], True)
        self._queue_depth = (self._queue_depth[0], True)
        self._block_size = (self._block_size[0], True)
        self._send_socket_buffer = (self._send_socket_buffer[0], True)
        self._receive_socket_buffer = (self._receive_socket_buffer[0], True)
        self._xport_scheduler = (self._xport_scheduler[0], True)

    def is_dirty(self):
        return any([self._destination_type[1], self._remote_delphix_engine_info[1], self._compression[1], self._encryption[1], self._queue_depth[1], self._block_size[1], self._send_socket_buffer[1], self._receive_socket_buffer[1], self._xport_scheduler[1]])

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
        if not isinstance(other, NetworkDSPTestParameters):
            return False
        return super().__eq__(other) and \
               self.destination_type == other.destination_type and \
               self.remote_delphix_engine_info == other.remote_delphix_engine_info and \
               self.compression == other.compression and \
               self.encryption == other.encryption and \
               self.queue_depth == other.queue_depth and \
               self.block_size == other.block_size and \
               self.send_socket_buffer == other.send_socket_buffer and \
               self.receive_socket_buffer == other.receive_socket_buffer and \
               self.xport_scheduler == other.xport_scheduler

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def destination_type(self):
        """
        *(default value: REMOTE_HOST)* Whether the test is testing connectivity
        to a Delphix Engine or remote host. *(permitted values: REMOTE_HOST,
        DELPHIX_ENGINE)*

        :rtype: ``str``
        """
        return self._destination_type[0]

    @destination_type.setter
    def destination_type(self, value):
        self._destination_type = (value, True)

    @property
    def remote_delphix_engine_info(self):
        """
        Address, username and password used when running a test to another
        Delphix Engine.

        :rtype: :py:class:`v1_11_11.web.vo.RemoteDelphixEngineInfo`
        """
        return self._remote_delphix_engine_info[0]

    @remote_delphix_engine_info.setter
    def remote_delphix_engine_info(self, value):
        self._remote_delphix_engine_info = (value, True)

    @property
    def compression(self):
        """
        Whether or not compression is used for the test.

        :rtype: ``bool``
        """
        return self._compression[0]

    @compression.setter
    def compression(self, value):
        self._compression = (value, True)

    @property
    def encryption(self):
        """
        Whether or not encryption is used for the test.

        :rtype: ``bool``
        """
        return self._encryption[0]

    @encryption.setter
    def encryption(self, value):
        self._encryption = (value, True)

    @property
    def queue_depth(self):
        """
        *(default value: 32)* The queue depth used for the DSP throughput test.

        :rtype: ``int``
        """
        return self._queue_depth[0]

    @queue_depth.setter
    def queue_depth(self, value):
        self._queue_depth = (value, True)

    @property
    def block_size(self):
        """
        *(default value: 65536)* The size of each transmit request in bytes.

        :rtype: ``int``
        """
        return self._block_size[0]

    @block_size.setter
    def block_size(self, value):
        self._block_size = (value, True)

    @property
    def send_socket_buffer(self):
        """
        *(default value: 262144)* The size of the send socket buffer in bytes.

        :rtype: ``int``
        """
        return self._send_socket_buffer[0]

    @send_socket_buffer.setter
    def send_socket_buffer(self, value):
        self._send_socket_buffer = (value, True)

    @property
    def receive_socket_buffer(self):
        """
        *(default value: 262144)* The size of the receive socket buffer in
        bytes.

        :rtype: ``int``
        """
        return self._receive_socket_buffer[0]

    @receive_socket_buffer.setter
    def receive_socket_buffer(self, value):
        self._receive_socket_buffer = (value, True)

    @property
    def xport_scheduler(self):
        """
        *(default value: ROUND_ROBIN)* The transport scheduler to use.
        *(permitted values: ROUND_ROBIN, LEAST_QUEUE)*

        :rtype: ``str``
        """
        return self._xport_scheduler[0]

    @xport_scheduler.setter
    def xport_scheduler(self, value):
        self._xport_scheduler = (value, True)

