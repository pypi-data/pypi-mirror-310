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
#     /delphix-retention-policy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_24.web.objects.Policy import Policy
from delphixpy.v1_11_24 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RetentionPolicy(Policy):
    """
    *(extends* :py:class:`v1_11_24.web.vo.Policy` *)* This policy controls what
    data (log and snapshot) is kept.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RetentionPolicy", True)
        self._data_duration = (self.__undef__, True)
        self._data_unit = (self.__undef__, True)
        self._log_duration = (self.__undef__, True)
        self._log_unit = (self.__undef__, True)
        self._num_of_daily = (self.__undef__, True)
        self._num_of_weekly = (self.__undef__, True)
        self._day_of_week = (self.__undef__, True)
        self._num_of_monthly = (self.__undef__, True)
        self._day_of_month = (self.__undef__, True)
        self._num_of_yearly = (self.__undef__, True)
        self._day_of_year = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._data_duration = (data.get("dataDuration", obj.__undef__), dirty)
        if obj._data_duration[0] is not None and obj._data_duration[0] is not obj.__undef__:
            assert isinstance(obj._data_duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._data_duration[0], type(obj._data_duration[0])))
            common.validate_format(obj._data_duration[0], "None", None, None)
        obj._data_unit = (data.get("dataUnit", obj.__undef__), dirty)
        if obj._data_unit[0] is not None and obj._data_unit[0] is not obj.__undef__:
            assert isinstance(obj._data_unit[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._data_unit[0], type(obj._data_unit[0])))
            assert obj._data_unit[0] in ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'], "Expected enum ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'] but got %s" % obj._data_unit[0]
            common.validate_format(obj._data_unit[0], "None", None, None)
        obj._log_duration = (data.get("logDuration", obj.__undef__), dirty)
        if obj._log_duration[0] is not None and obj._log_duration[0] is not obj.__undef__:
            assert isinstance(obj._log_duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._log_duration[0], type(obj._log_duration[0])))
            common.validate_format(obj._log_duration[0], "None", None, None)
        obj._log_unit = (data.get("logUnit", obj.__undef__), dirty)
        if obj._log_unit[0] is not None and obj._log_unit[0] is not obj.__undef__:
            assert isinstance(obj._log_unit[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._log_unit[0], type(obj._log_unit[0])))
            assert obj._log_unit[0] in ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'], "Expected enum ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'] but got %s" % obj._log_unit[0]
            common.validate_format(obj._log_unit[0], "None", None, None)
        obj._num_of_daily = (data.get("numOfDaily", obj.__undef__), dirty)
        if obj._num_of_daily[0] is not None and obj._num_of_daily[0] is not obj.__undef__:
            assert isinstance(obj._num_of_daily[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_of_daily[0], type(obj._num_of_daily[0])))
            common.validate_format(obj._num_of_daily[0], "None", None, None)
        obj._num_of_weekly = (data.get("numOfWeekly", obj.__undef__), dirty)
        if obj._num_of_weekly[0] is not None and obj._num_of_weekly[0] is not obj.__undef__:
            assert isinstance(obj._num_of_weekly[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_of_weekly[0], type(obj._num_of_weekly[0])))
            common.validate_format(obj._num_of_weekly[0], "None", None, None)
        obj._day_of_week = (data.get("dayOfWeek", obj.__undef__), dirty)
        if obj._day_of_week[0] is not None and obj._day_of_week[0] is not obj.__undef__:
            assert isinstance(obj._day_of_week[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._day_of_week[0], type(obj._day_of_week[0])))
            assert obj._day_of_week[0] in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'], "Expected enum ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'] but got %s" % obj._day_of_week[0]
            common.validate_format(obj._day_of_week[0], "None", None, None)
        obj._num_of_monthly = (data.get("numOfMonthly", obj.__undef__), dirty)
        if obj._num_of_monthly[0] is not None and obj._num_of_monthly[0] is not obj.__undef__:
            assert isinstance(obj._num_of_monthly[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_of_monthly[0], type(obj._num_of_monthly[0])))
            common.validate_format(obj._num_of_monthly[0], "None", None, None)
        obj._day_of_month = (data.get("dayOfMonth", obj.__undef__), dirty)
        if obj._day_of_month[0] is not None and obj._day_of_month[0] is not obj.__undef__:
            assert isinstance(obj._day_of_month[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._day_of_month[0], type(obj._day_of_month[0])))
            common.validate_format(obj._day_of_month[0], "None", None, None)
        obj._num_of_yearly = (data.get("numOfYearly", obj.__undef__), dirty)
        if obj._num_of_yearly[0] is not None and obj._num_of_yearly[0] is not obj.__undef__:
            assert isinstance(obj._num_of_yearly[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_of_yearly[0], type(obj._num_of_yearly[0])))
            common.validate_format(obj._num_of_yearly[0], "None", None, None)
        obj._day_of_year = (data.get("dayOfYear", obj.__undef__), dirty)
        if obj._day_of_year[0] is not None and obj._day_of_year[0] is not obj.__undef__:
            assert isinstance(obj._day_of_year[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._day_of_year[0], type(obj._day_of_year[0])))
            common.validate_format(obj._day_of_year[0], "None", None, 32)
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
        if "data_duration" == "type" or (self.data_duration is not self.__undef__ and (not (dirty and not self._data_duration[1]) or self.is_dirty_list(self.data_duration, self._data_duration) or belongs_to_parent)):
            dct["dataDuration"] = dictify(self.data_duration)
        if "data_unit" == "type" or (self.data_unit is not self.__undef__ and (not (dirty and not self._data_unit[1]) or self.is_dirty_list(self.data_unit, self._data_unit) or belongs_to_parent)):
            dct["dataUnit"] = dictify(self.data_unit)
        if "log_duration" == "type" or (self.log_duration is not self.__undef__ and (not (dirty and not self._log_duration[1]) or self.is_dirty_list(self.log_duration, self._log_duration) or belongs_to_parent)):
            dct["logDuration"] = dictify(self.log_duration)
        if "log_unit" == "type" or (self.log_unit is not self.__undef__ and (not (dirty and not self._log_unit[1]) or self.is_dirty_list(self.log_unit, self._log_unit) or belongs_to_parent)):
            dct["logUnit"] = dictify(self.log_unit)
        if "num_of_daily" == "type" or (self.num_of_daily is not self.__undef__ and (not (dirty and not self._num_of_daily[1]) or self.is_dirty_list(self.num_of_daily, self._num_of_daily) or belongs_to_parent)):
            dct["numOfDaily"] = dictify(self.num_of_daily)
        if "num_of_weekly" == "type" or (self.num_of_weekly is not self.__undef__ and (not (dirty and not self._num_of_weekly[1]) or self.is_dirty_list(self.num_of_weekly, self._num_of_weekly) or belongs_to_parent)):
            dct["numOfWeekly"] = dictify(self.num_of_weekly)
        if "day_of_week" == "type" or (self.day_of_week is not self.__undef__ and (not (dirty and not self._day_of_week[1]) or self.is_dirty_list(self.day_of_week, self._day_of_week) or belongs_to_parent)):
            dct["dayOfWeek"] = dictify(self.day_of_week)
        if "num_of_monthly" == "type" or (self.num_of_monthly is not self.__undef__ and (not (dirty and not self._num_of_monthly[1]) or self.is_dirty_list(self.num_of_monthly, self._num_of_monthly) or belongs_to_parent)):
            dct["numOfMonthly"] = dictify(self.num_of_monthly)
        if "day_of_month" == "type" or (self.day_of_month is not self.__undef__ and (not (dirty and not self._day_of_month[1]) or self.is_dirty_list(self.day_of_month, self._day_of_month) or belongs_to_parent)):
            dct["dayOfMonth"] = dictify(self.day_of_month)
        if "num_of_yearly" == "type" or (self.num_of_yearly is not self.__undef__ and (not (dirty and not self._num_of_yearly[1]) or self.is_dirty_list(self.num_of_yearly, self._num_of_yearly) or belongs_to_parent)):
            dct["numOfYearly"] = dictify(self.num_of_yearly)
        if "day_of_year" == "type" or (self.day_of_year is not self.__undef__ and (not (dirty and not self._day_of_year[1]) or self.is_dirty_list(self.day_of_year, self._day_of_year) or belongs_to_parent)):
            dct["dayOfYear"] = dictify(self.day_of_year)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._data_duration = (self._data_duration[0], True)
        self._data_unit = (self._data_unit[0], True)
        self._log_duration = (self._log_duration[0], True)
        self._log_unit = (self._log_unit[0], True)
        self._num_of_daily = (self._num_of_daily[0], True)
        self._num_of_weekly = (self._num_of_weekly[0], True)
        self._day_of_week = (self._day_of_week[0], True)
        self._num_of_monthly = (self._num_of_monthly[0], True)
        self._day_of_month = (self._day_of_month[0], True)
        self._num_of_yearly = (self._num_of_yearly[0], True)
        self._day_of_year = (self._day_of_year[0], True)

    def is_dirty(self):
        return any([self._data_duration[1], self._data_unit[1], self._log_duration[1], self._log_unit[1], self._num_of_daily[1], self._num_of_weekly[1], self._day_of_week[1], self._num_of_monthly[1], self._day_of_month[1], self._num_of_yearly[1], self._day_of_year[1]])

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
        if not isinstance(other, RetentionPolicy):
            return False
        return super().__eq__(other) and \
               self.data_duration == other.data_duration and \
               self.data_unit == other.data_unit and \
               self.log_duration == other.log_duration and \
               self.log_unit == other.log_unit and \
               self.num_of_daily == other.num_of_daily and \
               self.num_of_weekly == other.num_of_weekly and \
               self.day_of_week == other.day_of_week and \
               self.num_of_monthly == other.num_of_monthly and \
               self.day_of_month == other.day_of_month and \
               self.num_of_yearly == other.num_of_yearly and \
               self.day_of_year == other.day_of_year

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def data_duration(self):
        """
        Amount of time (in dataUnit units) to keep source data.

        :rtype: ``int``
        """
        return self._data_duration[0]

    @data_duration.setter
    def data_duration(self, value):
        self._data_duration = (value, True)

    @property
    def data_unit(self):
        """
        Time unit for dataDuration. *(permitted values: DAY, WEEK, MONTH,
        QUARTER, YEAR)*

        :rtype: ``str``
        """
        return self._data_unit[0]

    @data_unit.setter
    def data_unit(self, value):
        self._data_unit = (value, True)

    @property
    def log_duration(self):
        """
        Amount of time (in logUnit units) to keep log data.

        :rtype: ``int``
        """
        return self._log_duration[0]

    @log_duration.setter
    def log_duration(self, value):
        self._log_duration = (value, True)

    @property
    def log_unit(self):
        """
        Time unit for logDuration. *(permitted values: DAY, WEEK, MONTH,
        QUARTER, YEAR)*

        :rtype: ``str``
        """
        return self._log_unit[0]

    @log_unit.setter
    def log_unit(self, value):
        self._log_unit = (value, True)

    @property
    def num_of_daily(self):
        """
        Number of daily snapshots to keep.

        :rtype: ``int``
        """
        return self._num_of_daily[0]

    @num_of_daily.setter
    def num_of_daily(self, value):
        self._num_of_daily = (value, True)

    @property
    def num_of_weekly(self):
        """
        Number of weekly snapshots to keep.

        :rtype: ``int``
        """
        return self._num_of_weekly[0]

    @num_of_weekly.setter
    def num_of_weekly(self, value):
        self._num_of_weekly = (value, True)

    @property
    def day_of_week(self):
        """
        Day of week upon which to enforce weekly snapshot retention.
        *(permitted values: MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,
        SATURDAY, SUNDAY)*

        :rtype: ``str``
        """
        return self._day_of_week[0]

    @day_of_week.setter
    def day_of_week(self, value):
        self._day_of_week = (value, True)

    @property
    def num_of_monthly(self):
        """
        Number of monthly snapshots to keep.

        :rtype: ``int``
        """
        return self._num_of_monthly[0]

    @num_of_monthly.setter
    def num_of_monthly(self, value):
        self._num_of_monthly = (value, True)

    @property
    def day_of_month(self):
        """
        Day of month upon which to enforce monthly snapshot retention.

        :rtype: ``int``
        """
        return self._day_of_month[0]

    @day_of_month.setter
    def day_of_month(self, value):
        self._day_of_month = (value, True)

    @property
    def num_of_yearly(self):
        """
        Number of yearly snapshots to keep.

        :rtype: ``int``
        """
        return self._num_of_yearly[0]

    @num_of_yearly.setter
    def num_of_yearly(self, value):
        self._num_of_yearly = (value, True)

    @property
    def day_of_year(self):
        """
        Day of year upon which to enforce yearly snapshot retention, expressed
        a month / day string (e.g., "Jan 1").

        :rtype: ``str``
        """
        return self._day_of_year[0]

    @day_of_year.setter
    def day_of_year(self, value):
        self._day_of_year = (value, True)

