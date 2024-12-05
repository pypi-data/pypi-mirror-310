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
#     /delphix-host-configuration.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_34 import factory
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HostConfiguration(TypedObject):
    """
    *(extends* :py:class:`v1_11_34.web.vo.TypedObject` *)* The representation
    of the host configuration properties.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HostConfiguration", True)
        self._last_updated = (self.__undef__, True)
        self._discovered = (self.__undef__, True)
        self._last_refreshed = (self.__undef__, True)
        self._operating_system = (self.__undef__, True)
        self._machine = (self.__undef__, True)
        self._power_shell_version = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._last_updated = (data.get("lastUpdated", obj.__undef__), dirty)
        if obj._last_updated[0] is not None and obj._last_updated[0] is not obj.__undef__:
            assert isinstance(obj._last_updated[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_updated[0], type(obj._last_updated[0])))
            common.validate_format(obj._last_updated[0], "None", None, None)
        obj._discovered = (data.get("discovered", obj.__undef__), dirty)
        if obj._discovered[0] is not None and obj._discovered[0] is not obj.__undef__:
            assert isinstance(obj._discovered[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._discovered[0], type(obj._discovered[0])))
            common.validate_format(obj._discovered[0], "None", None, None)
        obj._last_refreshed = (data.get("lastRefreshed", obj.__undef__), dirty)
        if obj._last_refreshed[0] is not None and obj._last_refreshed[0] is not obj.__undef__:
            assert isinstance(obj._last_refreshed[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_refreshed[0], type(obj._last_refreshed[0])))
            common.validate_format(obj._last_refreshed[0], "None", None, None)
        if "operatingSystem" in data and data["operatingSystem"] is not None:
            obj._operating_system = (factory.create_object(data["operatingSystem"], "HostOS"), dirty)
            factory.validate_type(obj._operating_system[0], "HostOS")
        else:
            obj._operating_system = (obj.__undef__, dirty)
        if "machine" in data and data["machine"] is not None:
            obj._machine = (factory.create_object(data["machine"], "HostMachine"), dirty)
            factory.validate_type(obj._machine[0], "HostMachine")
        else:
            obj._machine = (obj.__undef__, dirty)
        obj._power_shell_version = (data.get("powerShellVersion", obj.__undef__), dirty)
        if obj._power_shell_version[0] is not None and obj._power_shell_version[0] is not obj.__undef__:
            assert isinstance(obj._power_shell_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._power_shell_version[0], type(obj._power_shell_version[0])))
            common.validate_format(obj._power_shell_version[0], "None", None, None)
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
        if "last_updated" == "type" or (self.last_updated is not self.__undef__ and (not (dirty and not self._last_updated[1]))):
            dct["lastUpdated"] = dictify(self.last_updated)
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        if "last_refreshed" == "type" or (self.last_refreshed is not self.__undef__ and (not (dirty and not self._last_refreshed[1]))):
            dct["lastRefreshed"] = dictify(self.last_refreshed)
        if "operating_system" == "type" or (self.operating_system is not self.__undef__ and (not (dirty and not self._operating_system[1]))):
            dct["operatingSystem"] = dictify(self.operating_system)
        if "machine" == "type" or (self.machine is not self.__undef__ and (not (dirty and not self._machine[1]))):
            dct["machine"] = dictify(self.machine)
        if "power_shell_version" == "type" or (self.power_shell_version is not self.__undef__ and (not (dirty and not self._power_shell_version[1]))):
            dct["powerShellVersion"] = dictify(self.power_shell_version)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._last_updated = (self._last_updated[0], True)
        self._discovered = (self._discovered[0], True)
        self._last_refreshed = (self._last_refreshed[0], True)
        self._operating_system = (self._operating_system[0], True)
        self._machine = (self._machine[0], True)
        self._power_shell_version = (self._power_shell_version[0], True)

    def is_dirty(self):
        return any([self._last_updated[1], self._discovered[1], self._last_refreshed[1], self._operating_system[1], self._machine[1], self._power_shell_version[1]])

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
        if not isinstance(other, HostConfiguration):
            return False
        return super().__eq__(other) and \
               self.last_updated == other.last_updated and \
               self.discovered == other.discovered and \
               self.last_refreshed == other.last_refreshed and \
               self.operating_system == other.operating_system and \
               self.machine == other.machine and \
               self.power_shell_version == other.power_shell_version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def last_updated(self):
        """
        The timestamp when the host was last updated.

        :rtype: ``str``
        """
        return self._last_updated[0]

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated = (value, True)

    @property
    def discovered(self):
        """
        Indicates whether the host configuration properties were discovered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

    @property
    def last_refreshed(self):
        """
        The timestamp when the host was last refreshed.

        :rtype: ``str``
        """
        return self._last_refreshed[0]

    @last_refreshed.setter
    def last_refreshed(self, value):
        self._last_refreshed = (value, True)

    @property
    def operating_system(self):
        """
        The host operating system information.

        :rtype: :py:class:`v1_11_34.web.vo.HostOS`
        """
        return self._operating_system[0]

    @operating_system.setter
    def operating_system(self, value):
        self._operating_system = (value, True)

    @property
    def machine(self):
        """
        The host machine information.

        :rtype: :py:class:`v1_11_34.web.vo.HostMachine`
        """
        return self._machine[0]

    @machine.setter
    def machine(self, value):
        self._machine = (value, True)

    @property
    def power_shell_version(self):
        """
        The PowerShell version installed on the windows target host.

        :rtype: ``str``
        """
        return self._power_shell_version[0]

    @power_shell_version.setter
    def power_shell_version(self, value):
        self._power_shell_version = (value, True)

