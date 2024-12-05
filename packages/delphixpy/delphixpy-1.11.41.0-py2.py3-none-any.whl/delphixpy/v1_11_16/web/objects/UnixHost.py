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
#     /delphix-unix-host.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.Host import Host
from delphixpy.v1_11_16 import factory
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UnixHost(Host):
    """
    *(extends* :py:class:`v1_11_16.web.vo.Host` *)* The representation of a
    Unix host object.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UnixHost", True)
        self._toolkit_path = (self.__undef__, True)
        self._oracle_host_parameters = (self.__undef__, True)
        self._ssh_verification_strategy = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._toolkit_path = (data.get("toolkitPath", obj.__undef__), dirty)
        if obj._toolkit_path[0] is not None and obj._toolkit_path[0] is not obj.__undef__:
            assert isinstance(obj._toolkit_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._toolkit_path[0], type(obj._toolkit_path[0])))
            common.validate_format(obj._toolkit_path[0], "None", None, None)
        if "oracleHostParameters" in data and data["oracleHostParameters"] is not None:
            obj._oracle_host_parameters = (factory.create_object(data["oracleHostParameters"], "OracleHostParameters"), dirty)
            factory.validate_type(obj._oracle_host_parameters[0], "OracleHostParameters")
        else:
            obj._oracle_host_parameters = (obj.__undef__, dirty)
        if "sshVerificationStrategy" in data and data["sshVerificationStrategy"] is not None:
            obj._ssh_verification_strategy = (factory.create_object(data["sshVerificationStrategy"], "SshVerificationStrategy"), dirty)
            factory.validate_type(obj._ssh_verification_strategy[0], "SshVerificationStrategy")
        else:
            obj._ssh_verification_strategy = (obj.__undef__, dirty)
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
        if "toolkit_path" == "type" or (self.toolkit_path is not self.__undef__ and (not (dirty and not self._toolkit_path[1]) or self.is_dirty_list(self.toolkit_path, self._toolkit_path) or belongs_to_parent)):
            dct["toolkitPath"] = dictify(self.toolkit_path)
        if "oracle_host_parameters" == "type" or (self.oracle_host_parameters is not self.__undef__ and (not (dirty and not self._oracle_host_parameters[1]) or self.is_dirty_list(self.oracle_host_parameters, self._oracle_host_parameters) or belongs_to_parent)):
            dct["oracleHostParameters"] = dictify(self.oracle_host_parameters, prop_is_list_or_vo=True)
        if "ssh_verification_strategy" == "type" or (self.ssh_verification_strategy is not self.__undef__ and (not (dirty and not self._ssh_verification_strategy[1]) or self.is_dirty_list(self.ssh_verification_strategy, self._ssh_verification_strategy) or belongs_to_parent)):
            dct["sshVerificationStrategy"] = dictify(self.ssh_verification_strategy, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._toolkit_path = (self._toolkit_path[0], True)
        self._oracle_host_parameters = (self._oracle_host_parameters[0], True)
        self._ssh_verification_strategy = (self._ssh_verification_strategy[0], True)

    def is_dirty(self):
        return any([self._toolkit_path[1], self._oracle_host_parameters[1], self._ssh_verification_strategy[1]])

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
        if not isinstance(other, UnixHost):
            return False
        return super().__eq__(other) and \
               self.toolkit_path == other.toolkit_path and \
               self.oracle_host_parameters == other.oracle_host_parameters and \
               self.ssh_verification_strategy == other.ssh_verification_strategy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def toolkit_path(self):
        """
        The path for the toolkit that resides on the host.

        :rtype: ``str``
        """
        return self._toolkit_path[0]

    @toolkit_path.setter
    def toolkit_path(self, value):
        self._toolkit_path = (value, True)

    @property
    def oracle_host_parameters(self):
        """
        The Oracle specific parameters associated with the host.

        :rtype: :py:class:`v1_11_16.web.vo.OracleHostParameters`
        """
        return self._oracle_host_parameters[0]

    @oracle_host_parameters.setter
    def oracle_host_parameters(self, value):
        self._oracle_host_parameters = (value, True)

    @property
    def ssh_verification_strategy(self):
        """
        Mechanism to use for ssh host verification.

        :rtype: :py:class:`v1_11_16.web.vo.SshVerificationStrategy`
        """
        return self._ssh_verification_strategy[0]

    @ssh_verification_strategy.setter
    def ssh_verification_strategy(self, value):
        self._ssh_verification_strategy = (value, True)

