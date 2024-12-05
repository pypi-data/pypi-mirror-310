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
#     /delphix-replica-retention-policy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.Policy import Policy
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ReplicaRetentionPolicy(Policy):
    """
    *(extends* :py:class:`v1_11_23.web.vo.Policy` *)* This policy controls how
    long replica objects are retained after they have been deleted on the
    replication source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ReplicaRetentionPolicy", True)
        self._duration = (self.__undef__, True)
        self._duration_unit = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._duration = (data.get("duration", obj.__undef__), dirty)
        if obj._duration[0] is not None and obj._duration[0] is not obj.__undef__:
            assert isinstance(obj._duration[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._duration[0], type(obj._duration[0])))
            common.validate_format(obj._duration[0], "None", None, None)
        obj._duration_unit = (data.get("durationUnit", obj.__undef__), dirty)
        if obj._duration_unit[0] is not None and obj._duration_unit[0] is not obj.__undef__:
            assert isinstance(obj._duration_unit[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._duration_unit[0], type(obj._duration_unit[0])))
            assert obj._duration_unit[0] in ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'], "Expected enum ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'] but got %s" % obj._duration_unit[0]
            common.validate_format(obj._duration_unit[0], "None", None, None)
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
        if "duration" == "type" or (self.duration is not self.__undef__ and (not (dirty and not self._duration[1]) or self.is_dirty_list(self.duration, self._duration) or belongs_to_parent)):
            dct["duration"] = dictify(self.duration)
        if "duration_unit" == "type" or (self.duration_unit is not self.__undef__ and (not (dirty and not self._duration_unit[1]) or self.is_dirty_list(self.duration_unit, self._duration_unit) or belongs_to_parent)):
            dct["durationUnit"] = dictify(self.duration_unit)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._duration = (self._duration[0], True)
        self._duration_unit = (self._duration_unit[0], True)

    def is_dirty(self):
        return any([self._duration[1], self._duration_unit[1]])

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
        if not isinstance(other, ReplicaRetentionPolicy):
            return False
        return super().__eq__(other) and \
               self.duration == other.duration and \
               self.duration_unit == other.duration_unit

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def duration(self):
        """
        Amount of time (in durationUnit units) to keep source data.

        :rtype: ``int``
        """
        return self._duration[0]

    @duration.setter
    def duration(self, value):
        self._duration = (value, True)

    @property
    def duration_unit(self):
        """
        Time unit for duration. *(permitted values: DAY, WEEK, MONTH, QUARTER,
        YEAR)*

        :rtype: ``str``
        """
        return self._duration_unit[0]

    @duration_unit.setter
    def duration_unit(self, value):
        self._duration_unit = (value, True)

