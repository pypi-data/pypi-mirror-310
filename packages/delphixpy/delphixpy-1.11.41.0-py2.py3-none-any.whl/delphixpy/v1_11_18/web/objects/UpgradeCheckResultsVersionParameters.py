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
#     /delphix-upgrade-check-results-version-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_18.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_18 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UpgradeCheckResultsVersionParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_18.web.vo.TypedObject` *)* Parameters used to
    modify an upgradeCheckResult. These parameters are mutually exclusive.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UpgradeCheckResultsVersionParameters", True)
        self._reference = (self.__undef__, True)
        self._bundle_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._reference = (data.get("reference", obj.__undef__), dirty)
        if obj._reference[0] is not None and obj._reference[0] is not obj.__undef__:
            assert isinstance(obj._reference[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._reference[0], type(obj._reference[0])))
            common.validate_format(obj._reference[0], "objectReference", None, None)
        obj._bundle_id = (data.get("bundleId", obj.__undef__), dirty)
        if obj._bundle_id[0] is not None and obj._bundle_id[0] is not obj.__undef__:
            assert isinstance(obj._bundle_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bundle_id[0], type(obj._bundle_id[0])))
            common.validate_format(obj._bundle_id[0], "None", None, None)
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
        if "reference" == "type" or (self.reference is not self.__undef__ and (not (dirty and not self._reference[1]) or self.is_dirty_list(self.reference, self._reference) or belongs_to_parent)):
            dct["reference"] = dictify(self.reference)
        if "bundle_id" == "type" or (self.bundle_id is not self.__undef__ and (not (dirty and not self._bundle_id[1]) or self.is_dirty_list(self.bundle_id, self._bundle_id) or belongs_to_parent)):
            dct["bundleId"] = dictify(self.bundle_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._reference = (self._reference[0], True)
        self._bundle_id = (self._bundle_id[0], True)

    def is_dirty(self):
        return any([self._reference[1], self._bundle_id[1]])

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
        if not isinstance(other, UpgradeCheckResultsVersionParameters):
            return False
        return super().__eq__(other) and \
               self.reference == other.reference and \
               self.bundle_id == other.bundle_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def reference(self):
        """
        Reference to a single upgrade check result.

        :rtype: ``str``
        """
        return self._reference[0]

    @reference.setter
    def reference(self, value):
        self._reference = (value, True)

    @property
    def bundle_id(self):
        """
        BundleID of upgrade check result(s).

        :rtype: ``str``
        """
        return self._bundle_id[0]

    @bundle_id.setter
    def bundle_id(self, value):
        self._bundle_id = (value, True)

