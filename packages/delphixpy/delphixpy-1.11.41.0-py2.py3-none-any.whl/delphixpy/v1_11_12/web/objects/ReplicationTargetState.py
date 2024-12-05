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
#     /delphix-replication-target-state.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_12.web.objects.UserObject import UserObject
from delphixpy.v1_11_12 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ReplicationTargetState(UserObject):
    """
    *(extends* :py:class:`v1_11_12.web.vo.UserObject` *)* State of a
    replication at the target.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ReplicationTargetState", True)
        self._last_known_source_version = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._last_known_source_version = (data.get("lastKnownSourceVersion", obj.__undef__), dirty)
        if obj._last_known_source_version[0] is not None and obj._last_known_source_version[0] is not obj.__undef__:
            assert isinstance(obj._last_known_source_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_known_source_version[0], type(obj._last_known_source_version[0])))
            common.validate_format(obj._last_known_source_version[0], "None", None, None)
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
        if "last_known_source_version" == "type" or (self.last_known_source_version is not self.__undef__ and (not (dirty and not self._last_known_source_version[1]))):
            dct["lastKnownSourceVersion"] = dictify(self.last_known_source_version)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._last_known_source_version = (self._last_known_source_version[0], True)

    def is_dirty(self):
        return any([self._last_known_source_version[1]])

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
        if not isinstance(other, ReplicationTargetState):
            return False
        return super().__eq__(other) and \
               self.last_known_source_version == other.last_known_source_version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def last_known_source_version(self):
        """
        The Delphix version of the source engine during the last replication of
        the namespace.

        :rtype: ``str``
        """
        return self._last_known_source_version[0]

    @last_known_source_version.setter
    def last_known_source_version(self, value):
        self._last_known_source_version = (value, True)

