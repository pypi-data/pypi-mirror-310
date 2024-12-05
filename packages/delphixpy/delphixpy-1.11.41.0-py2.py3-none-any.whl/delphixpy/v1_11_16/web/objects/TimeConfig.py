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
#     /delphix-time-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_16 import factory
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TimeConfig(TypedObject):
    """
    *(extends* :py:class:`v1_11_16.web.vo.TypedObject` *)* Get and set the
    current time configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TimeConfig", True)
        self._current_time = (self.__undef__, True)
        self._system_time_zone = (self.__undef__, True)
        self._system_time_zone_offset = (self.__undef__, True)
        self._system_time_zone_offset_string = (self.__undef__, True)
        self._ntp_config = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._current_time = (data.get("currentTime", obj.__undef__), dirty)
        if obj._current_time[0] is not None and obj._current_time[0] is not obj.__undef__:
            assert isinstance(obj._current_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._current_time[0], type(obj._current_time[0])))
            common.validate_format(obj._current_time[0], "date", None, None)
        obj._system_time_zone = (data.get("systemTimeZone", obj.__undef__), dirty)
        if obj._system_time_zone[0] is not None and obj._system_time_zone[0] is not obj.__undef__:
            assert isinstance(obj._system_time_zone[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._system_time_zone[0], type(obj._system_time_zone[0])))
            common.validate_format(obj._system_time_zone[0], "None", None, None)
        obj._system_time_zone_offset = (data.get("systemTimeZoneOffset", obj.__undef__), dirty)
        if obj._system_time_zone_offset[0] is not None and obj._system_time_zone_offset[0] is not obj.__undef__:
            assert isinstance(obj._system_time_zone_offset[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._system_time_zone_offset[0], type(obj._system_time_zone_offset[0])))
            common.validate_format(obj._system_time_zone_offset[0], "None", None, None)
        obj._system_time_zone_offset_string = (data.get("systemTimeZoneOffsetString", obj.__undef__), dirty)
        if obj._system_time_zone_offset_string[0] is not None and obj._system_time_zone_offset_string[0] is not obj.__undef__:
            assert isinstance(obj._system_time_zone_offset_string[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._system_time_zone_offset_string[0], type(obj._system_time_zone_offset_string[0])))
            common.validate_format(obj._system_time_zone_offset_string[0], "None", None, None)
        if "ntpConfig" in data and data["ntpConfig"] is not None:
            obj._ntp_config = (factory.create_object(data["ntpConfig"], "NTPConfig"), dirty)
            factory.validate_type(obj._ntp_config[0], "NTPConfig")
        else:
            obj._ntp_config = (obj.__undef__, dirty)
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
        if "current_time" == "type" or (self.current_time is not self.__undef__ and (not (dirty and not self._current_time[1]) or self.is_dirty_list(self.current_time, self._current_time) or belongs_to_parent)):
            dct["currentTime"] = dictify(self.current_time)
        if "system_time_zone" == "type" or (self.system_time_zone is not self.__undef__ and (not (dirty and not self._system_time_zone[1]) or self.is_dirty_list(self.system_time_zone, self._system_time_zone) or belongs_to_parent)):
            dct["systemTimeZone"] = dictify(self.system_time_zone)
        elif belongs_to_parent and self.system_time_zone is self.__undef__:
            dct["systemTimeZone"] = "Etc/UTC"
        if "system_time_zone_offset" == "type" or (self.system_time_zone_offset is not self.__undef__ and (not (dirty and not self._system_time_zone_offset[1]))):
            dct["systemTimeZoneOffset"] = dictify(self.system_time_zone_offset)
        if "system_time_zone_offset_string" == "type" or (self.system_time_zone_offset_string is not self.__undef__ and (not (dirty and not self._system_time_zone_offset_string[1]))):
            dct["systemTimeZoneOffsetString"] = dictify(self.system_time_zone_offset_string)
        if "ntp_config" == "type" or (self.ntp_config is not self.__undef__ and (not (dirty and not self._ntp_config[1]) or self.is_dirty_list(self.ntp_config, self._ntp_config) or belongs_to_parent)):
            dct["ntpConfig"] = dictify(self.ntp_config, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._current_time = (self._current_time[0], True)
        self._system_time_zone = (self._system_time_zone[0], True)
        self._system_time_zone_offset = (self._system_time_zone_offset[0], True)
        self._system_time_zone_offset_string = (self._system_time_zone_offset_string[0], True)
        self._ntp_config = (self._ntp_config[0], True)

    def is_dirty(self):
        return any([self._current_time[1], self._system_time_zone[1], self._system_time_zone_offset[1], self._system_time_zone_offset_string[1], self._ntp_config[1]])

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
        if not isinstance(other, TimeConfig):
            return False
        return super().__eq__(other) and \
               self.current_time == other.current_time and \
               self.system_time_zone == other.system_time_zone and \
               self.system_time_zone_offset == other.system_time_zone_offset and \
               self.system_time_zone_offset_string == other.system_time_zone_offset_string and \
               self.ntp_config == other.ntp_config

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def current_time(self):
        """
        Current system time. This value can only be set if NTP is disabled. The
        management service is automatically restarted if the time is changed.

        :rtype: ``str``
        """
        return self._current_time[0]

    @current_time.setter
    def current_time(self, value):
        self._current_time = (value, True)

    @property
    def system_time_zone(self):
        """
        *(default value: Etc/UTC)* Default time zone for system wide policies
        and schedules. The management service is automatically restarted if the
        timezone is changed.

        :rtype: ``str``
        """
        return self._system_time_zone[0]

    @system_time_zone.setter
    def system_time_zone(self, value):
        self._system_time_zone = (value, True)

    @property
    def system_time_zone_offset(self):
        """
        The difference, in minutes, between UTC and local time. For example, if
        your time zone is UTC -5:00 (Eastern Standard Time), 300 will be
        returned. Daylight saving time prevents this value from being a
        constant even for a given locale.

        :rtype: ``int``
        """
        return self._system_time_zone_offset[0]

    @system_time_zone_offset.setter
    def system_time_zone_offset(self, value):
        self._system_time_zone_offset = (value, True)

    @property
    def system_time_zone_offset_string(self):
        """
        System time zone offset as a String. For instance 'UTC -5:00'.

        :rtype: ``str``
        """
        return self._system_time_zone_offset_string[0]

    @system_time_zone_offset_string.setter
    def system_time_zone_offset_string(self, value):
        self._system_time_zone_offset_string = (value, True)

    @property
    def ntp_config(self):
        """
        NTP configuration.

        :rtype: :py:class:`v1_11_16.web.vo.NTPConfig`
        """
        return self._ntp_config[0]

    @ntp_config.setter
    def ntp_config(self, value):
        self._ntp_config = (value, True)

