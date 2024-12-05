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
#     /delphix-failback-capability.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class FailbackCapability(TypedObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TypedObject` *)* A replica
    namespace's failback capability.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("FailbackCapability", True)
        self._capability = (self.__undef__, True)
        self._incapability_reason = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._capability = (data.get("capability", obj.__undef__), dirty)
        if obj._capability[0] is not None and obj._capability[0] is not obj.__undef__:
            assert isinstance(obj._capability[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._capability[0], type(obj._capability[0])))
            assert obj._capability[0] in ['FAILBACK_READY', 'FAILBACK_COMPATIBLE', 'FAILBACK_INCOMPATIBLE', 'FAILBACK_UNSUPPORTED', 'FAILOVER_COMMITED_CANNOT_FAILBACK'], "Expected enum ['FAILBACK_READY', 'FAILBACK_COMPATIBLE', 'FAILBACK_INCOMPATIBLE', 'FAILBACK_UNSUPPORTED', 'FAILOVER_COMMITED_CANNOT_FAILBACK'] but got %s" % obj._capability[0]
            common.validate_format(obj._capability[0], "None", None, None)
        obj._incapability_reason = (data.get("incapabilityReason", obj.__undef__), dirty)
        if obj._incapability_reason[0] is not None and obj._incapability_reason[0] is not obj.__undef__:
            assert isinstance(obj._incapability_reason[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._incapability_reason[0], type(obj._incapability_reason[0])))
            common.validate_format(obj._incapability_reason[0], "None", None, None)
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
        if "capability" == "type" or (self.capability is not self.__undef__ and (not (dirty and not self._capability[1]))):
            dct["capability"] = dictify(self.capability)
        if "incapability_reason" == "type" or (self.incapability_reason is not self.__undef__ and (not (dirty and not self._incapability_reason[1]))):
            dct["incapabilityReason"] = dictify(self.incapability_reason)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._capability = (self._capability[0], True)
        self._incapability_reason = (self._incapability_reason[0], True)

    def is_dirty(self):
        return any([self._capability[1], self._incapability_reason[1]])

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
        if not isinstance(other, FailbackCapability):
            return False
        return super().__eq__(other) and \
               self.capability == other.capability and \
               self.incapability_reason == other.incapability_reason

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def capability(self):
        """
        Whether the namespace is capable of failback. *(permitted values:
        FAILBACK_READY, FAILBACK_COMPATIBLE, FAILBACK_INCOMPATIBLE,
        FAILBACK_UNSUPPORTED, FAILOVER_COMMITED_CANNOT_FAILBACK)*

        :rtype: ``str``
        """
        return self._capability[0]

    @capability.setter
    def capability(self, value):
        self._capability = (value, True)

    @property
    def incapability_reason(self):
        """
        Reason why the namespace is not capable of failback.

        :rtype: ``str``
        """
        return self._incapability_reason[0]

    @incapability_reason.setter
    def incapability_reason(self, value):
        self._incapability_reason = (value, True)

