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
#     /delphix-staging-source-operations.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_5.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_5 import factory
from delphixpy.v1_11_5 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class StagingSourceOperations(TypedObject):
    """
    *(extends* :py:class:`v1_11_5.web.vo.TypedObject` *)* Describes operations
    which are performed on staging sources at various times.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("StagingSourceOperations", True)
        self._pre_validated_sync = (self.__undef__, True)
        self._post_validated_sync = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._pre_validated_sync = []
        for item in data.get("preValidatedSync") or []:
            obj._pre_validated_sync.append(factory.create_object(item))
            factory.validate_type(obj._pre_validated_sync[-1], "SourceOperation")
        obj._pre_validated_sync = (obj._pre_validated_sync, dirty)
        obj._post_validated_sync = []
        for item in data.get("postValidatedSync") or []:
            obj._post_validated_sync.append(factory.create_object(item))
            factory.validate_type(obj._post_validated_sync[-1], "SourceOperation")
        obj._post_validated_sync = (obj._post_validated_sync, dirty)
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
        if "pre_validated_sync" == "type" or (self.pre_validated_sync is not self.__undef__ and (not (dirty and not self._pre_validated_sync[1]) or self.is_dirty_list(self.pre_validated_sync, self._pre_validated_sync) or belongs_to_parent)):
            dct["preValidatedSync"] = dictify(self.pre_validated_sync, prop_is_list_or_vo=True)
        if "post_validated_sync" == "type" or (self.post_validated_sync is not self.__undef__ and (not (dirty and not self._post_validated_sync[1]) or self.is_dirty_list(self.post_validated_sync, self._post_validated_sync) or belongs_to_parent)):
            dct["postValidatedSync"] = dictify(self.post_validated_sync, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._pre_validated_sync = (self._pre_validated_sync[0], True)
        self._post_validated_sync = (self._post_validated_sync[0], True)

    def is_dirty(self):
        return any([self._pre_validated_sync[1], self._post_validated_sync[1]])

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
        if not isinstance(other, StagingSourceOperations):
            return False
        return super().__eq__(other) and \
               self.pre_validated_sync == other.pre_validated_sync and \
               self.post_validated_sync == other.post_validated_sync

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def pre_validated_sync(self):
        """
        Operations to perform on the staging source before performing a
        validated sync.

        :rtype: ``list`` of :py:class:`v1_11_5.web.vo.SourceOperation`
        """
        return self._pre_validated_sync[0]

    @pre_validated_sync.setter
    def pre_validated_sync(self, value):
        self._pre_validated_sync = (value, True)

    @property
    def post_validated_sync(self):
        """
        Operations to perform on the staging source after performing a
        validated sync.

        :rtype: ``list`` of :py:class:`v1_11_5.web.vo.SourceOperation`
        """
        return self._post_validated_sync[0]

    @post_validated_sync.setter
    def post_validated_sync(self, value):
        self._post_validated_sync = (value, True)

