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
#     /delphix-dsp-best-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_41.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_41 import factory
from delphixpy.v1_11_41 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class DSPBestParameters(PersistentObject):
    """
    *(extends* :py:class:`v1_11_41.web.vo.PersistentObject` *)* DSP parameters,
    found by autotuner, that give the highest throughput for a certain target.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("DSPBestParameters", True)
        self._destination_type = (self.__undef__, True)
        self._remote_delphix_engine_info = (self.__undef__, True)
        self._remote_host = (self.__undef__, True)
        self._queue_depth = (self.__undef__, True)
        self._throughput = (self.__undef__, True)
        self._num_connections = (self.__undef__, True)
        self._buffer_size = (self.__undef__, True)


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
        obj._remote_host = (data.get("remoteHost", obj.__undef__), dirty)
        if obj._remote_host[0] is not None and obj._remote_host[0] is not obj.__undef__:
            assert isinstance(obj._remote_host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._remote_host[0], type(obj._remote_host[0])))
            common.validate_format(obj._remote_host[0], "objectReference", None, None)
        obj._queue_depth = (data.get("queueDepth", obj.__undef__), dirty)
        if obj._queue_depth[0] is not None and obj._queue_depth[0] is not obj.__undef__:
            assert isinstance(obj._queue_depth[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._queue_depth[0], type(obj._queue_depth[0])))
            common.validate_format(obj._queue_depth[0], "None", None, None)
        obj._throughput = (data.get("throughput", obj.__undef__), dirty)
        if obj._throughput[0] is not None and obj._throughput[0] is not obj.__undef__:
            assert isinstance(obj._throughput[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._throughput[0], type(obj._throughput[0])))
            common.validate_format(obj._throughput[0], "None", None, None)
        obj._num_connections = (data.get("numConnections", obj.__undef__), dirty)
        if obj._num_connections[0] is not None and obj._num_connections[0] is not obj.__undef__:
            assert isinstance(obj._num_connections[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_connections[0], type(obj._num_connections[0])))
            common.validate_format(obj._num_connections[0], "None", None, None)
        obj._buffer_size = (data.get("bufferSize", obj.__undef__), dirty)
        if obj._buffer_size[0] is not None and obj._buffer_size[0] is not obj.__undef__:
            assert isinstance(obj._buffer_size[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._buffer_size[0], type(obj._buffer_size[0])))
            common.validate_format(obj._buffer_size[0], "None", None, None)
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
        if "destination_type" == "type" or (self.destination_type is not self.__undef__ and (not (dirty and not self._destination_type[1]))):
            dct["destinationType"] = dictify(self.destination_type)
        if "remote_delphix_engine_info" == "type" or (self.remote_delphix_engine_info is not self.__undef__ and (not (dirty and not self._remote_delphix_engine_info[1]))):
            dct["remoteDelphixEngineInfo"] = dictify(self.remote_delphix_engine_info)
        if "remote_host" == "type" or (self.remote_host is not self.__undef__ and (not (dirty and not self._remote_host[1]))):
            dct["remoteHost"] = dictify(self.remote_host)
        if "queue_depth" == "type" or (self.queue_depth is not self.__undef__ and (not (dirty and not self._queue_depth[1]))):
            dct["queueDepth"] = dictify(self.queue_depth)
        if "throughput" == "type" or (self.throughput is not self.__undef__ and (not (dirty and not self._throughput[1]))):
            dct["throughput"] = dictify(self.throughput)
        if "num_connections" == "type" or (self.num_connections is not self.__undef__ and (not (dirty and not self._num_connections[1]))):
            dct["numConnections"] = dictify(self.num_connections)
        if "buffer_size" == "type" or (self.buffer_size is not self.__undef__ and (not (dirty and not self._buffer_size[1]))):
            dct["bufferSize"] = dictify(self.buffer_size)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._destination_type = (self._destination_type[0], True)
        self._remote_delphix_engine_info = (self._remote_delphix_engine_info[0], True)
        self._remote_host = (self._remote_host[0], True)
        self._queue_depth = (self._queue_depth[0], True)
        self._throughput = (self._throughput[0], True)
        self._num_connections = (self._num_connections[0], True)
        self._buffer_size = (self._buffer_size[0], True)

    def is_dirty(self):
        return any([self._destination_type[1], self._remote_delphix_engine_info[1], self._remote_host[1], self._queue_depth[1], self._throughput[1], self._num_connections[1], self._buffer_size[1]])

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
        if not isinstance(other, DSPBestParameters):
            return False
        return super().__eq__(other) and \
               self.destination_type == other.destination_type and \
               self.remote_delphix_engine_info == other.remote_delphix_engine_info and \
               self.remote_host == other.remote_host and \
               self.queue_depth == other.queue_depth and \
               self.throughput == other.throughput and \
               self.num_connections == other.num_connections and \
               self.buffer_size == other.buffer_size

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def destination_type(self):
        """
        Whether the test is testing connectivity to a Delphix Engine or remote
        host. *(permitted values: REMOTE_HOST, DELPHIX_ENGINE)*

        :rtype: ``str``
        """
        return self._destination_type[0]

    @destination_type.setter
    def destination_type(self, value):
        self._destination_type = (value, True)

    @property
    def remote_delphix_engine_info(self):
        """
        Information used when running a test to another Delphix Engine.

        :rtype: :py:class:`v1_11_41.web.vo.RemoteDelphixEngineInfo`
        """
        return self._remote_delphix_engine_info[0]

    @remote_delphix_engine_info.setter
    def remote_delphix_engine_info(self, value):
        self._remote_delphix_engine_info = (value, True)

    @property
    def remote_host(self):
        """
        The remote host for the test. The host must be part of an existing
        environment.

        :rtype: ``str``
        """
        return self._remote_host[0]

    @remote_host.setter
    def remote_host(self, value):
        self._remote_host = (value, True)

    @property
    def queue_depth(self):
        """
        The queue depth used to achieve maximum throughput.

        :rtype: ``int``
        """
        return self._queue_depth[0]

    @queue_depth.setter
    def queue_depth(self, value):
        self._queue_depth = (value, True)

    @property
    def throughput(self):
        """
        The average throughput measured.

        :rtype: ``float``
        """
        return self._throughput[0]

    @throughput.setter
    def throughput(self, value):
        self._throughput = (value, True)

    @property
    def num_connections(self):
        """
        The number of connections used to achieve maximum throughput.

        :rtype: ``int``
        """
        return self._num_connections[0]

    @num_connections.setter
    def num_connections(self, value):
        self._num_connections = (value, True)

    @property
    def buffer_size(self):
        """
        The size of the send and receive socket buffers in bytes used to
        achieve maximum throughput.

        :rtype: ``int``
        """
        return self._buffer_size[0]

    @buffer_size.setter
    def buffer_size(self, value):
        self._buffer_size = (value, True)

