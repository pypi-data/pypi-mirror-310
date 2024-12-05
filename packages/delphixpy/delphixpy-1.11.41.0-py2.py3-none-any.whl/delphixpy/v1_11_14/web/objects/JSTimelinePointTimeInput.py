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
#     /delphix-js-timeline-point-time-input.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.JSTimelinePointTimeParameters import JSTimelinePointTimeParameters
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSTimelinePointTimeInput(JSTimelinePointTimeParameters):
    """
    *(extends* :py:class:`v1_11_14.web.vo.JSTimelinePointTimeParameters` *)*
    Specifies a point in time on the Self-Service timeline for a specific
    branch. Latest provisionable points before the specified time will be used.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSTimelinePointTimeInput", True)
        self._time = (self.__undef__, True)
        self._branch = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "time" not in data:
            raise ValueError("Missing required property \"time\".")
        obj._time = (data.get("time", obj.__undef__), dirty)
        if obj._time[0] is not None and obj._time[0] is not obj.__undef__:
            assert isinstance(obj._time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._time[0], type(obj._time[0])))
            common.validate_format(obj._time[0], "date", None, None)
        if "branch" not in data:
            raise ValueError("Missing required property \"branch\".")
        obj._branch = (data.get("branch", obj.__undef__), dirty)
        if obj._branch[0] is not None and obj._branch[0] is not obj.__undef__:
            assert isinstance(obj._branch[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._branch[0], type(obj._branch[0])))
            common.validate_format(obj._branch[0], "objectReference", None, None)
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
        if "time" == "type" or (self.time is not self.__undef__ and (not (dirty and not self._time[1]) or self.is_dirty_list(self.time, self._time) or belongs_to_parent)):
            dct["time"] = dictify(self.time)
        if "branch" == "type" or (self.branch is not self.__undef__ and (not (dirty and not self._branch[1]) or self.is_dirty_list(self.branch, self._branch) or belongs_to_parent)):
            dct["branch"] = dictify(self.branch)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._time = (self._time[0], True)
        self._branch = (self._branch[0], True)

    def is_dirty(self):
        return any([self._time[1], self._branch[1]])

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
        if not isinstance(other, JSTimelinePointTimeInput):
            return False
        return super().__eq__(other) and \
               self.time == other.time and \
               self.branch == other.branch

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def time(self):
        """
        A point in time on the given branch.

        :rtype: ``str``
        """
        return self._time[0]

    @time.setter
    def time(self, value):
        self._time = (value, True)

    @property
    def branch(self):
        """
        The reference to the branch used for this operation.

        :rtype: ``str``
        """
        return self._branch[0]

    @branch.setter
    def branch(self, value):
        self._branch = (value, True)

