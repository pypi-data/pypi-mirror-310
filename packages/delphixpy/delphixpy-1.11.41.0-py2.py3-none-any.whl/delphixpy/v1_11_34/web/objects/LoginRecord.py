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
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class LoginRecord(TypedObject):
    """
    *(extends* :py:class:`v1_11_34.web.vo.TypedObject` *)* Represents a failed
    SSO login.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("LoginRecord", True)
        self._user_agent = (self.__undef__, True)
        self._origin_ip = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "userAgent" not in data:
            raise ValueError("Missing required property \"userAgent\".")
        obj._user_agent = (data.get("userAgent", obj.__undef__), dirty)
        if obj._user_agent[0] is not None and obj._user_agent[0] is not obj.__undef__:
            assert isinstance(obj._user_agent[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user_agent[0], type(obj._user_agent[0])))
            common.validate_format(obj._user_agent[0], "None", None, None)
        if "originIp" not in data:
            raise ValueError("Missing required property \"originIp\".")
        obj._origin_ip = (data.get("originIp", obj.__undef__), dirty)
        if obj._origin_ip[0] is not None and obj._origin_ip[0] is not obj.__undef__:
            assert isinstance(obj._origin_ip[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._origin_ip[0], type(obj._origin_ip[0])))
            common.validate_format(obj._origin_ip[0], "None", None, None)
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
        if "user_agent" == "type" or (self.user_agent is not self.__undef__ and (not (dirty and not self._user_agent[1]) or self.is_dirty_list(self.user_agent, self._user_agent) or belongs_to_parent)):
            dct["userAgent"] = dictify(self.user_agent)
        if "origin_ip" == "type" or (self.origin_ip is not self.__undef__ and (not (dirty and not self._origin_ip[1]) or self.is_dirty_list(self.origin_ip, self._origin_ip) or belongs_to_parent)):
            dct["originIp"] = dictify(self.origin_ip)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._user_agent = (self._user_agent[0], True)
        self._origin_ip = (self._origin_ip[0], True)

    def is_dirty(self):
        return any([self._user_agent[1], self._origin_ip[1]])

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
        if not isinstance(other, LoginRecord):
            return False
        return super().__eq__(other) and \
               self.user_agent == other.user_agent and \
               self.origin_ip == other.origin_ip

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def user_agent(self):
        """
        Name of client software used to initiate the action.

        :rtype: ``str``
        """
        return self._user_agent[0]

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = (value, True)

    @property
    def origin_ip(self):
        """
        Network address used to initiate the action.

        :rtype: ``str``
        """
        return self._origin_ip[0]

    @origin_ip.setter
    def origin_ip(self, value):
        self._origin_ip = (value, True)

