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
#     /delphix-sso.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SsoConfig(TypedObject):
    """
    *(extends* :py:class:`v1_11_11.web.vo.TypedObject` *)* SAML Single Sign-on
    (SSO) Configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SsoConfig", True)
        self._enabled = (self.__undef__, True)
        self._entity_id = (self.__undef__, True)
        self._saml_metadata = (self.__undef__, True)
        self._response_skew_time = (self.__undef__, True)
        self._max_authentication_age = (self.__undef__, True)
        self._cloud_sso = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._entity_id = (data.get("entityId", obj.__undef__), dirty)
        if obj._entity_id[0] is not None and obj._entity_id[0] is not obj.__undef__:
            assert isinstance(obj._entity_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._entity_id[0], type(obj._entity_id[0])))
            common.validate_format(obj._entity_id[0], "None", None, None)
        obj._saml_metadata = (data.get("samlMetadata", obj.__undef__), dirty)
        if obj._saml_metadata[0] is not None and obj._saml_metadata[0] is not obj.__undef__:
            assert isinstance(obj._saml_metadata[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._saml_metadata[0], type(obj._saml_metadata[0])))
            common.validate_format(obj._saml_metadata[0], "xml", None, None)
        obj._response_skew_time = (data.get("responseSkewTime", obj.__undef__), dirty)
        if obj._response_skew_time[0] is not None and obj._response_skew_time[0] is not obj.__undef__:
            assert isinstance(obj._response_skew_time[0], int), ("Expected one of ['integer', 'null'], but got %s of type %s" % (obj._response_skew_time[0], type(obj._response_skew_time[0])))
            common.validate_format(obj._response_skew_time[0], "None", None, None)
        obj._max_authentication_age = (data.get("maxAuthenticationAge", obj.__undef__), dirty)
        if obj._max_authentication_age[0] is not None and obj._max_authentication_age[0] is not obj.__undef__:
            assert isinstance(obj._max_authentication_age[0], int), ("Expected one of ['integer', 'null'], but got %s of type %s" % (obj._max_authentication_age[0], type(obj._max_authentication_age[0])))
            common.validate_format(obj._max_authentication_age[0], "None", None, None)
        obj._cloud_sso = (data.get("cloudSso", obj.__undef__), dirty)
        if obj._cloud_sso[0] is not None and obj._cloud_sso[0] is not obj.__undef__:
            assert isinstance(obj._cloud_sso[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._cloud_sso[0], type(obj._cloud_sso[0])))
            common.validate_format(obj._cloud_sso[0], "None", None, None)
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
        if "enabled" == "type" or (self.enabled is not self.__undef__ and (not (dirty and not self._enabled[1]) or self.is_dirty_list(self.enabled, self._enabled) or belongs_to_parent)):
            dct["enabled"] = dictify(self.enabled)
        if "entity_id" == "type" or (self.entity_id is not self.__undef__ and (not (dirty and not self._entity_id[1]) or self.is_dirty_list(self.entity_id, self._entity_id) or belongs_to_parent)):
            dct["entityId"] = dictify(self.entity_id)
        if "saml_metadata" == "type" or (self.saml_metadata is not self.__undef__ and (not (dirty and not self._saml_metadata[1]) or self.is_dirty_list(self.saml_metadata, self._saml_metadata) or belongs_to_parent)):
            dct["samlMetadata"] = dictify(self.saml_metadata)
        if "response_skew_time" == "type" or (self.response_skew_time is not self.__undef__ and (not (dirty and not self._response_skew_time[1]) or self.is_dirty_list(self.response_skew_time, self._response_skew_time) or belongs_to_parent)):
            dct["responseSkewTime"] = dictify(self.response_skew_time)
        if "max_authentication_age" == "type" or (self.max_authentication_age is not self.__undef__ and (not (dirty and not self._max_authentication_age[1]) or self.is_dirty_list(self.max_authentication_age, self._max_authentication_age) or belongs_to_parent)):
            dct["maxAuthenticationAge"] = dictify(self.max_authentication_age)
        if "cloud_sso" == "type" or (self.cloud_sso is not self.__undef__ and (not (dirty and not self._cloud_sso[1]))):
            dct["cloudSso"] = dictify(self.cloud_sso)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._entity_id = (self._entity_id[0], True)
        self._saml_metadata = (self._saml_metadata[0], True)
        self._response_skew_time = (self._response_skew_time[0], True)
        self._max_authentication_age = (self._max_authentication_age[0], True)
        self._cloud_sso = (self._cloud_sso[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._entity_id[1], self._saml_metadata[1], self._response_skew_time[1], self._max_authentication_age[1], self._cloud_sso[1]])

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
        if not isinstance(other, SsoConfig):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.entity_id == other.entity_id and \
               self.saml_metadata == other.saml_metadata and \
               self.response_skew_time == other.response_skew_time and \
               self.max_authentication_age == other.max_authentication_age and \
               self.cloud_sso == other.cloud_sso

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        Whether SAML single sign-on is enabled.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def entity_id(self):
        """
        Audience Restriction (SP entity ID, Partner's Entity ID) of this engine
        as an SSO service provider.

        :rtype: ``str``
        """
        return self._entity_id[0]

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = (value, True)

    @property
    def saml_metadata(self):
        """
        Metadata for the SAML identity provider.

        :rtype: ``str``
        """
        return self._saml_metadata[0]

    @saml_metadata.setter
    def saml_metadata(self, value):
        self._saml_metadata = (value, True)

    @property
    def response_skew_time(self):
        """
        Maximum time difference allowed between a SAML response and the
        engine's current time, in seconds. If not set, it defaults to 86,400
        seconds (one day).

        :rtype: ``int`` *or* ``null``
        """
        return self._response_skew_time[0]

    @response_skew_time.setter
    def response_skew_time(self, value):
        self._response_skew_time = (value, True)

    @property
    def max_authentication_age(self):
        """
        How far in the past to accept authentications to the identity provider,
        in seconds. If not set, it defaults to 120 seconds.

        :rtype: ``int`` *or* ``null``
        """
        return self._max_authentication_age[0]

    @max_authentication_age.setter
    def max_authentication_age(self, value):
        self._max_authentication_age = (value, True)

    @property
    def cloud_sso(self):
        """
        Whether this system has SSO configured by Delphix Central Management.

        :rtype: ``bool``
        """
        return self._cloud_sso[0]

    @cloud_sso.setter
    def cloud_sso(self, value):
        self._cloud_sso = (value, True)

