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
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.DatabaseTemplate import DatabaseTemplate
from delphixpy.v1_11_18 import factory
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PgSQLDatabaseTemplate(DatabaseTemplate):
    """
    *(extends* :py:class:`v1_11_18.web.vo.DatabaseTemplate` *)* Configuration
    for PostgreSQL virtual databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PgSQLDatabaseTemplate", True)
        self._hba_entries = (self.__undef__, True)
        self._ident_entries = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._hba_entries = []
        for item in data.get("hbaEntries") or []:
            obj._hba_entries.append(factory.create_object(item))
            factory.validate_type(obj._hba_entries[-1], "PgSQLHBAEntry")
        obj._hba_entries = (obj._hba_entries, dirty)
        obj._ident_entries = []
        for item in data.get("identEntries") or []:
            obj._ident_entries.append(factory.create_object(item))
            factory.validate_type(obj._ident_entries[-1], "PgSQLIdentEntry")
        obj._ident_entries = (obj._ident_entries, dirty)
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
        if "hba_entries" == "type" or (self.hba_entries is not self.__undef__ and (not (dirty and not self._hba_entries[1]) or self.is_dirty_list(self.hba_entries, self._hba_entries) or belongs_to_parent)):
            dct["hbaEntries"] = dictify(self.hba_entries, prop_is_list_or_vo=True)
        if "ident_entries" == "type" or (self.ident_entries is not self.__undef__ and (not (dirty and not self._ident_entries[1]) or self.is_dirty_list(self.ident_entries, self._ident_entries) or belongs_to_parent)):
            dct["identEntries"] = dictify(self.ident_entries, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._hba_entries = (self._hba_entries[0], True)
        self._ident_entries = (self._ident_entries[0], True)

    def is_dirty(self):
        return any([self._hba_entries[1], self._ident_entries[1]])

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
        if not isinstance(other, PgSQLDatabaseTemplate):
            return False
        return super().__eq__(other) and \
               self.hba_entries == other.hba_entries and \
               self.ident_entries == other.ident_entries

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def hba_entries(self):
        """
        Entries in the PostgreSQL host-based authentication file (pg_hba.conf).

        :rtype: ``list`` of :py:class:`v1_11_18.web.vo.PgSQLHBAEntry`
        """
        return self._hba_entries[0]

    @hba_entries.setter
    def hba_entries(self, value):
        self._hba_entries = (value, True)

    @property
    def ident_entries(self):
        """
        Entries in the PostgreSQL username map file (pg_ident.conf).

        :rtype: ``list`` of :py:class:`v1_11_18.web.vo.PgSQLIdentEntry`
        """
        return self._ident_entries[0]

    @ident_entries.setter
    def ident_entries(self, value):
        self._ident_entries = (value, True)

