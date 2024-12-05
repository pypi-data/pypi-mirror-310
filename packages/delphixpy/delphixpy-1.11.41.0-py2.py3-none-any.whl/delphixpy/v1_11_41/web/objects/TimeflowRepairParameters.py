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
#     /delphix-timeflow-repair-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_41.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_41 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class TimeflowRepairParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_41.web.vo.TypedObject` *)* Parameters to repair
    log files within a TimeFlow.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("TimeflowRepairParameters", True)
        self._start_location = (self.__undef__, True)
        self._end_location = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "startLocation" not in data:
            raise ValueError("Missing required property \"startLocation\".")
        obj._start_location = (data.get("startLocation", obj.__undef__), dirty)
        if obj._start_location[0] is not None and obj._start_location[0] is not obj.__undef__:
            assert isinstance(obj._start_location[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_location[0], type(obj._start_location[0])))
            common.validate_format(obj._start_location[0], "None", None, None)
        if "endLocation" not in data:
            raise ValueError("Missing required property \"endLocation\".")
        obj._end_location = (data.get("endLocation", obj.__undef__), dirty)
        if obj._end_location[0] is not None and obj._end_location[0] is not obj.__undef__:
            assert isinstance(obj._end_location[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._end_location[0], type(obj._end_location[0])))
            common.validate_format(obj._end_location[0], "None", None, None)
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
        if "start_location" == "type" or (self.start_location is not self.__undef__ and (not (dirty and not self._start_location[1]) or self.is_dirty_list(self.start_location, self._start_location) or belongs_to_parent)):
            dct["startLocation"] = dictify(self.start_location)
        if "end_location" == "type" or (self.end_location is not self.__undef__ and (not (dirty and not self._end_location[1]) or self.is_dirty_list(self.end_location, self._end_location) or belongs_to_parent)):
            dct["endLocation"] = dictify(self.end_location)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._start_location = (self._start_location[0], True)
        self._end_location = (self._end_location[0], True)

    def is_dirty(self):
        return any([self._start_location[1], self._end_location[1]])

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
        if not isinstance(other, TimeflowRepairParameters):
            return False
        return super().__eq__(other) and \
               self.start_location == other.start_location and \
               self.end_location == other.end_location

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def start_location(self):
        """
        The starting point of the range of log files to fetch.

        :rtype: ``str``
        """
        return self._start_location[0]

    @start_location.setter
    def start_location(self, value):
        self._start_location = (value, True)

    @property
    def end_location(self):
        """
        The ending point of the range of log files to fetch.

        :rtype: ``str``
        """
        return self._end_location[0]

    @end_location.setter
    def end_location(self, value):
        self._end_location = (value, True)

