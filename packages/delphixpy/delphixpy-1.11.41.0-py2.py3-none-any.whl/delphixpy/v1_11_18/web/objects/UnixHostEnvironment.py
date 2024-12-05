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
#     /delphix-unix-host-environment.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.HostEnvironment import HostEnvironment
from delphixpy.v1_11_18 import factory
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UnixHostEnvironment(HostEnvironment):
    """
    *(extends* :py:class:`v1_11_18.web.vo.HostEnvironment` *)* The
    representation of a unix host environment object.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UnixHostEnvironment", True)
        self._ase_host_environment_parameters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "aseHostEnvironmentParameters" in data and data["aseHostEnvironmentParameters"] is not None:
            obj._ase_host_environment_parameters = (factory.create_object(data["aseHostEnvironmentParameters"], "ASEHostEnvironmentParameters"), dirty)
            factory.validate_type(obj._ase_host_environment_parameters[0], "ASEHostEnvironmentParameters")
        else:
            obj._ase_host_environment_parameters = (obj.__undef__, dirty)
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
        if "ase_host_environment_parameters" == "type" or (self.ase_host_environment_parameters is not self.__undef__ and (not (dirty and not self._ase_host_environment_parameters[1]) or self.is_dirty_list(self.ase_host_environment_parameters, self._ase_host_environment_parameters) or belongs_to_parent)):
            dct["aseHostEnvironmentParameters"] = dictify(self.ase_host_environment_parameters, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._ase_host_environment_parameters = (self._ase_host_environment_parameters[0], True)

    def is_dirty(self):
        return any([self._ase_host_environment_parameters[1]])

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
        if not isinstance(other, UnixHostEnvironment):
            return False
        return super().__eq__(other) and \
               self.ase_host_environment_parameters == other.ase_host_environment_parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def ase_host_environment_parameters(self):
        """
        Parameters for an environment with SAP ASE instances.

        :rtype: :py:class:`v1_11_18.web.vo.ASEHostEnvironmentParameters`
        """
        return self._ase_host_environment_parameters[0]

    @ase_host_environment_parameters.setter
    def ase_host_environment_parameters(self, value):
        self._ase_host_environment_parameters = (value, True)

