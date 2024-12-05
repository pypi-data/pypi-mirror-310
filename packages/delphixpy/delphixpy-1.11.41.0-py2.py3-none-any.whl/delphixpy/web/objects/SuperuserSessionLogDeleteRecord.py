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

from delphixpy.web.objects.TypedObject import TypedObject
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SuperuserSessionLogDeleteRecord(TypedObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.TypedObject` *)* Represents a
    deletion of a Delphix superuser session log file.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SuperuserSessionLogDeleteRecord", True)
        self._user = (self.__undef__, True)
        self._user_ip_address = (self.__undef__, True)
        self._log_name = (self.__undef__, True)
        self._succeeded = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "user" not in data:
            raise ValueError("Missing required property \"user\".")
        obj._user = (data.get("user", obj.__undef__), dirty)
        if obj._user[0] is not None and obj._user[0] is not obj.__undef__:
            assert isinstance(obj._user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user[0], type(obj._user[0])))
            common.validate_format(obj._user[0], "None", None, None)
        if "userIpAddress" not in data:
            raise ValueError("Missing required property \"userIpAddress\".")
        obj._user_ip_address = (data.get("userIpAddress", obj.__undef__), dirty)
        if obj._user_ip_address[0] is not None and obj._user_ip_address[0] is not obj.__undef__:
            assert isinstance(obj._user_ip_address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user_ip_address[0], type(obj._user_ip_address[0])))
            common.validate_format(obj._user_ip_address[0], "None", None, None)
        if "logName" not in data:
            raise ValueError("Missing required property \"logName\".")
        obj._log_name = (data.get("logName", obj.__undef__), dirty)
        if obj._log_name[0] is not None and obj._log_name[0] is not obj.__undef__:
            assert isinstance(obj._log_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._log_name[0], type(obj._log_name[0])))
            common.validate_format(obj._log_name[0], "None", None, None)
        if "succeeded" not in data:
            raise ValueError("Missing required property \"succeeded\".")
        obj._succeeded = (data.get("succeeded", obj.__undef__), dirty)
        if obj._succeeded[0] is not None and obj._succeeded[0] is not obj.__undef__:
            assert isinstance(obj._succeeded[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._succeeded[0], type(obj._succeeded[0])))
            common.validate_format(obj._succeeded[0], "None", None, None)
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
        if "user" == "type" or (self.user is not self.__undef__ and (not (dirty and not self._user[1]) or self.is_dirty_list(self.user, self._user) or belongs_to_parent)):
            dct["user"] = dictify(self.user)
        if "user_ip_address" == "type" or (self.user_ip_address is not self.__undef__ and (not (dirty and not self._user_ip_address[1]) or self.is_dirty_list(self.user_ip_address, self._user_ip_address) or belongs_to_parent)):
            dct["userIpAddress"] = dictify(self.user_ip_address)
        if "log_name" == "type" or (self.log_name is not self.__undef__ and (not (dirty and not self._log_name[1]) or self.is_dirty_list(self.log_name, self._log_name) or belongs_to_parent)):
            dct["logName"] = dictify(self.log_name)
        if "succeeded" == "type" or (self.succeeded is not self.__undef__ and (not (dirty and not self._succeeded[1]) or self.is_dirty_list(self.succeeded, self._succeeded) or belongs_to_parent)):
            dct["succeeded"] = dictify(self.succeeded)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._user = (self._user[0], True)
        self._user_ip_address = (self._user_ip_address[0], True)
        self._log_name = (self._log_name[0], True)
        self._succeeded = (self._succeeded[0], True)

    def is_dirty(self):
        return any([self._user[1], self._user_ip_address[1], self._log_name[1], self._succeeded[1]])

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
        if not isinstance(other, SuperuserSessionLogDeleteRecord):
            return False
        return super().__eq__(other) and \
               self.user == other.user and \
               self.user_ip_address == other.user_ip_address and \
               self.log_name == other.log_name and \
               self.succeeded == other.succeeded

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def user(self):
        """
        The user who deleted the log file.

        :rtype: ``str``
        """
        return self._user[0]

    @user.setter
    def user(self, value):
        self._user = (value, True)

    @property
    def user_ip_address(self):
        """
        Ip address of the user who deleted the log file.

        :rtype: ``str``
        """
        return self._user_ip_address[0]

    @user_ip_address.setter
    def user_ip_address(self, value):
        self._user_ip_address = (value, True)

    @property
    def log_name(self):
        """
        Name of the log file that was deleted.

        :rtype: ``str``
        """
        return self._log_name[0]

    @log_name.setter
    def log_name(self, value):
        self._log_name = (value, True)

    @property
    def succeeded(self):
        """
        Whether the delete action was successful.

        :rtype: ``bool``
        """
        return self._succeeded[0]

    @succeeded.setter
    def succeeded(self, value):
        self._succeeded = (value, True)

