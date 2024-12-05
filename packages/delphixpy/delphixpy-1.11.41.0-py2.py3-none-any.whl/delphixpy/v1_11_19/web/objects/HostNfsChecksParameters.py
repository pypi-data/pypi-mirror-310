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
#     /delphix-host-nfs-checks-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_19.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_19 import factory
from delphixpy.v1_11_19 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class HostNfsChecksParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_19.web.vo.TypedObject` *)* Mechanism to verify
    user can mount/unmount on a remote host.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("HostNfsChecksParameters", True)
        self._connectivity_parameters = (self.__undef__, True)
        self._mount_path = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "connectivityParameters" in data and data["connectivityParameters"] is not None:
            obj._connectivity_parameters = (factory.create_object(data["connectivityParameters"], "UnixConnectivityParameters"), dirty)
            factory.validate_type(obj._connectivity_parameters[0], "UnixConnectivityParameters")
        else:
            obj._connectivity_parameters = (obj.__undef__, dirty)
        obj._mount_path = (data.get("mountPath", obj.__undef__), dirty)
        if obj._mount_path[0] is not None and obj._mount_path[0] is not obj.__undef__:
            assert isinstance(obj._mount_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_path[0], type(obj._mount_path[0])))
            common.validate_format(obj._mount_path[0], "unixpath", None, None)
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
        if "connectivity_parameters" == "type" or (self.connectivity_parameters is not self.__undef__ and (not (dirty and not self._connectivity_parameters[1]) or self.is_dirty_list(self.connectivity_parameters, self._connectivity_parameters) or belongs_to_parent)):
            dct["connectivityParameters"] = dictify(self.connectivity_parameters, prop_is_list_or_vo=True)
        if "mount_path" == "type" or (self.mount_path is not self.__undef__ and (not (dirty and not self._mount_path[1]) or self.is_dirty_list(self.mount_path, self._mount_path) or belongs_to_parent)):
            dct["mountPath"] = dictify(self.mount_path)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._connectivity_parameters = (self._connectivity_parameters[0], True)
        self._mount_path = (self._mount_path[0], True)

    def is_dirty(self):
        return any([self._connectivity_parameters[1], self._mount_path[1]])

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
        if not isinstance(other, HostNfsChecksParameters):
            return False
        return super().__eq__(other) and \
               self.connectivity_parameters == other.connectivity_parameters and \
               self.mount_path == other.mount_path

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def connectivity_parameters(self):
        """
        Parameters required to connect to the host.

        :rtype: :py:class:`v1_11_19.web.vo.UnixConnectivityParameters`
        """
        return self._connectivity_parameters[0]

    @connectivity_parameters.setter
    def connectivity_parameters(self, value):
        self._connectivity_parameters = (value, True)

    @property
    def mount_path(self):
        """
        Absolute path on the target environment where the filesystem should be
        mounted.

        :rtype: ``str``
        """
        return self._mount_path[0]

    @mount_path.setter
    def mount_path(self, value):
        self._mount_path = (value, True)

