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
#     /delphix-oauth2-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_22.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_22 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OAuth2Config(TypedObject):
    """
    *(extends* :py:class:`v1_11_22.web.vo.TypedObject` *)* OAuth2
    Configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OAuth2Config", True)
        self._enabled = (self.__undef__, True)
        self._issuer_uri = (self.__undef__, True)
        self._jwk_set_uri = (self.__undef__, True)
        self._audience = (self.__undef__, True)
        self._user_id_claim = (self.__undef__, True)
        self._user_matching_field_type = (self.__undef__, True)
        self._token_skew_time = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._issuer_uri = (data.get("issuerURI", obj.__undef__), dirty)
        if obj._issuer_uri[0] is not None and obj._issuer_uri[0] is not obj.__undef__:
            assert isinstance(obj._issuer_uri[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._issuer_uri[0], type(obj._issuer_uri[0])))
            common.validate_format(obj._issuer_uri[0], "None", None, None)
        obj._jwk_set_uri = (data.get("jwkSetURI", obj.__undef__), dirty)
        if obj._jwk_set_uri[0] is not None and obj._jwk_set_uri[0] is not obj.__undef__:
            assert isinstance(obj._jwk_set_uri[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._jwk_set_uri[0], type(obj._jwk_set_uri[0])))
            common.validate_format(obj._jwk_set_uri[0], "None", None, None)
        obj._audience = (data.get("audience", obj.__undef__), dirty)
        if obj._audience[0] is not None and obj._audience[0] is not obj.__undef__:
            assert isinstance(obj._audience[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._audience[0], type(obj._audience[0])))
            common.validate_format(obj._audience[0], "None", None, None)
        obj._user_id_claim = (data.get("userIdClaim", obj.__undef__), dirty)
        if obj._user_id_claim[0] is not None and obj._user_id_claim[0] is not obj.__undef__:
            assert isinstance(obj._user_id_claim[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user_id_claim[0], type(obj._user_id_claim[0])))
            common.validate_format(obj._user_id_claim[0], "None", None, None)
        obj._user_matching_field_type = (data.get("userMatchingFieldType", obj.__undef__), dirty)
        if obj._user_matching_field_type[0] is not None and obj._user_matching_field_type[0] is not obj.__undef__:
            assert isinstance(obj._user_matching_field_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user_matching_field_type[0], type(obj._user_matching_field_type[0])))
            assert obj._user_matching_field_type[0] in ['NAME', 'EMAIL_ADDRESS', 'PRINCIPAL'], "Expected enum ['NAME', 'EMAIL_ADDRESS', 'PRINCIPAL'] but got %s" % obj._user_matching_field_type[0]
            common.validate_format(obj._user_matching_field_type[0], "None", None, None)
        obj._token_skew_time = (data.get("tokenSkewTime", obj.__undef__), dirty)
        if obj._token_skew_time[0] is not None and obj._token_skew_time[0] is not obj.__undef__:
            assert isinstance(obj._token_skew_time[0], int), ("Expected one of ['integer', 'null'], but got %s of type %s" % (obj._token_skew_time[0], type(obj._token_skew_time[0])))
            common.validate_format(obj._token_skew_time[0], "None", None, None)
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
        if "issuer_uri" == "type" or (self.issuer_uri is not self.__undef__ and (not (dirty and not self._issuer_uri[1]) or self.is_dirty_list(self.issuer_uri, self._issuer_uri) or belongs_to_parent)):
            dct["issuerURI"] = dictify(self.issuer_uri)
        if "jwk_set_uri" == "type" or (self.jwk_set_uri is not self.__undef__ and (not (dirty and not self._jwk_set_uri[1]) or self.is_dirty_list(self.jwk_set_uri, self._jwk_set_uri) or belongs_to_parent)):
            dct["jwkSetURI"] = dictify(self.jwk_set_uri)
        if "audience" == "type" or (self.audience is not self.__undef__ and (not (dirty and not self._audience[1]) or self.is_dirty_list(self.audience, self._audience) or belongs_to_parent)):
            dct["audience"] = dictify(self.audience)
        if "user_id_claim" == "type" or (self.user_id_claim is not self.__undef__ and (not (dirty and not self._user_id_claim[1]) or self.is_dirty_list(self.user_id_claim, self._user_id_claim) or belongs_to_parent)):
            dct["userIdClaim"] = dictify(self.user_id_claim)
        if "user_matching_field_type" == "type" or (self.user_matching_field_type is not self.__undef__ and (not (dirty and not self._user_matching_field_type[1]) or self.is_dirty_list(self.user_matching_field_type, self._user_matching_field_type) or belongs_to_parent)):
            dct["userMatchingFieldType"] = dictify(self.user_matching_field_type)
        if "token_skew_time" == "type" or (self.token_skew_time is not self.__undef__ and (not (dirty and not self._token_skew_time[1]) or self.is_dirty_list(self.token_skew_time, self._token_skew_time) or belongs_to_parent)):
            dct["tokenSkewTime"] = dictify(self.token_skew_time)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._issuer_uri = (self._issuer_uri[0], True)
        self._jwk_set_uri = (self._jwk_set_uri[0], True)
        self._audience = (self._audience[0], True)
        self._user_id_claim = (self._user_id_claim[0], True)
        self._user_matching_field_type = (self._user_matching_field_type[0], True)
        self._token_skew_time = (self._token_skew_time[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._issuer_uri[1], self._jwk_set_uri[1], self._audience[1], self._user_id_claim[1], self._user_matching_field_type[1], self._token_skew_time[1]])

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
        if not isinstance(other, OAuth2Config):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.issuer_uri == other.issuer_uri and \
               self.jwk_set_uri == other.jwk_set_uri and \
               self.audience == other.audience and \
               self.user_id_claim == other.user_id_claim and \
               self.user_matching_field_type == other.user_matching_field_type and \
               self.token_skew_time == other.token_skew_time

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        Whether OAuth2 is enabled.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def issuer_uri(self):
        """
        URI of the OAuth Authorization issuer.

        :rtype: ``str``
        """
        return self._issuer_uri[0]

    @issuer_uri.setter
    def issuer_uri(self, value):
        self._issuer_uri = (value, True)

    @property
    def jwk_set_uri(self):
        """
        URI of the JWK key set.

        :rtype: ``str`` *or* ``null``
        """
        return self._jwk_set_uri[0]

    @jwk_set_uri.setter
    def jwk_set_uri(self, value):
        self._jwk_set_uri = (value, True)

    @property
    def audience(self):
        """
        The audience claim string issued by the Authorization Server for
        Delphix Engine access.

        :rtype: ``str``
        """
        return self._audience[0]

    @audience.setter
    def audience(self, value):
        self._audience = (value, True)

    @property
    def user_id_claim(self):
        """
        The claim in a token that should be used to associate a JWT with a
        Delphix Engine user.

        :rtype: ``str``
        """
        return self._user_id_claim[0]

    @user_id_claim.setter
    def user_id_claim(self, value):
        self._user_id_claim = (value, True)

    @property
    def user_matching_field_type(self):
        """
        The property associated with a Delphix user that will be matched with
        the user id claim. *(permitted values: NAME, EMAIL_ADDRESS, PRINCIPAL)*

        :rtype: ``str``
        """
        return self._user_matching_field_type[0]

    @user_matching_field_type.setter
    def user_matching_field_type(self, value):
        self._user_matching_field_type = (value, True)

    @property
    def token_skew_time(self):
        """
        Allow for clock drift between systems by extending the start and end of
        a token's validity window by this time (in seconds).If not set, the
        default skew is 60 seconds.

        :rtype: ``int`` *or* ``null``
        """
        return self._token_skew_time[0]

    @token_skew_time.setter
    def token_skew_time(self, value):
        self._token_skew_time = (value, True)

