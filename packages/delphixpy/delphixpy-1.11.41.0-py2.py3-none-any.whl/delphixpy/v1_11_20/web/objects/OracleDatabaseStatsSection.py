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
#     /delphix-oracle-database-stats-section.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_20 import factory
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleDatabaseStatsSection(TypedObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.TypedObject` *)* Oracle database
    performance statistics for a specific section.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleDatabaseStatsSection", True)
        self._section_name = (self.__undef__, True)
        self._column_headers = (self.__undef__, True)
        self._row_values = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._section_name = (data.get("sectionName", obj.__undef__), dirty)
        if obj._section_name[0] is not None and obj._section_name[0] is not obj.__undef__:
            assert isinstance(obj._section_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._section_name[0], type(obj._section_name[0])))
            common.validate_format(obj._section_name[0], "None", None, None)
        obj._column_headers = []
        for item in data.get("columnHeaders") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._column_headers.append(item)
        obj._column_headers = (obj._column_headers, dirty)
        obj._row_values = []
        for item in data.get("rowValues") or []:
            obj._row_values.append(factory.create_object(item))
            factory.validate_type(obj._row_values[-1], "OracleDatabaseStatistic")
        obj._row_values = (obj._row_values, dirty)
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
        if "section_name" == "type" or (self.section_name is not self.__undef__ and (not (dirty and not self._section_name[1]))):
            dct["sectionName"] = dictify(self.section_name)
        if "column_headers" == "type" or (self.column_headers is not self.__undef__ and (not (dirty and not self._column_headers[1]))):
            dct["columnHeaders"] = dictify(self.column_headers)
        if "row_values" == "type" or (self.row_values is not self.__undef__ and (not (dirty and not self._row_values[1]))):
            dct["rowValues"] = dictify(self.row_values)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._section_name = (self._section_name[0], True)
        self._column_headers = (self._column_headers[0], True)
        self._row_values = (self._row_values[0], True)

    def is_dirty(self):
        return any([self._section_name[1], self._column_headers[1], self._row_values[1]])

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
        if not isinstance(other, OracleDatabaseStatsSection):
            return False
        return super().__eq__(other) and \
               self.section_name == other.section_name and \
               self.column_headers == other.column_headers and \
               self.row_values == other.row_values

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def section_name(self):
        """
        Database statistic section name.

        :rtype: ``str``
        """
        return self._section_name[0]

    @section_name.setter
    def section_name(self, value):
        self._section_name = (value, True)

    @property
    def column_headers(self):
        """
        List of statistic column headers.

        :rtype: ``list`` of ``str``
        """
        return self._column_headers[0]

    @column_headers.setter
    def column_headers(self, value):
        self._column_headers = (value, True)

    @property
    def row_values(self):
        """
        List of statistic rows corresponding to column headers.

        :rtype: ``list`` of :py:class:`v1_11_20.web.vo.OracleDatabaseStatistic`
        """
        return self._row_values[0]

    @row_values.setter
    def row_values(self, value):
        self._row_values = (value, True)

