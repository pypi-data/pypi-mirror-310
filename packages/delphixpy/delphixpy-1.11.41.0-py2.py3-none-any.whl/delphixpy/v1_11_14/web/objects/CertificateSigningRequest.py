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
#     /delphix-certificate-signing-request.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.UserObject import UserObject
from delphixpy.v1_11_14 import factory
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CertificateSigningRequest(UserObject):
    """
    *(extends* :py:class:`v1_11_14.web.vo.UserObject` *)* Certificate signing
    request (CSR).
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CertificateSigningRequest", True)
        self._name = (self.__undef__, True)
        self._end_entity = (self.__undef__, True)
        self._key_pair = (self.__undef__, True)
        self._request_in_pem = (self.__undef__, True)
        self._subject_alternative_names = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "objectName", None, None)
        if "endEntity" in data and data["endEntity"] is not None:
            obj._end_entity = (factory.create_object(data["endEntity"], "EndEntity"), dirty)
            factory.validate_type(obj._end_entity[0], "EndEntity")
        else:
            obj._end_entity = (obj.__undef__, dirty)
        if "keyPair" in data and data["keyPair"] is not None:
            obj._key_pair = (factory.create_object(data["keyPair"], "KeyPair"), dirty)
            factory.validate_type(obj._key_pair[0], "KeyPair")
        else:
            obj._key_pair = (obj.__undef__, dirty)
        obj._request_in_pem = (data.get("requestInPem", obj.__undef__), dirty)
        if obj._request_in_pem[0] is not None and obj._request_in_pem[0] is not obj.__undef__:
            assert isinstance(obj._request_in_pem[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._request_in_pem[0], type(obj._request_in_pem[0])))
            common.validate_format(obj._request_in_pem[0], "None", None, None)
        obj._subject_alternative_names = []
        for item in data.get("subjectAlternativeNames") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "host", None, None)
            obj._subject_alternative_names.append(item)
        obj._subject_alternative_names = (obj._subject_alternative_names, dirty)
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
        if "end_entity" == "type" or (self.end_entity is not self.__undef__ and (not (dirty and not self._end_entity[1]))):
            dct["endEntity"] = dictify(self.end_entity)
        if "key_pair" == "type" or (self.key_pair is not self.__undef__ and (not (dirty and not self._key_pair[1]))):
            dct["keyPair"] = dictify(self.key_pair)
        if "request_in_pem" == "type" or (self.request_in_pem is not self.__undef__ and (not (dirty and not self._request_in_pem[1]))):
            dct["requestInPem"] = dictify(self.request_in_pem)
        if "subject_alternative_names" == "type" or (self.subject_alternative_names is not self.__undef__ and (not (dirty and not self._subject_alternative_names[1]))):
            dct["subjectAlternativeNames"] = dictify(self.subject_alternative_names)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._end_entity = (self._end_entity[0], True)
        self._key_pair = (self._key_pair[0], True)
        self._request_in_pem = (self._request_in_pem[0], True)
        self._subject_alternative_names = (self._subject_alternative_names[0], True)

    def is_dirty(self):
        return any([self._name[1], self._end_entity[1], self._key_pair[1], self._request_in_pem[1], self._subject_alternative_names[1]])

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
        if not isinstance(other, CertificateSigningRequest):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.end_entity == other.end_entity and \
               self.key_pair == other.key_pair and \
               self.request_in_pem == other.request_in_pem and \
               self.subject_alternative_names == other.subject_alternative_names

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        The Distinguished Name.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def end_entity(self):
        """
        The specific TLS service this CSR was generated for.

        :rtype: :py:class:`v1_11_14.web.vo.EndEntity`
        """
        return self._end_entity[0]

    @end_entity.setter
    def end_entity(self, value):
        self._end_entity = (value, True)

    @property
    def key_pair(self):
        """
        The backing key pair and signature algorithm it will use.

        :rtype: :py:class:`v1_11_14.web.vo.KeyPair`
        """
        return self._key_pair[0]

    @key_pair.setter
    def key_pair(self, value):
        self._key_pair = (value, True)

    @property
    def request_in_pem(self):
        """
        The CSR in PEM format.

        :rtype: ``str``
        """
        return self._request_in_pem[0]

    @request_in_pem.setter
    def request_in_pem(self, value):
        self._request_in_pem = (value, True)

    @property
    def subject_alternative_names(self):
        """
        The subject alternative names associated with this certificate.

        :rtype: ``list`` of ``str``
        """
        return self._subject_alternative_names[0]

    @subject_alternative_names.setter
    def subject_alternative_names(self, value):
        self._subject_alternative_names = (value, True)

