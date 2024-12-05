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
#     /delphix-analytics-cpu-util-datapoint.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.Datapoint import Datapoint
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CpuUtilDatapoint(Datapoint):
    """
    *(extends* :py:class:`v1_11_21.web.vo.Datapoint` *)* An analytics datapoint
    generated by the CPU_UTIL statistic type.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CpuUtilDatapoint", True)
        self._idle = (self.__undef__, True)
        self._kernel = (self.__undef__, True)
        self._user = (self.__undef__, True)
        self._dtrace = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._idle = (data.get("idle", obj.__undef__), dirty)
        if obj._idle[0] is not None and obj._idle[0] is not obj.__undef__:
            assert isinstance(obj._idle[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._idle[0], type(obj._idle[0])))
            common.validate_format(obj._idle[0], "None", None, None)
        obj._kernel = (data.get("kernel", obj.__undef__), dirty)
        if obj._kernel[0] is not None and obj._kernel[0] is not obj.__undef__:
            assert isinstance(obj._kernel[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._kernel[0], type(obj._kernel[0])))
            common.validate_format(obj._kernel[0], "None", None, None)
        obj._user = (data.get("user", obj.__undef__), dirty)
        if obj._user[0] is not None and obj._user[0] is not obj.__undef__:
            assert isinstance(obj._user[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._user[0], type(obj._user[0])))
            common.validate_format(obj._user[0], "None", None, None)
        obj._dtrace = (data.get("dtrace", obj.__undef__), dirty)
        if obj._dtrace[0] is not None and obj._dtrace[0] is not obj.__undef__:
            assert isinstance(obj._dtrace[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._dtrace[0], type(obj._dtrace[0])))
            common.validate_format(obj._dtrace[0], "None", None, None)
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
        if "idle" == "type" or (self.idle is not self.__undef__ and (not (dirty and not self._idle[1]))):
            dct["idle"] = dictify(self.idle)
        if "kernel" == "type" or (self.kernel is not self.__undef__ and (not (dirty and not self._kernel[1]))):
            dct["kernel"] = dictify(self.kernel)
        if "user" == "type" or (self.user is not self.__undef__ and (not (dirty and not self._user[1]))):
            dct["user"] = dictify(self.user)
        if "dtrace" == "type" or (self.dtrace is not self.__undef__ and (not (dirty and not self._dtrace[1]))):
            dct["dtrace"] = dictify(self.dtrace)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._idle = (self._idle[0], True)
        self._kernel = (self._kernel[0], True)
        self._user = (self._user[0], True)
        self._dtrace = (self._dtrace[0], True)

    def is_dirty(self):
        return any([self._idle[1], self._kernel[1], self._user[1], self._dtrace[1]])

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
        if not isinstance(other, CpuUtilDatapoint):
            return False
        return super().__eq__(other) and \
               self.idle == other.idle and \
               self.kernel == other.kernel and \
               self.user == other.user and \
               self.dtrace == other.dtrace

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def idle(self):
        """
        Idle time in milliseconds.

        :rtype: ``int``
        """
        return self._idle[0]

    @idle.setter
    def idle(self, value):
        self._idle = (value, True)

    @property
    def kernel(self):
        """
        Kernel time in milliseconds.

        :rtype: ``int``
        """
        return self._kernel[0]

    @kernel.setter
    def kernel(self, value):
        self._kernel = (value, True)

    @property
    def user(self):
        """
        User time in milliseconds.

        :rtype: ``int``
        """
        return self._user[0]

    @user.setter
    def user(self, value):
        self._user = (value, True)

    @property
    def dtrace(self):
        """
        DTrace time in milliseconds (subset of time in kernel).

        :rtype: ``int``
        """
        return self._dtrace[0]

    @dtrace.setter
    def dtrace(self, value):
        self._dtrace = (value, True)

