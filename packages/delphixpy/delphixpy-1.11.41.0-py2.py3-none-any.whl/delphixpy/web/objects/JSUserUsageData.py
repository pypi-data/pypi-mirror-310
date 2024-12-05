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
#     /delphix-js-user-usage-data.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.TypedObject import TypedObject
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSUserUsageData(TypedObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.TypedObject` *)* The space usage
    information for a Self-Service user.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSUserUsageData", True)
        self._user = (self.__undef__, True)
        self._total = (self.__undef__, True)
        self._num_containers = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._user = (data.get("user", obj.__undef__), dirty)
        if obj._user[0] is not None and obj._user[0] is not obj.__undef__:
            assert isinstance(obj._user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user[0], type(obj._user[0])))
            common.validate_format(obj._user[0], "objectReference", None, None)
        obj._total = (data.get("total", obj.__undef__), dirty)
        if obj._total[0] is not None and obj._total[0] is not obj.__undef__:
            assert isinstance(obj._total[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._total[0], type(obj._total[0])))
            common.validate_format(obj._total[0], "None", None, None)
        obj._num_containers = (data.get("numContainers", obj.__undef__), dirty)
        if obj._num_containers[0] is not None and obj._num_containers[0] is not obj.__undef__:
            assert isinstance(obj._num_containers[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._num_containers[0], type(obj._num_containers[0])))
            common.validate_format(obj._num_containers[0], "None", None, None)
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
        if "user" == "type" or (self.user is not self.__undef__ and (not (dirty and not self._user[1]))):
            dct["user"] = dictify(self.user)
        if "total" == "type" or (self.total is not self.__undef__ and (not (dirty and not self._total[1]))):
            dct["total"] = dictify(self.total)
        if "num_containers" == "type" or (self.num_containers is not self.__undef__ and (not (dirty and not self._num_containers[1]))):
            dct["numContainers"] = dictify(self.num_containers)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._user = (self._user[0], True)
        self._total = (self._total[0], True)
        self._num_containers = (self._num_containers[0], True)

    def is_dirty(self):
        return any([self._user[1], self._total[1], self._num_containers[1]])

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
        if not isinstance(other, JSUserUsageData):
            return False
        return super().__eq__(other) and \
               self.user == other.user and \
               self.total == other.total and \
               self.num_containers == other.num_containers

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def user(self):
        """
        The user.

        :rtype: ``str``
        """
        return self._user[0]

    @user.setter
    def user(self, value):
        self._user = (value, True)

    @property
    def total(self):
        """
        The amount of space referenced by the data containers owned by this
        user.

        :rtype: ``float``
        """
        return self._total[0]

    @total.setter
    def total(self, value):
        self._total = (value, True)

    @property
    def num_containers(self):
        """
        The number of containers owned by this user.

        :rtype: ``int``
        """
        return self._num_containers[0]

    @num_containers.setter
    def num_containers(self, value):
        self._num_containers = (value, True)

