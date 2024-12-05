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
#     /delphix-dsp-autotuner-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_38 import factory
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class DSPAutotunerParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_38.web.vo.TypedObject` *)* Network information
    required by the DSP autotuner.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("DSPAutotunerParameters", True)
        self._destination_type = (self.__undef__, True)
        self._direction = (self.__undef__, True)
        self._remote_host = (self.__undef__, True)
        self._remote_delphix_engine_info = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._destination_type = (data.get("destinationType", obj.__undef__), dirty)
        if obj._destination_type[0] is not None and obj._destination_type[0] is not obj.__undef__:
            assert isinstance(obj._destination_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._destination_type[0], type(obj._destination_type[0])))
            assert obj._destination_type[0] in ['REMOTE_HOST', 'DELPHIX_ENGINE'], "Expected enum ['REMOTE_HOST', 'DELPHIX_ENGINE'] but got %s" % obj._destination_type[0]
            common.validate_format(obj._destination_type[0], "None", None, None)
        obj._direction = (data.get("direction", obj.__undef__), dirty)
        if obj._direction[0] is not None and obj._direction[0] is not obj.__undef__:
            assert isinstance(obj._direction[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._direction[0], type(obj._direction[0])))
            assert obj._direction[0] in ['TRANSMIT', 'RECEIVE'], "Expected enum ['TRANSMIT', 'RECEIVE'] but got %s" % obj._direction[0]
            common.validate_format(obj._direction[0], "None", None, None)
        obj._remote_host = (data.get("remoteHost", obj.__undef__), dirty)
        if obj._remote_host[0] is not None and obj._remote_host[0] is not obj.__undef__:
            assert isinstance(obj._remote_host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._remote_host[0], type(obj._remote_host[0])))
            common.validate_format(obj._remote_host[0], "objectReference", None, None)
        if "remoteDelphixEngineInfo" in data and data["remoteDelphixEngineInfo"] is not None:
            obj._remote_delphix_engine_info = (factory.create_object(data["remoteDelphixEngineInfo"], "RemoteDelphixEngineInfo"), dirty)
            factory.validate_type(obj._remote_delphix_engine_info[0], "RemoteDelphixEngineInfo")
        else:
            obj._remote_delphix_engine_info = (obj.__undef__, dirty)
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
        if "direction" == "type" or (self.direction is not self.__undef__ and (not (dirty and not self._direction[1]) or self.is_dirty_list(self.direction, self._direction) or belongs_to_parent)):
            dct["direction"] = dictify(self.direction)
        elif belongs_to_parent and self.direction is self.__undef__:
            dct["direction"] = "TRANSMIT"
        if "remote_host" == "type" or (self.remote_host is not self.__undef__ and (not (dirty and not self._remote_host[1]) or self.is_dirty_list(self.remote_host, self._remote_host) or belongs_to_parent)):
            dct["remoteHost"] = dictify(self.remote_host)
        if "remote_delphix_engine_info" == "type" or (self.remote_delphix_engine_info is not self.__undef__ and (not (dirty and not self._remote_delphix_engine_info[1]) or self.is_dirty_list(self.remote_delphix_engine_info, self._remote_delphix_engine_info) or belongs_to_parent)):
            dct["remoteDelphixEngineInfo"] = dictify(self.remote_delphix_engine_info, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._destination_type = (self._destination_type[0], True)
        self._direction = (self._direction[0], True)
        self._remote_host = (self._remote_host[0], True)
        self._remote_delphix_engine_info = (self._remote_delphix_engine_info[0], True)

    def is_dirty(self):
        return any([self._destination_type[1], self._direction[1], self._remote_host[1], self._remote_delphix_engine_info[1]])

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
        if not isinstance(other, DSPAutotunerParameters):
            return False
        return super().__eq__(other) and \
               self.destination_type == other.destination_type and \
               self.direction == other.direction and \
               self.remote_host == other.remote_host and \
               self.remote_delphix_engine_info == other.remote_delphix_engine_info

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def destination_type(self):
        """
        Whether the test is testing connectivity to a Delphix Engine or a
        remote host. *(permitted values: REMOTE_HOST, DELPHIX_ENGINE)*

        :rtype: ``str``
        """
        return self._destination_type[0]

    @destination_type.setter
    def destination_type(self, value):
        self._destination_type = (value, True)

    @property
    def direction(self):
        """
        *(default value: TRANSMIT)* Whether the test is a transmit or receive
        test. *(permitted values: TRANSMIT, RECEIVE)*

        :rtype: ``str``
        """
        return self._direction[0]

    @direction.setter
    def direction(self, value):
        self._direction = (value, True)

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
    def remote_delphix_engine_info(self):
        """
        Address, username and password used when running a test to another
        Delphix Engine.

        :rtype: :py:class:`v1_11_38.web.vo.RemoteDelphixEngineInfo`
        """
        return self._remote_delphix_engine_info[0]

    @remote_delphix_engine_info.setter
    def remote_delphix_engine_info(self, value):
        self._remote_delphix_engine_info = (value, True)

