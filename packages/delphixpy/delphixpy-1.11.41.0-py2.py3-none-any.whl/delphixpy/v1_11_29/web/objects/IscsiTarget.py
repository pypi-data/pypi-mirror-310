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
#     /delphix-iscsi-target.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_29.web.objects.PersistentObject import PersistentObject
from delphixpy.v1_11_29 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class IscsiTarget(PersistentObject):
    """
    *(extends* :py:class:`v1_11_29.web.vo.PersistentObject` *)* Configuration
    of an iSCSI target endpoint.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("IscsiTarget", True)
        self._name = (self.__undef__, True)
        self._iqn = (self.__undef__, True)
        self._portal = (self.__undef__, True)
        self._port = (self.__undef__, True)
        self._chap_username = (self.__undef__, True)
        self._chap_password = (self.__undef__, True)
        self._chap_username_in = (self.__undef__, True)
        self._chap_password_in = (self.__undef__, True)
        self._state = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "objectName", None, None)
        obj._iqn = (data.get("iqn", obj.__undef__), dirty)
        if obj._iqn[0] is not None and obj._iqn[0] is not obj.__undef__:
            assert isinstance(obj._iqn[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._iqn[0], type(obj._iqn[0])))
            common.validate_format(obj._iqn[0], "None", None, None)
        obj._portal = (data.get("portal", obj.__undef__), dirty)
        if obj._portal[0] is not None and obj._portal[0] is not obj.__undef__:
            assert isinstance(obj._portal[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._portal[0], type(obj._portal[0])))
            common.validate_format(obj._portal[0], "host", None, None)
        obj._port = (data.get("port", obj.__undef__), dirty)
        if obj._port[0] is not None and obj._port[0] is not obj.__undef__:
            assert isinstance(obj._port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._port[0], type(obj._port[0])))
            common.validate_format(obj._port[0], "None", None, None)
        obj._chap_username = (data.get("chapUsername", obj.__undef__), dirty)
        if obj._chap_username[0] is not None and obj._chap_username[0] is not obj.__undef__:
            assert isinstance(obj._chap_username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._chap_username[0], type(obj._chap_username[0])))
            common.validate_format(obj._chap_username[0], "None", None, None)
        obj._chap_password = (data.get("chapPassword", obj.__undef__), dirty)
        if obj._chap_password[0] is not None and obj._chap_password[0] is not obj.__undef__:
            assert isinstance(obj._chap_password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._chap_password[0], type(obj._chap_password[0])))
            common.validate_format(obj._chap_password[0], "password", None, None)
        obj._chap_username_in = (data.get("chapUsernameIn", obj.__undef__), dirty)
        if obj._chap_username_in[0] is not None and obj._chap_username_in[0] is not obj.__undef__:
            assert isinstance(obj._chap_username_in[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._chap_username_in[0], type(obj._chap_username_in[0])))
            common.validate_format(obj._chap_username_in[0], "None", None, None)
        obj._chap_password_in = (data.get("chapPasswordIn", obj.__undef__), dirty)
        if obj._chap_password_in[0] is not None and obj._chap_password_in[0] is not obj.__undef__:
            assert isinstance(obj._chap_password_in[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._chap_password_in[0], type(obj._chap_password_in[0])))
            common.validate_format(obj._chap_password_in[0], "password", None, None)
        obj._state = (data.get("state", obj.__undef__), dirty)
        if obj._state[0] is not None and obj._state[0] is not obj.__undef__:
            assert isinstance(obj._state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state[0], type(obj._state[0])))
            assert obj._state[0] in ['NOT_CONNECTED', 'CONNECTED', 'IN_USE', 'ERROR'], "Expected enum ['NOT_CONNECTED', 'CONNECTED', 'IN_USE', 'ERROR'] but got %s" % obj._state[0]
            common.validate_format(obj._state[0], "None", None, None)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]))):
            dct["name"] = dictify(self.name)
        if "iqn" == "type" or (self.iqn is not self.__undef__ and (not (dirty and not self._iqn[1]) or self.is_dirty_list(self.iqn, self._iqn) or belongs_to_parent)):
            dct["iqn"] = dictify(self.iqn)
        if "portal" == "type" or (self.portal is not self.__undef__ and (not (dirty and not self._portal[1]) or self.is_dirty_list(self.portal, self._portal) or belongs_to_parent)):
            dct["portal"] = dictify(self.portal)
        if "port" == "type" or (self.port is not self.__undef__ and (not (dirty and not self._port[1]) or self.is_dirty_list(self.port, self._port) or belongs_to_parent)):
            dct["port"] = dictify(self.port)
        elif belongs_to_parent and self.port is self.__undef__:
            dct["port"] = 3260
        if "chap_username" == "type" or (self.chap_username is not self.__undef__ and (not (dirty and not self._chap_username[1]) or self.is_dirty_list(self.chap_username, self._chap_username) or belongs_to_parent)):
            dct["chapUsername"] = dictify(self.chap_username)
        if "chap_password" == "type" or (self.chap_password is not self.__undef__ and (not (dirty and not self._chap_password[1]) or self.is_dirty_list(self.chap_password, self._chap_password) or belongs_to_parent)):
            dct["chapPassword"] = dictify(self.chap_password)
        if "chap_username_in" == "type" or (self.chap_username_in is not self.__undef__ and (not (dirty and not self._chap_username_in[1]) or self.is_dirty_list(self.chap_username_in, self._chap_username_in) or belongs_to_parent)):
            dct["chapUsernameIn"] = dictify(self.chap_username_in)
        if "chap_password_in" == "type" or (self.chap_password_in is not self.__undef__ and (not (dirty and not self._chap_password_in[1]) or self.is_dirty_list(self.chap_password_in, self._chap_password_in) or belongs_to_parent)):
            dct["chapPasswordIn"] = dictify(self.chap_password_in)
        if "state" == "type" or (self.state is not self.__undef__ and (not (dirty and not self._state[1]))):
            dct["state"] = dictify(self.state)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._iqn = (self._iqn[0], True)
        self._portal = (self._portal[0], True)
        self._port = (self._port[0], True)
        self._chap_username = (self._chap_username[0], True)
        self._chap_password = (self._chap_password[0], True)
        self._chap_username_in = (self._chap_username_in[0], True)
        self._chap_password_in = (self._chap_password_in[0], True)
        self._state = (self._state[0], True)

    def is_dirty(self):
        return any([self._name[1], self._iqn[1], self._portal[1], self._port[1], self._chap_username[1], self._chap_password[1], self._chap_username_in[1], self._chap_password_in[1], self._state[1]])

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
        if not isinstance(other, IscsiTarget):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.iqn == other.iqn and \
               self.portal == other.portal and \
               self.port == other.port and \
               self.chap_username == other.chap_username and \
               self.chap_password == other.chap_password and \
               self.chap_username_in == other.chap_username_in and \
               self.chap_password_in == other.chap_password_in and \
               self.state == other.state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        Object name.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def iqn(self):
        """
        The target's IQN.

        :rtype: ``str``
        """
        return self._iqn[0]

    @iqn.setter
    def iqn(self, value):
        self._iqn = (value, True)

    @property
    def portal(self):
        """
        The target portal's hostname or IP address.

        :rtype: ``str``
        """
        return self._portal[0]

    @portal.setter
    def portal(self, value):
        self._portal = (value, True)

    @property
    def port(self):
        """
        *(default value: 3260)* The target portal's port.

        :rtype: ``int``
        """
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port = (value, True)

    @property
    def chap_username(self):
        """
        CHAP username to be used for iSCSI Target authentication.

        :rtype: ``str``
        """
        return self._chap_username[0]

    @chap_username.setter
    def chap_username(self, value):
        self._chap_username = (value, True)

    @property
    def chap_password(self):
        """
        CHAP password to be used for iSCSI Target authentication.

        :rtype: ``str``
        """
        return self._chap_password[0]

    @chap_password.setter
    def chap_password(self, value):
        self._chap_password = (value, True)

    @property
    def chap_username_in(self):
        """
        Target/Mutual CHAP username (bidirectional authentication).

        :rtype: ``str``
        """
        return self._chap_username_in[0]

    @chap_username_in.setter
    def chap_username_in(self, value):
        self._chap_username_in = (value, True)

    @property
    def chap_password_in(self):
        """
        Target/Mutual CHAP password (bidirectional authentication).

        :rtype: ``str``
        """
        return self._chap_password_in[0]

    @chap_password_in.setter
    def chap_password_in(self, value):
        self._chap_password_in = (value, True)

    @property
    def state(self):
        """
        The state of the iSCSI target connection. *(permitted values:
        NOT_CONNECTED, CONNECTED, IN_USE, ERROR)*

        :rtype: ``str``
        """
        return self._state[0]

    @state.setter
    def state(self, value):
        self._state = (value, True)

