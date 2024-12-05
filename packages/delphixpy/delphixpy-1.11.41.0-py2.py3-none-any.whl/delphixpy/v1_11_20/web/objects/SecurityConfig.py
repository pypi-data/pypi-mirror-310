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
#     /delphix-security-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SecurityConfig(TypedObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.TypedObject` *)* System wide security
    configuration.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SecurityConfig", True)
        self._banner = (self.__undef__, True)
        self._is_cors_enabled = (self.__undef__, True)
        self._allowed_cors_origins = (self.__undef__, True)
        self._enable_cors_supports_credentials = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._banner = (data.get("banner", obj.__undef__), dirty)
        if obj._banner[0] is not None and obj._banner[0] is not obj.__undef__:
            assert isinstance(obj._banner[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._banner[0], type(obj._banner[0])))
            common.validate_format(obj._banner[0], "None", None, None)
        obj._is_cors_enabled = (data.get("isCORSEnabled", obj.__undef__), dirty)
        if obj._is_cors_enabled[0] is not None and obj._is_cors_enabled[0] is not obj.__undef__:
            assert isinstance(obj._is_cors_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._is_cors_enabled[0], type(obj._is_cors_enabled[0])))
            common.validate_format(obj._is_cors_enabled[0], "None", None, None)
        obj._allowed_cors_origins = (data.get("allowedCORSOrigins", obj.__undef__), dirty)
        if obj._allowed_cors_origins[0] is not None and obj._allowed_cors_origins[0] is not obj.__undef__:
            assert isinstance(obj._allowed_cors_origins[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._allowed_cors_origins[0], type(obj._allowed_cors_origins[0])))
            common.validate_format(obj._allowed_cors_origins[0], "None", None, None)
        obj._enable_cors_supports_credentials = (data.get("enableCORSSupportsCredentials", obj.__undef__), dirty)
        if obj._enable_cors_supports_credentials[0] is not None and obj._enable_cors_supports_credentials[0] is not obj.__undef__:
            assert isinstance(obj._enable_cors_supports_credentials[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enable_cors_supports_credentials[0], type(obj._enable_cors_supports_credentials[0])))
            common.validate_format(obj._enable_cors_supports_credentials[0], "None", None, None)
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
        if "banner" == "type" or (self.banner is not self.__undef__ and (not (dirty and not self._banner[1]) or self.is_dirty_list(self.banner, self._banner) or belongs_to_parent)):
            dct["banner"] = dictify(self.banner)
        if "is_cors_enabled" == "type" or (self.is_cors_enabled is not self.__undef__ and (not (dirty and not self._is_cors_enabled[1]) or self.is_dirty_list(self.is_cors_enabled, self._is_cors_enabled) or belongs_to_parent)):
            dct["isCORSEnabled"] = dictify(self.is_cors_enabled)
        if "allowed_cors_origins" == "type" or (self.allowed_cors_origins is not self.__undef__ and (not (dirty and not self._allowed_cors_origins[1]) or self.is_dirty_list(self.allowed_cors_origins, self._allowed_cors_origins) or belongs_to_parent)):
            dct["allowedCORSOrigins"] = dictify(self.allowed_cors_origins)
        if "enable_cors_supports_credentials" == "type" or (self.enable_cors_supports_credentials is not self.__undef__ and (not (dirty and not self._enable_cors_supports_credentials[1]) or self.is_dirty_list(self.enable_cors_supports_credentials, self._enable_cors_supports_credentials) or belongs_to_parent)):
            dct["enableCORSSupportsCredentials"] = dictify(self.enable_cors_supports_credentials)
        elif belongs_to_parent and self.enable_cors_supports_credentials is self.__undef__:
            dct["enableCORSSupportsCredentials"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._banner = (self._banner[0], True)
        self._is_cors_enabled = (self._is_cors_enabled[0], True)
        self._allowed_cors_origins = (self._allowed_cors_origins[0], True)
        self._enable_cors_supports_credentials = (self._enable_cors_supports_credentials[0], True)

    def is_dirty(self):
        return any([self._banner[1], self._is_cors_enabled[1], self._allowed_cors_origins[1], self._enable_cors_supports_credentials[1]])

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
        if not isinstance(other, SecurityConfig):
            return False
        return super().__eq__(other) and \
               self.banner == other.banner and \
               self.is_cors_enabled == other.is_cors_enabled and \
               self.allowed_cors_origins == other.allowed_cors_origins and \
               self.enable_cors_supports_credentials == other.enable_cors_supports_credentials

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def banner(self):
        """
        Banner displayed prior to login.

        :rtype: ``str`` *or* ``null``
        """
        return self._banner[0]

    @banner.setter
    def banner(self, value):
        self._banner = (value, True)

    @property
    def is_cors_enabled(self):
        """
        Whether or not CORS is enabled. Changing this value requires a stack
        restart for it to take effect.

        :rtype: ``bool``
        """
        return self._is_cors_enabled[0]

    @is_cors_enabled.setter
    def is_cors_enabled(self, value):
        self._is_cors_enabled = (value, True)

    @property
    def allowed_cors_origins(self):
        """
        Allowed origin domains for CORS. Should be a comma separated list. Use
        * for all domains. Defaults to none. Changing this value requires a
        stack restart for it to take effect.

        :rtype: ``str``
        """
        return self._allowed_cors_origins[0]

    @allowed_cors_origins.setter
    def allowed_cors_origins(self, value):
        self._allowed_cors_origins = (value, True)

    @property
    def enable_cors_supports_credentials(self):
        """
        Whether or not the resource supports user credentials. This flag is
        exposed as part of the Access-Control-Allow-Credentials header in a
        pre-flight response. It helps browsers determine whether or not an
        actual request can be made using credentials. Changing this value
        requires a stack restart for it to take effect.

        :rtype: ``bool``
        """
        return self._enable_cors_supports_credentials[0]

    @enable_cors_supports_credentials.setter
    def enable_cors_supports_credentials(self, value):
        self._enable_cors_supports_credentials = (value, True)

