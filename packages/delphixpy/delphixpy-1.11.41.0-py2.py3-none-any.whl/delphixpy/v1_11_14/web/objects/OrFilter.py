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
#     /delphix-alert-or-filter.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.AlertFilter import AlertFilter
from delphixpy.v1_11_14 import factory
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OrFilter(AlertFilter):
    """
    *(extends* :py:class:`v1_11_14.web.vo.AlertFilter` *)* A container filter
    that combines other filters together using OR logic.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OrFilter", True)
        self._sub_filters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._sub_filters = []
        for item in data.get("subFilters") or []:
            obj._sub_filters.append(factory.create_object(item))
            factory.validate_type(obj._sub_filters[-1], "AlertFilter")
        obj._sub_filters = (obj._sub_filters, dirty)
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
        if "sub_filters" == "type" or (self.sub_filters is not self.__undef__ and (not (dirty and not self._sub_filters[1]) or self.is_dirty_list(self.sub_filters, self._sub_filters) or belongs_to_parent)):
            dct["subFilters"] = dictify(self.sub_filters, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._sub_filters = (self._sub_filters[0], True)

    def is_dirty(self):
        return any([self._sub_filters[1]])

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
        if not isinstance(other, OrFilter):
            return False
        return super().__eq__(other) and \
               self.sub_filters == other.sub_filters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def sub_filters(self):
        """
        Filters which are combined together using OR logic.

        :rtype: ``list`` of :py:class:`v1_11_14.web.vo.AlertFilter`
        """
        return self._sub_filters[0]

    @sub_filters.setter
    def sub_filters(self, value):
        self._sub_filters = (value, True)

