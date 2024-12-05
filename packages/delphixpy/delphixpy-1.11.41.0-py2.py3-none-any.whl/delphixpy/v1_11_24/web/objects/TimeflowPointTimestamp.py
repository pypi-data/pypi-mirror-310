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
#     /delphix-timeflow-point-timestamp.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_24.web.objects.TimeflowPointParameters import TimeflowPointParameters
from delphixpy.v1_11_24 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TimeflowPointTimestamp(TimeflowPointParameters):
    """
    *(extends* :py:class:`v1_11_24.web.vo.TimeflowPointParameters` *)* TimeFlow
    point based on a timestamp.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TimeflowPointTimestamp", True)
        self._timestamp = (self.__undef__, True)
        self._timeflow = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "timestamp" not in data:
            raise ValueError("Missing required property \"timestamp\".")
        obj._timestamp = (data.get("timestamp", obj.__undef__), dirty)
        if obj._timestamp[0] is not None and obj._timestamp[0] is not obj.__undef__:
            assert isinstance(obj._timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._timestamp[0], type(obj._timestamp[0])))
            common.validate_format(obj._timestamp[0], "date", None, None)
        if "timeflow" not in data:
            raise ValueError("Missing required property \"timeflow\".")
        obj._timeflow = (data.get("timeflow", obj.__undef__), dirty)
        if obj._timeflow[0] is not None and obj._timeflow[0] is not obj.__undef__:
            assert isinstance(obj._timeflow[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._timeflow[0], type(obj._timeflow[0])))
            common.validate_format(obj._timeflow[0], "objectReference", None, None)
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
        if "timestamp" == "type" or (self.timestamp is not self.__undef__ and (not (dirty and not self._timestamp[1]) or self.is_dirty_list(self.timestamp, self._timestamp) or belongs_to_parent)):
            dct["timestamp"] = dictify(self.timestamp)
        if "timeflow" == "type" or (self.timeflow is not self.__undef__ and (not (dirty and not self._timeflow[1]) or self.is_dirty_list(self.timeflow, self._timeflow) or belongs_to_parent)):
            dct["timeflow"] = dictify(self.timeflow)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._timestamp = (self._timestamp[0], True)
        self._timeflow = (self._timeflow[0], True)

    def is_dirty(self):
        return any([self._timestamp[1], self._timeflow[1]])

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
        if not isinstance(other, TimeflowPointTimestamp):
            return False
        return super().__eq__(other) and \
               self.timestamp == other.timestamp and \
               self.timeflow == other.timeflow

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def timestamp(self):
        """
        The logical time corresponding to the TimeFlow location.

        :rtype: ``str``
        """
        return self._timestamp[0]

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = (value, True)

    @property
    def timeflow(self):
        """
        Reference to TimeFlow containing this point.

        :rtype: ``str``
        """
        return self._timeflow[0]

    @timeflow.setter
    def timeflow(self, value):
        self._timeflow = (value, True)

