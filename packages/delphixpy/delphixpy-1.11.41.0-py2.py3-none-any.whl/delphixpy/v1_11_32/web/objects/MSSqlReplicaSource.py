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
#     /delphix-mssql-replica-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.MSSqlSource import MSSqlSource
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlReplicaSource(MSSqlSource):
    """
    *(extends* :py:class:`v1_11_32.web.vo.MSSqlSource` *)* A replica MSSQL
    source that constitutes an AG virtual source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlReplicaSource", True)
        self._mount_base = (self.__undef__, True)
        self._config = (self.__undef__, True)
        self._ag_source_reference = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._mount_base = (data.get("mountBase", obj.__undef__), dirty)
        if obj._mount_base[0] is not None and obj._mount_base[0] is not obj.__undef__:
            assert isinstance(obj._mount_base[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_base[0], type(obj._mount_base[0])))
            common.validate_format(obj._mount_base[0], "None", None, 256)
        obj._config = (data.get("config", obj.__undef__), dirty)
        if obj._config[0] is not None and obj._config[0] is not obj.__undef__:
            assert isinstance(obj._config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config[0], type(obj._config[0])))
            common.validate_format(obj._config[0], "objectReference", None, None)
        obj._ag_source_reference = (data.get("agSourceReference", obj.__undef__), dirty)
        if obj._ag_source_reference[0] is not None and obj._ag_source_reference[0] is not obj.__undef__:
            assert isinstance(obj._ag_source_reference[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ag_source_reference[0], type(obj._ag_source_reference[0])))
            common.validate_format(obj._ag_source_reference[0], "objectReference", None, None)
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
        if "mount_base" == "type" or (self.mount_base is not self.__undef__ and (not (dirty and not self._mount_base[1]))):
            dct["mountBase"] = dictify(self.mount_base)
        if "config" == "type" or (self.config is not self.__undef__ and (not (dirty and not self._config[1]))):
            dct["config"] = dictify(self.config)
        if "ag_source_reference" == "type" or (self.ag_source_reference is not self.__undef__ and (not (dirty and not self._ag_source_reference[1]))):
            dct["agSourceReference"] = dictify(self.ag_source_reference)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._mount_base = (self._mount_base[0], True)
        self._config = (self._config[0], True)
        self._ag_source_reference = (self._ag_source_reference[0], True)

    def is_dirty(self):
        return any([self._mount_base[1], self._config[1], self._ag_source_reference[1]])

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
        if not isinstance(other, MSSqlReplicaSource):
            return False
        return super().__eq__(other) and \
               self.mount_base == other.mount_base and \
               self.config == other.config and \
               self.ag_source_reference == other.ag_source_reference

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def mount_base(self):
        """
        The base mount point for the iSCSI LUN mounts.

        :rtype: ``str``
        """
        return self._mount_base[0]

    @mount_base.setter
    def mount_base(self, value):
        self._mount_base = (value, True)

    @property
    def config(self):
        """
        Reference to the configuration for the source.

        :rtype: ``str``
        """
        return self._config[0]

    @config.setter
    def config(self, value):
        self._config = (value, True)

    @property
    def ag_source_reference(self):
        """
        Reference to the AG virtual source.

        :rtype: ``str``
        """
        return self._ag_source_reference[0]

    @ag_source_reference.setter
    def ag_source_reference(self, value):
        self._ag_source_reference = (value, True)

