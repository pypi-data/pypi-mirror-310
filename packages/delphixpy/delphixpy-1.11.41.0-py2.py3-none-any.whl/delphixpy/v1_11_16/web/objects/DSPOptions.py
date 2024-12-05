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
#     /delphix-dsp-options.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class DSPOptions(TypedObject):
    """
    *(extends* :py:class:`v1_11_16.web.vo.TypedObject` *)* Options commonly
    used by apps that use DSP.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("DSPOptions", True)
        self._compression = (self.__undef__, True)
        self._encryption = (self.__undef__, True)
        self._bandwidth_limit = (self.__undef__, True)
        self._num_connections = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._compression = (data.get("compression", obj.__undef__), dirty)
        if obj._compression[0] is not None and obj._compression[0] is not obj.__undef__:
            assert isinstance(obj._compression[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._compression[0], type(obj._compression[0])))
            common.validate_format(obj._compression[0], "None", None, None)
        obj._encryption = (data.get("encryption", obj.__undef__), dirty)
        if obj._encryption[0] is not None and obj._encryption[0] is not obj.__undef__:
            assert isinstance(obj._encryption[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._encryption[0], type(obj._encryption[0])))
            common.validate_format(obj._encryption[0], "None", None, None)
        obj._bandwidth_limit = (data.get("bandwidthLimit", obj.__undef__), dirty)
        if obj._bandwidth_limit[0] is not None and obj._bandwidth_limit[0] is not obj.__undef__:
            assert isinstance(obj._bandwidth_limit[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._bandwidth_limit[0], type(obj._bandwidth_limit[0])))
            common.validate_format(obj._bandwidth_limit[0], "None", None, None)
        obj._num_connections = (data.get("numConnections", obj.__undef__), dirty)
        if obj._num_connections[0] is not None and obj._num_connections[0] is not obj.__undef__:
            assert isinstance(obj._num_connections[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_connections[0], type(obj._num_connections[0])))
            common.validate_format(obj._num_connections[0], "None", None, None)
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
        if "compression" == "type" or (self.compression is not self.__undef__ and (not (dirty and not self._compression[1]) or self.is_dirty_list(self.compression, self._compression) or belongs_to_parent)):
            dct["compression"] = dictify(self.compression)
        elif belongs_to_parent and self.compression is self.__undef__:
            dct["compression"] = False
        if "encryption" == "type" or (self.encryption is not self.__undef__ and (not (dirty and not self._encryption[1]) or self.is_dirty_list(self.encryption, self._encryption) or belongs_to_parent)):
            dct["encryption"] = dictify(self.encryption)
        elif belongs_to_parent and self.encryption is self.__undef__:
            dct["encryption"] = False
        if "bandwidth_limit" == "type" or (self.bandwidth_limit is not self.__undef__ and (not (dirty and not self._bandwidth_limit[1]) or self.is_dirty_list(self.bandwidth_limit, self._bandwidth_limit) or belongs_to_parent)):
            dct["bandwidthLimit"] = dictify(self.bandwidth_limit)
        elif belongs_to_parent and self.bandwidth_limit is self.__undef__:
            dct["bandwidthLimit"] = 0
        if "num_connections" == "type" or (self.num_connections is not self.__undef__ and (not (dirty and not self._num_connections[1]) or self.is_dirty_list(self.num_connections, self._num_connections) or belongs_to_parent)):
            dct["numConnections"] = dictify(self.num_connections)
        elif belongs_to_parent and self.num_connections is self.__undef__:
            dct["numConnections"] = 1
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._compression = (self._compression[0], True)
        self._encryption = (self._encryption[0], True)
        self._bandwidth_limit = (self._bandwidth_limit[0], True)
        self._num_connections = (self._num_connections[0], True)

    def is_dirty(self):
        return any([self._compression[1], self._encryption[1], self._bandwidth_limit[1], self._num_connections[1]])

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
        if not isinstance(other, DSPOptions):
            return False
        return super().__eq__(other) and \
               self.compression == other.compression and \
               self.encryption == other.encryption and \
               self.bandwidth_limit == other.bandwidth_limit and \
               self.num_connections == other.num_connections

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def compression(self):
        """
        Compress the data stream over the network.

        :rtype: ``bool``
        """
        return self._compression[0]

    @compression.setter
    def compression(self, value):
        self._compression = (value, True)

    @property
    def encryption(self):
        """
        Encrypt the data stream over the network.

        :rtype: ``bool``
        """
        return self._encryption[0]

    @encryption.setter
    def encryption(self, value):
        self._encryption = (value, True)

    @property
    def bandwidth_limit(self):
        """
        Bandwidth limit (MB/s) for network traffic. A value of 0 means no
        limit.

        :rtype: ``int``
        """
        return self._bandwidth_limit[0]

    @bandwidth_limit.setter
    def bandwidth_limit(self, value):
        self._bandwidth_limit = (value, True)

    @property
    def num_connections(self):
        """
        *(default value: 1)* Total number of transport connections to use.

        :rtype: ``int``
        """
        return self._num_connections[0]

    @num_connections.setter
    def num_connections(self, value):
        self._num_connections = (value, True)

