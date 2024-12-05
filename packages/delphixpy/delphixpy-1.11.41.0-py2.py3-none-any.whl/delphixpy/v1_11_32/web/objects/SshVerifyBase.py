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
#     /delphix-ssh-verify-base.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_32.web.objects.SshVerificationStrategy import SshVerificationStrategy
from delphixpy.v1_11_32 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SshVerifyBase(SshVerificationStrategy):
    """
    *(extends* :py:class:`v1_11_32.web.vo.SshVerificationStrategy` *)* Base for
    ssh verification strategies that use the host's key.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SshVerifyBase", True)
        self._key_type = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "keyType" not in data:
            raise ValueError("Missing required property \"keyType\".")
        obj._key_type = (data.get("keyType", obj.__undef__), dirty)
        if obj._key_type[0] is not None and obj._key_type[0] is not obj.__undef__:
            assert isinstance(obj._key_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._key_type[0], type(obj._key_type[0])))
            assert obj._key_type[0] in ['RSA', 'DSA', 'ECDSA', 'ED25519'], "Expected enum ['RSA', 'DSA', 'ECDSA', 'ED25519'] but got %s" % obj._key_type[0]
            common.validate_format(obj._key_type[0], "None", None, None)
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
        if "key_type" == "type" or (self.key_type is not self.__undef__ and (not (dirty and not self._key_type[1]) or self.is_dirty_list(self.key_type, self._key_type) or belongs_to_parent)):
            dct["keyType"] = dictify(self.key_type)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._key_type = (self._key_type[0], True)

    def is_dirty(self):
        return any([self._key_type[1]])

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
        if not isinstance(other, SshVerifyBase):
            return False
        return super().__eq__(other) and \
               self.key_type == other.key_type

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def key_type(self):
        """
        Type of ssh key. *(permitted values: RSA, DSA, ECDSA, ED25519)*

        :rtype: ``str``
        """
        return self._key_type[0]

    @key_type.setter
    def key_type(self, value):
        self._key_type = (value, True)

