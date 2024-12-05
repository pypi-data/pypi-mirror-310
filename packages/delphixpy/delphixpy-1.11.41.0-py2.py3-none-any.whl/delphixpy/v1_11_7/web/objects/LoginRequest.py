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
#     /delphix-loginrequest.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_7.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_7 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class LoginRequest(TypedObject):
    """
    *(extends* :py:class:`v1_11_7.web.vo.TypedObject` *)* Represents a Delphix
    user authentication request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("LoginRequest", True)
        self._username = (self.__undef__, True)
        self._password = (self.__undef__, True)
        self._keep_alive_mode = (self.__undef__, True)
        self._target = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "username" not in data:
            raise ValueError("Missing required property \"username\".")
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        if "password" not in data:
            raise ValueError("Missing required property \"password\".")
        obj._password = (data.get("password", obj.__undef__), dirty)
        if obj._password[0] is not None and obj._password[0] is not obj.__undef__:
            assert isinstance(obj._password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._password[0], type(obj._password[0])))
            common.validate_format(obj._password[0], "password", None, None)
        obj._keep_alive_mode = (data.get("keepAliveMode", obj.__undef__), dirty)
        if obj._keep_alive_mode[0] is not None and obj._keep_alive_mode[0] is not obj.__undef__:
            assert isinstance(obj._keep_alive_mode[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._keep_alive_mode[0], type(obj._keep_alive_mode[0])))
            assert obj._keep_alive_mode[0] in ['ALL_REQUESTS', 'KEEP_ALIVE_HEADER_ONLY'], "Expected enum ['ALL_REQUESTS', 'KEEP_ALIVE_HEADER_ONLY'] but got %s" % obj._keep_alive_mode[0]
            common.validate_format(obj._keep_alive_mode[0], "None", None, None)
        obj._target = (data.get("target", obj.__undef__), dirty)
        if obj._target[0] is not None and obj._target[0] is not obj.__undef__:
            assert isinstance(obj._target[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target[0], type(obj._target[0])))
            assert obj._target[0] in ['DOMAIN', 'SYSTEM'], "Expected enum ['DOMAIN', 'SYSTEM'] but got %s" % obj._target[0]
            common.validate_format(obj._target[0], "None", None, None)
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
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]) or self.is_dirty_list(self.username, self._username) or belongs_to_parent)):
            dct["username"] = dictify(self.username)
        if "password" == "type" or (self.password is not self.__undef__ and (not (dirty and not self._password[1]) or self.is_dirty_list(self.password, self._password) or belongs_to_parent)):
            dct["password"] = dictify(self.password)
        if "keep_alive_mode" == "type" or (self.keep_alive_mode is not self.__undef__ and (not (dirty and not self._keep_alive_mode[1]))):
            dct["keepAliveMode"] = dictify(self.keep_alive_mode)
        if "target" == "type" or (self.target is not self.__undef__ and (not (dirty and not self._target[1]))):
            dct["target"] = dictify(self.target)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._username = (self._username[0], True)
        self._password = (self._password[0], True)
        self._keep_alive_mode = (self._keep_alive_mode[0], True)
        self._target = (self._target[0], True)

    def is_dirty(self):
        return any([self._username[1], self._password[1], self._keep_alive_mode[1], self._target[1]])

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
        if not isinstance(other, LoginRequest):
            return False
        return super().__eq__(other) and \
               self.username == other.username and \
               self.password == other.password and \
               self.keep_alive_mode == other.keep_alive_mode and \
               self.target == other.target

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def username(self):
        """
        The username of the user to authenticate.

        :rtype: ``str``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def password(self):
        """
        The password of the user to authenticate.

        :rtype: ``str``
        """
        return self._password[0]

    @password.setter
    def password(self, value):
        self._password = (value, True)

    @property
    def keep_alive_mode(self):
        """
        *(default value: ALL_REQUESTS)* Whether to keep session alive for all
        requests or only via 'KeepSessionAlive' request headers. Defaults to
        ALL_REQUESTS if omitted. *(permitted values: ALL_REQUESTS,
        KEEP_ALIVE_HEADER_ONLY)*

        :rtype: ``str``
        """
        return self._keep_alive_mode[0]

    @keep_alive_mode.setter
    def keep_alive_mode(self, value):
        self._keep_alive_mode = (value, True)

    @property
    def target(self):
        """
        The authentication domain. *(permitted values: DOMAIN, SYSTEM)*

        :rtype: ``str``
        """
        return self._target[0]

    @target.setter
    def target(self, value):
        self._target = (value, True)

