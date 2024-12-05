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
#     /delphix-about.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_38 import factory
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PublicSystemInfo(TypedObject):
    """
    *(extends* :py:class:`v1_11_38.web.vo.TypedObject` *)* Retrieve static
    system-wide properties.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PublicSystemInfo", True)
        self._product_type = (self.__undef__, True)
        self._engine_type = (self.__undef__, True)
        self._sso_enabled = (self.__undef__, True)
        self._vendor_name = (self.__undef__, True)
        self._vendor_address = (self.__undef__, True)
        self._vendor_phone_number = (self.__undef__, True)
        self._vendor_email = (self.__undef__, True)
        self._vendor_url = (self.__undef__, True)
        self._product_name = (self.__undef__, True)
        self._engine_qualifier = (self.__undef__, True)
        self._support_contacts = (self.__undef__, True)
        self._support_url = (self.__undef__, True)
        self._build_title = (self.__undef__, True)
        self._build_timestamp = (self.__undef__, True)
        self._build_version = (self.__undef__, True)
        self._configured = (self.__undef__, True)
        self._enabled_features = (self.__undef__, True)
        self._toggleable_features = (self.__undef__, True)
        self._api_version = (self.__undef__, True)
        self._banner = (self.__undef__, True)
        self._locales = (self.__undef__, True)
        self._current_locale = (self.__undef__, True)
        self._kernel_name = (self.__undef__, True)
        self._theme = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._product_type = (data.get("productType", obj.__undef__), dirty)
        if obj._product_type[0] is not None and obj._product_type[0] is not obj.__undef__:
            assert isinstance(obj._product_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._product_type[0], type(obj._product_type[0])))
            common.validate_format(obj._product_type[0], "None", None, None)
        obj._engine_type = (data.get("engineType", obj.__undef__), dirty)
        if obj._engine_type[0] is not None and obj._engine_type[0] is not obj.__undef__:
            assert isinstance(obj._engine_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine_type[0], type(obj._engine_type[0])))
            assert obj._engine_type[0] in ['VIRTUALIZATION', 'MASKING', 'BOTH', 'UNSET', 'DCT'], "Expected enum ['VIRTUALIZATION', 'MASKING', 'BOTH', 'UNSET', 'DCT'] but got %s" % obj._engine_type[0]
            common.validate_format(obj._engine_type[0], "None", None, None)
        obj._sso_enabled = (data.get("ssoEnabled", obj.__undef__), dirty)
        if obj._sso_enabled[0] is not None and obj._sso_enabled[0] is not obj.__undef__:
            assert isinstance(obj._sso_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._sso_enabled[0], type(obj._sso_enabled[0])))
            common.validate_format(obj._sso_enabled[0], "None", None, None)
        obj._vendor_name = (data.get("vendorName", obj.__undef__), dirty)
        if obj._vendor_name[0] is not None and obj._vendor_name[0] is not obj.__undef__:
            assert isinstance(obj._vendor_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._vendor_name[0], type(obj._vendor_name[0])))
            common.validate_format(obj._vendor_name[0], "None", None, None)
        obj._vendor_address = []
        for item in data.get("vendorAddress") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._vendor_address.append(item)
        obj._vendor_address = (obj._vendor_address, dirty)
        obj._vendor_phone_number = (data.get("vendorPhoneNumber", obj.__undef__), dirty)
        if obj._vendor_phone_number[0] is not None and obj._vendor_phone_number[0] is not obj.__undef__:
            assert isinstance(obj._vendor_phone_number[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._vendor_phone_number[0], type(obj._vendor_phone_number[0])))
            common.validate_format(obj._vendor_phone_number[0], "None", None, None)
        obj._vendor_email = (data.get("vendorEmail", obj.__undef__), dirty)
        if obj._vendor_email[0] is not None and obj._vendor_email[0] is not obj.__undef__:
            assert isinstance(obj._vendor_email[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._vendor_email[0], type(obj._vendor_email[0])))
            common.validate_format(obj._vendor_email[0], "email", None, None)
        obj._vendor_url = (data.get("vendorURL", obj.__undef__), dirty)
        if obj._vendor_url[0] is not None and obj._vendor_url[0] is not obj.__undef__:
            assert isinstance(obj._vendor_url[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._vendor_url[0], type(obj._vendor_url[0])))
            common.validate_format(obj._vendor_url[0], "None", None, None)
        obj._product_name = (data.get("productName", obj.__undef__), dirty)
        if obj._product_name[0] is not None and obj._product_name[0] is not obj.__undef__:
            assert isinstance(obj._product_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._product_name[0], type(obj._product_name[0])))
            common.validate_format(obj._product_name[0], "None", None, None)
        obj._engine_qualifier = (data.get("engineQualifier", obj.__undef__), dirty)
        if obj._engine_qualifier[0] is not None and obj._engine_qualifier[0] is not obj.__undef__:
            assert isinstance(obj._engine_qualifier[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._engine_qualifier[0], type(obj._engine_qualifier[0])))
            common.validate_format(obj._engine_qualifier[0], "None", None, None)
        obj._support_contacts = []
        for item in data.get("supportContacts") or []:
            obj._support_contacts.append(factory.create_object(item))
            factory.validate_type(obj._support_contacts[-1], "SupportContact")
        obj._support_contacts = (obj._support_contacts, dirty)
        obj._support_url = (data.get("supportURL", obj.__undef__), dirty)
        if obj._support_url[0] is not None and obj._support_url[0] is not obj.__undef__:
            assert isinstance(obj._support_url[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._support_url[0], type(obj._support_url[0])))
            common.validate_format(obj._support_url[0], "None", None, None)
        obj._build_title = (data.get("buildTitle", obj.__undef__), dirty)
        if obj._build_title[0] is not None and obj._build_title[0] is not obj.__undef__:
            assert isinstance(obj._build_title[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._build_title[0], type(obj._build_title[0])))
            common.validate_format(obj._build_title[0], "None", None, None)
        obj._build_timestamp = (data.get("buildTimestamp", obj.__undef__), dirty)
        if obj._build_timestamp[0] is not None and obj._build_timestamp[0] is not obj.__undef__:
            assert isinstance(obj._build_timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._build_timestamp[0], type(obj._build_timestamp[0])))
            common.validate_format(obj._build_timestamp[0], "date", None, None)
        if "buildVersion" in data and data["buildVersion"] is not None:
            obj._build_version = (factory.create_object(data["buildVersion"], "VersionInfo"), dirty)
            factory.validate_type(obj._build_version[0], "VersionInfo")
        else:
            obj._build_version = (obj.__undef__, dirty)
        obj._configured = (data.get("configured", obj.__undef__), dirty)
        if obj._configured[0] is not None and obj._configured[0] is not obj.__undef__:
            assert isinstance(obj._configured[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._configured[0], type(obj._configured[0])))
            common.validate_format(obj._configured[0], "None", None, None)
        obj._enabled_features = []
        for item in data.get("enabledFeatures") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._enabled_features.append(item)
        obj._enabled_features = (obj._enabled_features, dirty)
        obj._toggleable_features = []
        for item in data.get("toggleableFeatures") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._toggleable_features.append(item)
        obj._toggleable_features = (obj._toggleable_features, dirty)
        if "apiVersion" in data and data["apiVersion"] is not None:
            obj._api_version = (factory.create_object(data["apiVersion"], "APIVersion"), dirty)
            factory.validate_type(obj._api_version[0], "APIVersion")
        else:
            obj._api_version = (obj.__undef__, dirty)
        obj._banner = (data.get("banner", obj.__undef__), dirty)
        if obj._banner[0] is not None and obj._banner[0] is not obj.__undef__:
            assert isinstance(obj._banner[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._banner[0], type(obj._banner[0])))
            common.validate_format(obj._banner[0], "None", None, None)
        obj._locales = []
        for item in data.get("locales") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "locale", None, None)
            obj._locales.append(item)
        obj._locales = (obj._locales, dirty)
        obj._current_locale = (data.get("currentLocale", obj.__undef__), dirty)
        if obj._current_locale[0] is not None and obj._current_locale[0] is not obj.__undef__:
            assert isinstance(obj._current_locale[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._current_locale[0], type(obj._current_locale[0])))
            common.validate_format(obj._current_locale[0], "locale", None, None)
        obj._kernel_name = (data.get("kernelName", obj.__undef__), dirty)
        if obj._kernel_name[0] is not None and obj._kernel_name[0] is not obj.__undef__:
            assert isinstance(obj._kernel_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._kernel_name[0], type(obj._kernel_name[0])))
            common.validate_format(obj._kernel_name[0], "None", None, None)
        if "theme" in data and data["theme"] is not None:
            obj._theme = (data["theme"], dirty)
        else:
            obj._theme = (obj.__undef__, dirty)
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
        if "product_type" == "type" or (self.product_type is not self.__undef__ and (not (dirty and not self._product_type[1]))):
            dct["productType"] = dictify(self.product_type)
        if "engine_type" == "type" or (self.engine_type is not self.__undef__ and (not (dirty and not self._engine_type[1]) or self.is_dirty_list(self.engine_type, self._engine_type) or belongs_to_parent)):
            dct["engineType"] = dictify(self.engine_type)
        elif belongs_to_parent and self.engine_type is self.__undef__:
            dct["engineType"] = "UNSET"
        if "sso_enabled" == "type" or (self.sso_enabled is not self.__undef__ and (not (dirty and not self._sso_enabled[1]))):
            dct["ssoEnabled"] = dictify(self.sso_enabled)
        if "vendor_name" == "type" or (self.vendor_name is not self.__undef__ and (not (dirty and not self._vendor_name[1]) or self.is_dirty_list(self.vendor_name, self._vendor_name) or belongs_to_parent)):
            dct["vendorName"] = dictify(self.vendor_name)
        if "vendor_address" == "type" or (self.vendor_address is not self.__undef__ and (not (dirty and not self._vendor_address[1]) or self.is_dirty_list(self.vendor_address, self._vendor_address) or belongs_to_parent)):
            dct["vendorAddress"] = dictify(self.vendor_address, prop_is_list_or_vo=True)
        if "vendor_phone_number" == "type" or (self.vendor_phone_number is not self.__undef__ and (not (dirty and not self._vendor_phone_number[1]) or self.is_dirty_list(self.vendor_phone_number, self._vendor_phone_number) or belongs_to_parent)):
            dct["vendorPhoneNumber"] = dictify(self.vendor_phone_number)
        if "vendor_email" == "type" or (self.vendor_email is not self.__undef__ and (not (dirty and not self._vendor_email[1]) or self.is_dirty_list(self.vendor_email, self._vendor_email) or belongs_to_parent)):
            dct["vendorEmail"] = dictify(self.vendor_email)
        if "vendor_url" == "type" or (self.vendor_url is not self.__undef__ and (not (dirty and not self._vendor_url[1]) or self.is_dirty_list(self.vendor_url, self._vendor_url) or belongs_to_parent)):
            dct["vendorURL"] = dictify(self.vendor_url)
        if "product_name" == "type" or (self.product_name is not self.__undef__ and (not (dirty and not self._product_name[1]))):
            dct["productName"] = dictify(self.product_name)
        if "engine_qualifier" == "type" or (self.engine_qualifier is not self.__undef__ and (not (dirty and not self._engine_qualifier[1]) or self.is_dirty_list(self.engine_qualifier, self._engine_qualifier) or belongs_to_parent)):
            dct["engineQualifier"] = dictify(self.engine_qualifier)
        if "support_contacts" == "type" or (self.support_contacts is not self.__undef__ and (not (dirty and not self._support_contacts[1]) or self.is_dirty_list(self.support_contacts, self._support_contacts) or belongs_to_parent)):
            dct["supportContacts"] = dictify(self.support_contacts, prop_is_list_or_vo=True)
        if "support_url" == "type" or (self.support_url is not self.__undef__ and (not (dirty and not self._support_url[1]) or self.is_dirty_list(self.support_url, self._support_url) or belongs_to_parent)):
            dct["supportURL"] = dictify(self.support_url)
        if "build_title" == "type" or (self.build_title is not self.__undef__ and (not (dirty and not self._build_title[1]))):
            dct["buildTitle"] = dictify(self.build_title)
        if "build_timestamp" == "type" or (self.build_timestamp is not self.__undef__ and (not (dirty and not self._build_timestamp[1]))):
            dct["buildTimestamp"] = dictify(self.build_timestamp)
        if "build_version" == "type" or (self.build_version is not self.__undef__ and (not (dirty and not self._build_version[1]))):
            dct["buildVersion"] = dictify(self.build_version)
        if "configured" == "type" or (self.configured is not self.__undef__ and (not (dirty and not self._configured[1]))):
            dct["configured"] = dictify(self.configured)
        if "enabled_features" == "type" or (self.enabled_features is not self.__undef__ and (not (dirty and not self._enabled_features[1]))):
            dct["enabledFeatures"] = dictify(self.enabled_features)
        if "toggleable_features" == "type" or (self.toggleable_features is not self.__undef__ and (not (dirty and not self._toggleable_features[1]))):
            dct["toggleableFeatures"] = dictify(self.toggleable_features)
        if "api_version" == "type" or (self.api_version is not self.__undef__ and (not (dirty and not self._api_version[1]))):
            dct["apiVersion"] = dictify(self.api_version)
        if "banner" == "type" or (self.banner is not self.__undef__ and (not (dirty and not self._banner[1]))):
            dct["banner"] = dictify(self.banner)
        if "locales" == "type" or (self.locales is not self.__undef__ and (not (dirty and not self._locales[1]))):
            dct["locales"] = dictify(self.locales)
        if "current_locale" == "type" or (self.current_locale is not self.__undef__ and (not (dirty and not self._current_locale[1]))):
            dct["currentLocale"] = dictify(self.current_locale)
        if "kernel_name" == "type" or (self.kernel_name is not self.__undef__ and (not (dirty and not self._kernel_name[1]))):
            dct["kernelName"] = dictify(self.kernel_name)
        if "theme" == "type" or (self.theme is not self.__undef__ and (not (dirty and not self._theme[1]))):
            dct["theme"] = dictify(self.theme)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._product_type = (self._product_type[0], True)
        self._engine_type = (self._engine_type[0], True)
        self._sso_enabled = (self._sso_enabled[0], True)
        self._vendor_name = (self._vendor_name[0], True)
        self._vendor_address = (self._vendor_address[0], True)
        self._vendor_phone_number = (self._vendor_phone_number[0], True)
        self._vendor_email = (self._vendor_email[0], True)
        self._vendor_url = (self._vendor_url[0], True)
        self._product_name = (self._product_name[0], True)
        self._engine_qualifier = (self._engine_qualifier[0], True)
        self._support_contacts = (self._support_contacts[0], True)
        self._support_url = (self._support_url[0], True)
        self._build_title = (self._build_title[0], True)
        self._build_timestamp = (self._build_timestamp[0], True)
        self._build_version = (self._build_version[0], True)
        self._configured = (self._configured[0], True)
        self._enabled_features = (self._enabled_features[0], True)
        self._toggleable_features = (self._toggleable_features[0], True)
        self._api_version = (self._api_version[0], True)
        self._banner = (self._banner[0], True)
        self._locales = (self._locales[0], True)
        self._current_locale = (self._current_locale[0], True)
        self._kernel_name = (self._kernel_name[0], True)
        self._theme = (self._theme[0], True)

    def is_dirty(self):
        return any([self._product_type[1], self._engine_type[1], self._sso_enabled[1], self._vendor_name[1], self._vendor_address[1], self._vendor_phone_number[1], self._vendor_email[1], self._vendor_url[1], self._product_name[1], self._engine_qualifier[1], self._support_contacts[1], self._support_url[1], self._build_title[1], self._build_timestamp[1], self._build_version[1], self._configured[1], self._enabled_features[1], self._toggleable_features[1], self._api_version[1], self._banner[1], self._locales[1], self._current_locale[1], self._kernel_name[1], self._theme[1]])

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
        if not isinstance(other, PublicSystemInfo):
            return False
        return super().__eq__(other) and \
               self.product_type == other.product_type and \
               self.engine_type == other.engine_type and \
               self.sso_enabled == other.sso_enabled and \
               self.vendor_name == other.vendor_name and \
               self.vendor_address == other.vendor_address and \
               self.vendor_phone_number == other.vendor_phone_number and \
               self.vendor_email == other.vendor_email and \
               self.vendor_url == other.vendor_url and \
               self.product_name == other.product_name and \
               self.engine_qualifier == other.engine_qualifier and \
               self.support_contacts == other.support_contacts and \
               self.support_url == other.support_url and \
               self.build_title == other.build_title and \
               self.build_timestamp == other.build_timestamp and \
               self.build_version == other.build_version and \
               self.configured == other.configured and \
               self.enabled_features == other.enabled_features and \
               self.toggleable_features == other.toggleable_features and \
               self.api_version == other.api_version and \
               self.banner == other.banner and \
               self.locales == other.locales and \
               self.current_locale == other.current_locale and \
               self.kernel_name == other.kernel_name and \
               self.theme == other.theme

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def product_type(self):
        """
        Product type.

        :rtype: ``str``
        """
        return self._product_type[0]

    @product_type.setter
    def product_type(self, value):
        self._product_type = (value, True)

    @property
    def engine_type(self):
        """
        *(default value: UNSET)* Engine type, could be Masking, Virtualization,
        DCT... *(permitted values: VIRTUALIZATION, MASKING, BOTH, UNSET, DCT)*

        :rtype: ``str``
        """
        return self._engine_type[0]

    @engine_type.setter
    def engine_type(self, value):
        self._engine_type = (value, True)

    @property
    def sso_enabled(self):
        """
        Indicates whether SSO is enabled for this engine.

        :rtype: ``bool``
        """
        return self._sso_enabled[0]

    @sso_enabled.setter
    def sso_enabled(self, value):
        self._sso_enabled = (value, True)

    @property
    def vendor_name(self):
        """
        Vendor name, for use in messages like 'Please contact <vendorName>
        customer support'.

        :rtype: ``str``
        """
        return self._vendor_name[0]

    @vendor_name.setter
    def vendor_name(self, value):
        self._vendor_name = (value, True)

    @property
    def vendor_address(self):
        """
        Address of vendor headquarters. Free form collection of strings to
        accomodate any region.

        :rtype: ``list`` of ``str``
        """
        return self._vendor_address[0]

    @vendor_address.setter
    def vendor_address(self, value):
        self._vendor_address = (value, True)

    @property
    def vendor_phone_number(self):
        """
        Corporate headquarters telephone number.

        :rtype: ``str``
        """
        return self._vendor_phone_number[0]

    @vendor_phone_number.setter
    def vendor_phone_number(self, value):
        self._vendor_phone_number = (value, True)

    @property
    def vendor_email(self):
        """
        Corporate headquarters email address.

        :rtype: ``str``
        """
        return self._vendor_email[0]

    @vendor_email.setter
    def vendor_email(self, value):
        self._vendor_email = (value, True)

    @property
    def vendor_url(self):
        """
        Corporate home page.

        :rtype: ``str``
        """
        return self._vendor_url[0]

    @vendor_url.setter
    def vendor_url(self, value):
        self._vendor_url = (value, True)

    @property
    def product_name(self):
        """
        Name of the product that the system is running.

        :rtype: ``str``
        """
        return self._product_name[0]

    @product_name.setter
    def product_name(self, value):
        self._product_name = (value, True)

    @property
    def engine_qualifier(self):
        """
        Qualifier for referencing instances of (e.g. 'Delphix') engines in
        messages like 'The <engineQualifier> Engine failed to ...'.

        :rtype: ``str``
        """
        return self._engine_qualifier[0]

    @engine_qualifier.setter
    def engine_qualifier(self, value):
        self._engine_qualifier = (value, True)

    @property
    def support_contacts(self):
        """
        Technical support phone numbers.

        :rtype: ``list`` of :py:class:`v1_11_38.web.vo.SupportContact`
        """
        return self._support_contacts[0]

    @support_contacts.setter
    def support_contacts(self, value):
        self._support_contacts = (value, True)

    @property
    def support_url(self):
        """
        Technical Support URL.

        :rtype: ``str``
        """
        return self._support_url[0]

    @support_url.setter
    def support_url(self, value):
        self._support_url = (value, True)

    @property
    def build_title(self):
        """
        Description of the current system software.

        :rtype: ``str``
        """
        return self._build_title[0]

    @build_title.setter
    def build_title(self, value):
        self._build_title = (value, True)

    @property
    def build_timestamp(self):
        """
        Time at which the current system software was built.

        :rtype: ``str``
        """
        return self._build_timestamp[0]

    @build_timestamp.setter
    def build_timestamp(self, value):
        self._build_timestamp = (value, True)

    @property
    def build_version(self):
        """
        Delphix version of the current system software.

        :rtype: :py:class:`v1_11_38.web.vo.VersionInfo`
        """
        return self._build_version[0]

    @build_version.setter
    def build_version(self, value):
        self._build_version = (value, True)

    @property
    def configured(self):
        """
        Indicates whether the server has gone through initial setup or not.

        :rtype: ``bool``
        """
        return self._configured[0]

    @configured.setter
    def configured(self, value):
        self._configured = (value, True)

    @property
    def enabled_features(self):
        """
        The list of enabled features on this Delphix Engine.

        :rtype: ``list`` of ``str``
        """
        return self._enabled_features[0]

    @enabled_features.setter
    def enabled_features(self, value):
        self._enabled_features = (value, True)

    @property
    def toggleable_features(self):
        """
        The list of toggleable features on this Delphix Engine.

        :rtype: ``list`` of ``str``
        """
        return self._toggleable_features[0]

    @toggleable_features.setter
    def toggleable_features(self, value):
        self._toggleable_features = (value, True)

    @property
    def api_version(self):
        """
        Maximum supported API version of the current system software.

        :rtype: :py:class:`v1_11_38.web.vo.APIVersion`
        """
        return self._api_version[0]

    @api_version.setter
    def api_version(self, value):
        self._api_version = (value, True)

    @property
    def banner(self):
        """
        Security banner to display prior to login.

        :rtype: ``str``
        """
        return self._banner[0]

    @banner.setter
    def banner(self, value):
        self._banner = (value, True)

    @property
    def locales(self):
        """
        List of available locales.

        :rtype: ``list`` of ``str``
        """
        return self._locales[0]

    @locales.setter
    def locales(self, value):
        self._locales = (value, True)

    @property
    def current_locale(self):
        """
        The current system locale.

        :rtype: ``str``
        """
        return self._current_locale[0]

    @current_locale.setter
    def current_locale(self, value):
        self._current_locale = (value, True)

    @property
    def kernel_name(self):
        """
        The operating system kernel name.

        :rtype: ``str``
        """
        return self._kernel_name[0]

    @kernel_name.setter
    def kernel_name(self, value):
        self._kernel_name = (value, True)

    @property
    def theme(self):
        """
        Color values of the corporate custom UI theme.

        :rtype: :py:class:`v1_11_38.web.vo.SchemaDraftV4`
        """
        return self._theme[0]

    @theme.setter
    def theme(self, value):
        self._theme = (value, True)

