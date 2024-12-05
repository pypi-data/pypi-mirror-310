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
#     /delphix-timeflow-snapshot-day-range.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_26.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_26 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TimeflowSnapshotDayRange(TypedObject):
    """
    *(extends* :py:class:`v1_11_26.web.vo.TypedObject` *)* Count of TimeFlow
    snapshots aggregated by day.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TimeflowSnapshotDayRange", True)
        self._count = (self.__undef__, True)
        self._date = (self.__undef__, True)
        self._start_of_day = (self.__undef__, True)
        self._end_of_day = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._count = (data.get("count", obj.__undef__), dirty)
        if obj._count[0] is not None and obj._count[0] is not obj.__undef__:
            assert isinstance(obj._count[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._count[0], type(obj._count[0])))
            common.validate_format(obj._count[0], "None", None, None)
        obj._date = (data.get("date", obj.__undef__), dirty)
        if obj._date[0] is not None and obj._date[0] is not obj.__undef__:
            assert isinstance(obj._date[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._date[0], type(obj._date[0])))
            common.validate_format(obj._date[0], "None", None, None)
        obj._start_of_day = (data.get("startOfDay", obj.__undef__), dirty)
        if obj._start_of_day[0] is not None and obj._start_of_day[0] is not obj.__undef__:
            assert isinstance(obj._start_of_day[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_of_day[0], type(obj._start_of_day[0])))
            common.validate_format(obj._start_of_day[0], "date", None, None)
        obj._end_of_day = (data.get("endOfDay", obj.__undef__), dirty)
        if obj._end_of_day[0] is not None and obj._end_of_day[0] is not obj.__undef__:
            assert isinstance(obj._end_of_day[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._end_of_day[0], type(obj._end_of_day[0])))
            common.validate_format(obj._end_of_day[0], "date", None, None)
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
        if "count" == "type" or (self.count is not self.__undef__ and (not (dirty and not self._count[1]))):
            dct["count"] = dictify(self.count)
        if "date" == "type" or (self.date is not self.__undef__ and (not (dirty and not self._date[1]))):
            dct["date"] = dictify(self.date)
        if "start_of_day" == "type" or (self.start_of_day is not self.__undef__ and (not (dirty and not self._start_of_day[1]))):
            dct["startOfDay"] = dictify(self.start_of_day)
        if "end_of_day" == "type" or (self.end_of_day is not self.__undef__ and (not (dirty and not self._end_of_day[1]))):
            dct["endOfDay"] = dictify(self.end_of_day)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._count = (self._count[0], True)
        self._date = (self._date[0], True)
        self._start_of_day = (self._start_of_day[0], True)
        self._end_of_day = (self._end_of_day[0], True)

    def is_dirty(self):
        return any([self._count[1], self._date[1], self._start_of_day[1], self._end_of_day[1]])

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
        if not isinstance(other, TimeflowSnapshotDayRange):
            return False
        return super().__eq__(other) and \
               self.count == other.count and \
               self.date == other.date and \
               self.start_of_day == other.start_of_day and \
               self.end_of_day == other.end_of_day

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def count(self):
        """
        Number of TimeFlow snapshots on that day.

        :rtype: ``float``
        """
        return self._count[0]

    @count.setter
    def count(self, value):
        self._count = (value, True)

    @property
    def date(self):
        """
        Date for which TimeFlow snapshots have been aggregated.

        :rtype: ``str``
        """
        return self._date[0]

    @date.setter
    def date(self, value):
        self._date = (value, True)

    @property
    def start_of_day(self):
        """
        Start of day of this range in the time zone used for computation.

        :rtype: ``str``
        """
        return self._start_of_day[0]

    @start_of_day.setter
    def start_of_day(self, value):
        self._start_of_day = (value, True)

    @property
    def end_of_day(self):
        """
        End of day of this range in the time zone used for computation.

        :rtype: ``str``
        """
        return self._end_of_day[0]

    @end_of_day.setter
    def end_of_day(self, value):
        self._end_of_day = (value, True)

