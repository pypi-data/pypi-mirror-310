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
#     /delphix-policy.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.UserObject import UserObject
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Policy(UserObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.UserObject` *)* The base policy
    type.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Policy", True)
        self._default = (self.__undef__, True)
        self._customized = (self.__undef__, True)
        self._effective_type = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._default = (data.get("default", obj.__undef__), dirty)
        if obj._default[0] is not None and obj._default[0] is not obj.__undef__:
            assert isinstance(obj._default[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._default[0], type(obj._default[0])))
            common.validate_format(obj._default[0], "None", None, None)
        obj._customized = (data.get("customized", obj.__undef__), dirty)
        if obj._customized[0] is not None and obj._customized[0] is not obj.__undef__:
            assert isinstance(obj._customized[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._customized[0], type(obj._customized[0])))
            common.validate_format(obj._customized[0], "None", None, None)
        obj._effective_type = (data.get("effectiveType", obj.__undef__), dirty)
        if obj._effective_type[0] is not None and obj._effective_type[0] is not obj.__undef__:
            assert isinstance(obj._effective_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._effective_type[0], type(obj._effective_type[0])))
            assert obj._effective_type[0] in ['DIRECT_APPLIED', 'INHERITED'], "Expected enum ['DIRECT_APPLIED', 'INHERITED'] but got %s" % obj._effective_type[0]
            common.validate_format(obj._effective_type[0], "None", None, None)
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
        if "default" == "type" or (self.default is not self.__undef__ and (not (dirty and not self._default[1]))):
            dct["default"] = dictify(self.default)
        if "customized" == "type" or (self.customized is not self.__undef__ and (not (dirty and not self._customized[1]) or self.is_dirty_list(self.customized, self._customized) or belongs_to_parent)):
            dct["customized"] = dictify(self.customized)
        elif belongs_to_parent and self.customized is self.__undef__:
            dct["customized"] = False
        if "effective_type" == "type" or (self.effective_type is not self.__undef__ and (not (dirty and not self._effective_type[1]))):
            dct["effectiveType"] = dictify(self.effective_type)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._default = (self._default[0], True)
        self._customized = (self._customized[0], True)
        self._effective_type = (self._effective_type[0], True)

    def is_dirty(self):
        return any([self._default[1], self._customized[1], self._effective_type[1]])

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
        if not isinstance(other, Policy):
            return False
        return super().__eq__(other) and \
               self.default == other.default and \
               self.customized == other.customized and \
               self.effective_type == other.effective_type

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def default(self):
        """
        True if this is the default policy created when the system is setup.
        Default policies cannot be deleted.

        :rtype: ``bool``
        """
        return self._default[0]

    @default.setter
    def default(self, value):
        self._default = (value, True)

    @property
    def customized(self):
        """
        True if this policy is customized specifically for one object.
        Customized policies cannot be shared between objects.

        :rtype: ``bool``
        """
        return self._customized[0]

    @customized.setter
    def customized(self, value):
        self._customized = (value, True)

    @property
    def effective_type(self):
        """
        Whether this policy has been directly applied or inherited. See the
        effectivePolicies parameter of the list call for details. *(permitted
        values: DIRECT_APPLIED, INHERITED)*

        :rtype: ``str``
        """
        return self._effective_type[0]

    @effective_type.setter
    def effective_type(self, value):
        self._effective_type = (value, True)

