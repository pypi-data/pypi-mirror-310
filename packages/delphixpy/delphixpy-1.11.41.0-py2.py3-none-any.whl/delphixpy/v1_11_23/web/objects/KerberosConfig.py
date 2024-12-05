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
#     /delphix-kerberos-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.UserObject import UserObject
from delphixpy.v1_11_23 import factory
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class KerberosConfig(UserObject):
    """
    *(extends* :py:class:`v1_11_23.web.vo.UserObject` *)* Kerberos Client
    Configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("KerberosConfig", True)
        self._realm = (self.__undef__, True)
        self._kdcs = (self.__undef__, True)
        self._keytab = (self.__undef__, True)
        self._principal = (self.__undef__, True)
        self._enabled = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._realm = (data.get("realm", obj.__undef__), dirty)
        if obj._realm[0] is not None and obj._realm[0] is not obj.__undef__:
            assert isinstance(obj._realm[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._realm[0], type(obj._realm[0])))
            common.validate_format(obj._realm[0], "None", None, None)
        obj._kdcs = []
        for item in data.get("kdcs") or []:
            obj._kdcs.append(factory.create_object(item))
            factory.validate_type(obj._kdcs[-1], "KerberosKDC")
        obj._kdcs = (obj._kdcs, dirty)
        obj._keytab = (data.get("keytab", obj.__undef__), dirty)
        if obj._keytab[0] is not None and obj._keytab[0] is not obj.__undef__:
            assert isinstance(obj._keytab[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._keytab[0], type(obj._keytab[0])))
            common.validate_format(obj._keytab[0], "password", None, None)
        obj._principal = (data.get("principal", obj.__undef__), dirty)
        if obj._principal[0] is not None and obj._principal[0] is not obj.__undef__:
            assert isinstance(obj._principal[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._principal[0], type(obj._principal[0])))
            common.validate_format(obj._principal[0], "None", None, None)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
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
        if "realm" == "type" or (self.realm is not self.__undef__ and (not (dirty and not self._realm[1]) or self.is_dirty_list(self.realm, self._realm) or belongs_to_parent)):
            dct["realm"] = dictify(self.realm)
        if "kdcs" == "type" or (self.kdcs is not self.__undef__ and (not (dirty and not self._kdcs[1]) or self.is_dirty_list(self.kdcs, self._kdcs) or belongs_to_parent)):
            dct["kdcs"] = dictify(self.kdcs, prop_is_list_or_vo=True)
        if "keytab" == "type" or (self.keytab is not self.__undef__ and (not (dirty and not self._keytab[1]) or self.is_dirty_list(self.keytab, self._keytab) or belongs_to_parent)):
            dct["keytab"] = dictify(self.keytab)
        if "principal" == "type" or (self.principal is not self.__undef__ and (not (dirty and not self._principal[1]) or self.is_dirty_list(self.principal, self._principal) or belongs_to_parent)):
            dct["principal"] = dictify(self.principal)
        if "enabled" == "type" or (self.enabled is not self.__undef__ and (not (dirty and not self._enabled[1]))):
            dct["enabled"] = dictify(self.enabled)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._realm = (self._realm[0], True)
        self._kdcs = (self._kdcs[0], True)
        self._keytab = (self._keytab[0], True)
        self._principal = (self._principal[0], True)
        self._enabled = (self._enabled[0], True)

    def is_dirty(self):
        return any([self._realm[1], self._kdcs[1], self._keytab[1], self._principal[1], self._enabled[1]])

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
        if not isinstance(other, KerberosConfig):
            return False
        return super().__eq__(other) and \
               self.realm == other.realm and \
               self.kdcs == other.kdcs and \
               self.keytab == other.keytab and \
               self.principal == other.principal and \
               self.enabled == other.enabled

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def realm(self):
        """
        Kerberos Realm name.

        :rtype: ``str``
        """
        return self._realm[0]

    @realm.setter
    def realm(self, value):
        self._realm = (value, True)

    @property
    def kdcs(self):
        """
        One of more KDC servers.

        :rtype: ``list`` of :py:class:`v1_11_23.web.vo.KerberosKDC`
        """
        return self._kdcs[0]

    @kdcs.setter
    def kdcs(self, value):
        self._kdcs = (value, True)

    @property
    def keytab(self):
        """
        Kerberos keytab file data in base64 encoding.

        :rtype: ``str``
        """
        return self._keytab[0]

    @keytab.setter
    def keytab(self, value):
        self._keytab = (value, True)

    @property
    def principal(self):
        """
        Kerberos principal name.

        :rtype: ``str``
        """
        return self._principal[0]

    @principal.setter
    def principal(self, value):
        self._principal = (value, True)

    @property
    def enabled(self):
        """
        Indicates whether kerberos has been configured or not.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

