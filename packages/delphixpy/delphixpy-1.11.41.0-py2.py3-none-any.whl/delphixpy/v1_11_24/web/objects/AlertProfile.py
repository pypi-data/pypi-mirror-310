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
#     /delphix-alert-profile.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_24.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_24 import factory
from delphixpy.v1_11_24 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AlertProfile(PersistentObject):
    """
    *(extends* :py:class:`v1_11_24.web.vo.PersistentObject` *)* A profile that
    describes a set of actions to take in response to an alert being generated.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AlertProfile", True)
        self._filter_spec = (self.__undef__, True)
        self._actions = (self.__undef__, True)
        self._user = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "filterSpec" in data and data["filterSpec"] is not None:
            obj._filter_spec = (factory.create_object(data["filterSpec"], "AlertFilter"), dirty)
            factory.validate_type(obj._filter_spec[0], "AlertFilter")
        else:
            obj._filter_spec = (obj.__undef__, dirty)
        obj._actions = []
        for item in data.get("actions") or []:
            obj._actions.append(factory.create_object(item))
            factory.validate_type(obj._actions[-1], "AlertAction")
        obj._actions = (obj._actions, dirty)
        obj._user = (data.get("user", obj.__undef__), dirty)
        if obj._user[0] is not None and obj._user[0] is not obj.__undef__:
            assert isinstance(obj._user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user[0], type(obj._user[0])))
            common.validate_format(obj._user[0], "objectReference", None, None)
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
        if "filter_spec" == "type" or (self.filter_spec is not self.__undef__ and (not (dirty and not self._filter_spec[1]) or self.is_dirty_list(self.filter_spec, self._filter_spec) or belongs_to_parent)):
            dct["filterSpec"] = dictify(self.filter_spec, prop_is_list_or_vo=True)
        if "actions" == "type" or (self.actions is not self.__undef__ and (not (dirty and not self._actions[1]) or self.is_dirty_list(self.actions, self._actions) or belongs_to_parent)):
            dct["actions"] = dictify(self.actions, prop_is_list_or_vo=True)
        if "user" == "type" or (self.user is not self.__undef__ and (not (dirty and not self._user[1]) or self.is_dirty_list(self.user, self._user) or belongs_to_parent)):
            dct["user"] = dictify(self.user)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._filter_spec = (self._filter_spec[0], True)
        self._actions = (self._actions[0], True)
        self._user = (self._user[0], True)

    def is_dirty(self):
        return any([self._filter_spec[1], self._actions[1], self._user[1]])

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
        if not isinstance(other, AlertProfile):
            return False
        return super().__eq__(other) and \
               self.filter_spec == other.filter_spec and \
               self.actions == other.actions and \
               self.user == other.user

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def filter_spec(self):
        """
        Specifies which alerts should be matched by this profile.

        :rtype: :py:class:`v1_11_24.web.vo.AlertFilter`
        """
        return self._filter_spec[0]

    @filter_spec.setter
    def filter_spec(self, value):
        self._filter_spec = (value, True)

    @property
    def actions(self):
        """
        List of actions to take. Only alerts visible to the user and matching
        the optional filters are included. If there are multiple actions with
        the same result (such as emailing a user), only one result is acted
        upon.

        :rtype: ``list`` of :py:class:`v1_11_24.web.vo.AlertAction`
        """
        return self._actions[0]

    @actions.setter
    def actions(self, value):
        self._actions = (value, True)

    @property
    def user(self):
        """
        User to which the alert profile is assigned. Defaults to the logged-in
        user.

        :rtype: ``str``
        """
        return self._user[0]

    @user.setter
    def user(self, value):
        self._user = (value, True)

