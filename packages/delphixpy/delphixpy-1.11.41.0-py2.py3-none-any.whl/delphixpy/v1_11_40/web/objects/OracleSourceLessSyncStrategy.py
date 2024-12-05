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
#     /delphix-oracle-source-less-sync-strategy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.OracleSyncStrategy import OracleSyncStrategy
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleSourceLessSyncStrategy(OracleSyncStrategy):
    """
    *(extends* :py:class:`v1_11_40.web.vo.OracleSyncStrategy` *)* Base type for
    Oracle source less sync strategy and associated parameters.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleSourceLessSyncStrategy", True)
        self._staging_source = (self.__undef__, True)
        self._validate_by_opening_db_in_read_only_mode = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._staging_source = (data.get("stagingSource", obj.__undef__), dirty)
        if obj._staging_source[0] is not None and obj._staging_source[0] is not obj.__undef__:
            assert isinstance(obj._staging_source[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_source[0], type(obj._staging_source[0])))
            common.validate_format(obj._staging_source[0], "objectReference", None, None)
        obj._validate_by_opening_db_in_read_only_mode = (data.get("validateByOpeningDbInReadOnlyMode", obj.__undef__), dirty)
        if obj._validate_by_opening_db_in_read_only_mode[0] is not None and obj._validate_by_opening_db_in_read_only_mode[0] is not obj.__undef__:
            assert isinstance(obj._validate_by_opening_db_in_read_only_mode[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._validate_by_opening_db_in_read_only_mode[0], type(obj._validate_by_opening_db_in_read_only_mode[0])))
            common.validate_format(obj._validate_by_opening_db_in_read_only_mode[0], "None", None, None)
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
        if "staging_source" == "type" or (self.staging_source is not self.__undef__ and (not (dirty and not self._staging_source[1]))):
            dct["stagingSource"] = dictify(self.staging_source)
        if "validate_by_opening_db_in_read_only_mode" == "type" or (self.validate_by_opening_db_in_read_only_mode is not self.__undef__ and (not (dirty and not self._validate_by_opening_db_in_read_only_mode[1]) or self.is_dirty_list(self.validate_by_opening_db_in_read_only_mode, self._validate_by_opening_db_in_read_only_mode) or belongs_to_parent)):
            dct["validateByOpeningDbInReadOnlyMode"] = dictify(self.validate_by_opening_db_in_read_only_mode)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._staging_source = (self._staging_source[0], True)
        self._validate_by_opening_db_in_read_only_mode = (self._validate_by_opening_db_in_read_only_mode[0], True)

    def is_dirty(self):
        return any([self._staging_source[1], self._validate_by_opening_db_in_read_only_mode[1]])

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
        if not isinstance(other, OracleSourceLessSyncStrategy):
            return False
        return super().__eq__(other) and \
               self.staging_source == other.staging_source and \
               self.validate_by_opening_db_in_read_only_mode == other.validate_by_opening_db_in_read_only_mode

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def staging_source(self):
        """
        Reference to the staging source.

        :rtype: ``str``
        """
        return self._staging_source[0]

    @staging_source.setter
    def staging_source(self, value):
        self._staging_source = (value, True)

    @property
    def validate_by_opening_db_in_read_only_mode(self):
        """
        Whether this staging database snapshot will be validated by opening it
        in read-only mode.

        :rtype: ``bool``
        """
        return self._validate_by_opening_db_in_read_only_mode[0]

    @validate_by_opening_db_in_read_only_mode.setter
    def validate_by_opening_db_in_read_only_mode(self, value):
        self._validate_by_opening_db_in_read_only_mode = (value, True)

