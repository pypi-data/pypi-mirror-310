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
#     /delphix-superuser-session.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.UserObject import UserObject
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SuperuserSession(UserObject):
    """
    *(extends* :py:class:`v1_11_39.web.vo.UserObject` *)* Audit logs for
    superuser sessions.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SuperuserSession", True)
        self._ip_address = (self.__undef__, True)
        self._start_time_utc = (self.__undef__, True)
        self._duration = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._ip_address = (data.get("ipAddress", obj.__undef__), dirty)
        if obj._ip_address[0] is not None and obj._ip_address[0] is not obj.__undef__:
            assert isinstance(obj._ip_address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ip_address[0], type(obj._ip_address[0])))
            common.validate_format(obj._ip_address[0], "None", None, None)
        obj._start_time_utc = (data.get("startTimeUTC", obj.__undef__), dirty)
        if obj._start_time_utc[0] is not None and obj._start_time_utc[0] is not obj.__undef__:
            assert isinstance(obj._start_time_utc[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_time_utc[0], type(obj._start_time_utc[0])))
            common.validate_format(obj._start_time_utc[0], "date", None, None)
        obj._duration = (data.get("duration", obj.__undef__), dirty)
        if obj._duration[0] is not None and obj._duration[0] is not obj.__undef__:
            assert isinstance(obj._duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._duration[0], type(obj._duration[0])))
            common.validate_format(obj._duration[0], "None", None, None)
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
        if "ip_address" == "type" or (self.ip_address is not self.__undef__ and (not (dirty and not self._ip_address[1]))):
            dct["ipAddress"] = dictify(self.ip_address)
        if "start_time_utc" == "type" or (self.start_time_utc is not self.__undef__ and (not (dirty and not self._start_time_utc[1]))):
            dct["startTimeUTC"] = dictify(self.start_time_utc)
        if "duration" == "type" or (self.duration is not self.__undef__ and (not (dirty and not self._duration[1]))):
            dct["duration"] = dictify(self.duration)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._ip_address = (self._ip_address[0], True)
        self._start_time_utc = (self._start_time_utc[0], True)
        self._duration = (self._duration[0], True)

    def is_dirty(self):
        return any([self._ip_address[1], self._start_time_utc[1], self._duration[1]])

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
        if not isinstance(other, SuperuserSession):
            return False
        return super().__eq__(other) and \
               self.ip_address == other.ip_address and \
               self.start_time_utc == other.start_time_utc and \
               self.duration == other.duration

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def ip_address(self):
        """
        IP address from where the session was initiated.

        :rtype: ``str``
        """
        return self._ip_address[0]

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = (value, True)

    @property
    def start_time_utc(self):
        """
        Start time of the session.

        :rtype: ``str``
        """
        return self._start_time_utc[0]

    @start_time_utc.setter
    def start_time_utc(self, value):
        self._start_time_utc = (value, True)

    @property
    def duration(self):
        """
        Duration of the session in seconds.

        :rtype: ``int``
        """
        return self._duration[0]

    @duration.setter
    def duration(self, value):
        self._duration = (value, True)

