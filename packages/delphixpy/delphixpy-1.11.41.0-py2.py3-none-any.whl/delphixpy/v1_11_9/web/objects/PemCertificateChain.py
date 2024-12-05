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
#     /delphix-pem-certificate-chain.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_9.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_9 import factory
from delphixpy.v1_11_9 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PemCertificateChain(TypedObject):
    """
    *(extends* :py:class:`v1_11_9.web.vo.TypedObject` *)* A chain of X.509
    Certificates in PEM format.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PemCertificateChain", True)
        self._chain = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "chain" not in data:
            raise ValueError("Missing required property \"chain\".")
        obj._chain = []
        for item in data.get("chain") or []:
            obj._chain.append(factory.create_object(item))
            factory.validate_type(obj._chain[-1], "PemCertificate")
        obj._chain = (obj._chain, dirty)
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
        if "chain" == "type" or (self.chain is not self.__undef__ and (not (dirty and not self._chain[1]) or self.is_dirty_list(self.chain, self._chain) or belongs_to_parent)):
            dct["chain"] = dictify(self.chain, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._chain = (self._chain[0], True)

    def is_dirty(self):
        return any([self._chain[1]])

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
        if not isinstance(other, PemCertificateChain):
            return False
        return super().__eq__(other) and \
               self.chain == other.chain

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def chain(self):
        """
        The chain of X.509 certificates in PEM format.

        :rtype: ``list`` of :py:class:`v1_11_9.web.vo.PemCertificate`
        """
        return self._chain[0]

    @chain.setter
    def chain(self, value):
        self._chain = (value, True)

