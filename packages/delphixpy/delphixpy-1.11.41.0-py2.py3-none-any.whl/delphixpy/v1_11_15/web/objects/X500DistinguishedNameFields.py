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
#     /delphix-x500-distinguished-name-fields.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_15.web.objects.X500DistinguishedName import X500DistinguishedName
from delphixpy.v1_11_15 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class X500DistinguishedNameFields(X500DistinguishedName):
    """
    *(extends* :py:class:`v1_11_15.web.vo.X500DistinguishedName` *)* The
    representation of a X.500 Distinguished Name by separate fields.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("X500DistinguishedNameFields", True)
        self._common_name = (self.__undef__, True)
        self._city = (self.__undef__, True)
        self._state_region = (self.__undef__, True)
        self._country = (self.__undef__, True)
        self._organization = (self.__undef__, True)
        self._organization_unit = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._common_name = (data.get("commonName", obj.__undef__), dirty)
        if obj._common_name[0] is not None and obj._common_name[0] is not obj.__undef__:
            assert isinstance(obj._common_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._common_name[0], type(obj._common_name[0])))
            common.validate_format(obj._common_name[0], "None", None, None)
        obj._city = (data.get("city", obj.__undef__), dirty)
        if obj._city[0] is not None and obj._city[0] is not obj.__undef__:
            assert isinstance(obj._city[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._city[0], type(obj._city[0])))
            common.validate_format(obj._city[0], "None", None, None)
        obj._state_region = (data.get("stateRegion", obj.__undef__), dirty)
        if obj._state_region[0] is not None and obj._state_region[0] is not obj.__undef__:
            assert isinstance(obj._state_region[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state_region[0], type(obj._state_region[0])))
            common.validate_format(obj._state_region[0], "None", None, None)
        obj._country = (data.get("country", obj.__undef__), dirty)
        if obj._country[0] is not None and obj._country[0] is not obj.__undef__:
            assert isinstance(obj._country[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._country[0], type(obj._country[0])))
            common.validate_format(obj._country[0], "None", None, None)
        obj._organization = (data.get("organization", obj.__undef__), dirty)
        if obj._organization[0] is not None and obj._organization[0] is not obj.__undef__:
            assert isinstance(obj._organization[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._organization[0], type(obj._organization[0])))
            common.validate_format(obj._organization[0], "None", None, None)
        obj._organization_unit = (data.get("organizationUnit", obj.__undef__), dirty)
        if obj._organization_unit[0] is not None and obj._organization_unit[0] is not obj.__undef__:
            assert isinstance(obj._organization_unit[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._organization_unit[0], type(obj._organization_unit[0])))
            common.validate_format(obj._organization_unit[0], "None", None, None)
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
        if "common_name" == "type" or (self.common_name is not self.__undef__ and (not (dirty and not self._common_name[1]) or self.is_dirty_list(self.common_name, self._common_name) or belongs_to_parent)):
            dct["commonName"] = dictify(self.common_name)
        if "city" == "type" or (self.city is not self.__undef__ and (not (dirty and not self._city[1]) or self.is_dirty_list(self.city, self._city) or belongs_to_parent)):
            dct["city"] = dictify(self.city)
        if "state_region" == "type" or (self.state_region is not self.__undef__ and (not (dirty and not self._state_region[1]) or self.is_dirty_list(self.state_region, self._state_region) or belongs_to_parent)):
            dct["stateRegion"] = dictify(self.state_region)
        if "country" == "type" or (self.country is not self.__undef__ and (not (dirty and not self._country[1]) or self.is_dirty_list(self.country, self._country) or belongs_to_parent)):
            dct["country"] = dictify(self.country)
        if "organization" == "type" or (self.organization is not self.__undef__ and (not (dirty and not self._organization[1]) or self.is_dirty_list(self.organization, self._organization) or belongs_to_parent)):
            dct["organization"] = dictify(self.organization)
        if "organization_unit" == "type" or (self.organization_unit is not self.__undef__ and (not (dirty and not self._organization_unit[1]) or self.is_dirty_list(self.organization_unit, self._organization_unit) or belongs_to_parent)):
            dct["organizationUnit"] = dictify(self.organization_unit)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._common_name = (self._common_name[0], True)
        self._city = (self._city[0], True)
        self._state_region = (self._state_region[0], True)
        self._country = (self._country[0], True)
        self._organization = (self._organization[0], True)
        self._organization_unit = (self._organization_unit[0], True)

    def is_dirty(self):
        return any([self._common_name[1], self._city[1], self._state_region[1], self._country[1], self._organization[1], self._organization_unit[1]])

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
        if not isinstance(other, X500DistinguishedNameFields):
            return False
        return super().__eq__(other) and \
               self.common_name == other.common_name and \
               self.city == other.city and \
               self.state_region == other.state_region and \
               self.country == other.country and \
               self.organization == other.organization and \
               self.organization_unit == other.organization_unit

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def common_name(self):
        """
        Common name (CN).

        :rtype: ``str``
        """
        return self._common_name[0]

    @common_name.setter
    def common_name(self, value):
        self._common_name = (value, True)

    @property
    def city(self):
        """
        City/locality (L).

        :rtype: ``str``
        """
        return self._city[0]

    @city.setter
    def city(self, value):
        self._city = (value, True)

    @property
    def state_region(self):
        """
        State/region (ST).

        :rtype: ``str``
        """
        return self._state_region[0]

    @state_region.setter
    def state_region(self, value):
        self._state_region = (value, True)

    @property
    def country(self):
        """
        Country (C).

        :rtype: ``str``
        """
        return self._country[0]

    @country.setter
    def country(self, value):
        self._country = (value, True)

    @property
    def organization(self):
        """
        Organization (O).

        :rtype: ``str``
        """
        return self._organization[0]

    @organization.setter
    def organization(self, value):
        self._organization = (value, True)

    @property
    def organization_unit(self):
        """
        Organization unit (OU).

        :rtype: ``str``
        """
        return self._organization_unit[0]

    @organization_unit.setter
    def organization_unit(self, value):
        self._organization_unit = (value, True)

