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
#     /delphix-pgsql-install.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_17.web.objects.SourceRepository import SourceRepository
from delphixpy.v1_11_17 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PgSQLInstall(SourceRepository):
    """
    *(extends* :py:class:`v1_11_17.web.vo.SourceRepository` *)* A PostgreSQL
    installation.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PgSQLInstall", True)
        self._version = (self.__undef__, True)
        self._variant = (self.__undef__, True)
        self._installation_path = (self.__undef__, True)
        self._bits = (self.__undef__, True)
        self._segment_size = (self.__undef__, True)
        self._discovered = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._version = (data.get("version", obj.__undef__), dirty)
        if obj._version[0] is not None and obj._version[0] is not obj.__undef__:
            assert isinstance(obj._version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._version[0], type(obj._version[0])))
            common.validate_format(obj._version[0], "pgsqlVersion", None, None)
        obj._variant = (data.get("variant", obj.__undef__), dirty)
        if obj._variant[0] is not None and obj._variant[0] is not obj.__undef__:
            assert isinstance(obj._variant[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._variant[0], type(obj._variant[0])))
            assert obj._variant[0] in ['PostgreSQL', 'EnterpriseDB'], "Expected enum ['PostgreSQL', 'EnterpriseDB'] but got %s" % obj._variant[0]
            common.validate_format(obj._variant[0], "None", None, None)
        obj._installation_path = (data.get("installationPath", obj.__undef__), dirty)
        if obj._installation_path[0] is not None and obj._installation_path[0] is not obj.__undef__:
            assert isinstance(obj._installation_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._installation_path[0], type(obj._installation_path[0])))
            common.validate_format(obj._installation_path[0], "None", None, 1024)
        obj._bits = (data.get("bits", obj.__undef__), dirty)
        if obj._bits[0] is not None and obj._bits[0] is not obj.__undef__:
            assert isinstance(obj._bits[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._bits[0], type(obj._bits[0])))
            assert obj._bits[0] in [32, 64], "Expected enum [32, 64] but got %s" % obj._bits[0]
            common.validate_format(obj._bits[0], "None", None, None)
        obj._segment_size = (data.get("segmentSize", obj.__undef__), dirty)
        if obj._segment_size[0] is not None and obj._segment_size[0] is not obj.__undef__:
            assert isinstance(obj._segment_size[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._segment_size[0], type(obj._segment_size[0])))
            assert obj._segment_size[0] in [1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864], "Expected enum [1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864] but got %s" % obj._segment_size[0]
            common.validate_format(obj._segment_size[0], "None", None, None)
        obj._discovered = (data.get("discovered", obj.__undef__), dirty)
        if obj._discovered[0] is not None and obj._discovered[0] is not obj.__undef__:
            assert isinstance(obj._discovered[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._discovered[0], type(obj._discovered[0])))
            common.validate_format(obj._discovered[0], "None", None, None)
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
        if "version" == "type" or (self.version is not self.__undef__ and (not (dirty and not self._version[1]))):
            dct["version"] = dictify(self.version)
        if "variant" == "type" or (self.variant is not self.__undef__ and (not (dirty and not self._variant[1]))):
            dct["variant"] = dictify(self.variant)
        if "installation_path" == "type" or (self.installation_path is not self.__undef__ and (not (dirty and not self._installation_path[1]) or self.is_dirty_list(self.installation_path, self._installation_path) or belongs_to_parent)):
            dct["installationPath"] = dictify(self.installation_path)
        if "bits" == "type" or (self.bits is not self.__undef__ and (not (dirty and not self._bits[1]))):
            dct["bits"] = dictify(self.bits)
        if "segment_size" == "type" or (self.segment_size is not self.__undef__ and (not (dirty and not self._segment_size[1]))):
            dct["segmentSize"] = dictify(self.segment_size)
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._version = (self._version[0], True)
        self._variant = (self._variant[0], True)
        self._installation_path = (self._installation_path[0], True)
        self._bits = (self._bits[0], True)
        self._segment_size = (self._segment_size[0], True)
        self._discovered = (self._discovered[0], True)

    def is_dirty(self):
        return any([self._version[1], self._variant[1], self._installation_path[1], self._bits[1], self._segment_size[1], self._discovered[1]])

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
        if not isinstance(other, PgSQLInstall):
            return False
        return super().__eq__(other) and \
               self.version == other.version and \
               self.variant == other.variant and \
               self.installation_path == other.installation_path and \
               self.bits == other.bits and \
               self.segment_size == other.segment_size and \
               self.discovered == other.discovered

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def version(self):
        """
        Version of the repository.

        :rtype: ``str``
        """
        return self._version[0]

    @version.setter
    def version(self, value):
        self._version = (value, True)

    @property
    def variant(self):
        """
        Variant of the repository. *(permitted values: PostgreSQL,
        EnterpriseDB)*

        :rtype: ``str``
        """
        return self._variant[0]

    @variant.setter
    def variant(self, value):
        self._variant = (value, True)

    @property
    def installation_path(self):
        """
        Directory path where the installation is located.

        :rtype: ``str``
        """
        return self._installation_path[0]

    @installation_path.setter
    def installation_path(self, value):
        self._installation_path = (value, True)

    @property
    def bits(self):
        """
        32 or 64 bit installation. *(permitted values: 32, 64)*

        :rtype: ``int``
        """
        return self._bits[0]

    @bits.setter
    def bits(self, value):
        self._bits = (value, True)

    @property
    def segment_size(self):
        """
        Size of the WAL segments (in bytes) generated by PostgreSQL binaries.
        *(permitted values: 1048576, 2097152, 4194304, 8388608, 16777216,
        33554432, 67108864)*

        :rtype: ``int``
        """
        return self._segment_size[0]

    @segment_size.setter
    def segment_size(self, value):
        self._segment_size = (value, True)

    @property
    def discovered(self):
        """
        Flag indicating whether the installation was discovered or manually
        entered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

