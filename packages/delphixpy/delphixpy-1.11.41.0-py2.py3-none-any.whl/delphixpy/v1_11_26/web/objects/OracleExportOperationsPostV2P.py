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
#     /delphix-oracle-export-operations-post-v2p.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_26.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_26 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleExportOperationsPostV2P(TypedObject):
    """
    *(extends* :py:class:`v1_11_26.web.vo.TypedObject` *)* Describes operations
    allowed on virtual source post V2P.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleExportOperationsPostV2P", True)
        self._allow_refresh_rewind_post_v2_p = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._allow_refresh_rewind_post_v2_p = (data.get("allowRefreshRewindPostV2P", obj.__undef__), dirty)
        if obj._allow_refresh_rewind_post_v2_p[0] is not None and obj._allow_refresh_rewind_post_v2_p[0] is not obj.__undef__:
            assert isinstance(obj._allow_refresh_rewind_post_v2_p[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._allow_refresh_rewind_post_v2_p[0], type(obj._allow_refresh_rewind_post_v2_p[0])))
            common.validate_format(obj._allow_refresh_rewind_post_v2_p[0], "None", None, None)
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
        if "allow_refresh_rewind_post_v2_p" == "type" or (self.allow_refresh_rewind_post_v2_p is not self.__undef__ and (not (dirty and not self._allow_refresh_rewind_post_v2_p[1]) or self.is_dirty_list(self.allow_refresh_rewind_post_v2_p, self._allow_refresh_rewind_post_v2_p) or belongs_to_parent)):
            dct["allowRefreshRewindPostV2P"] = dictify(self.allow_refresh_rewind_post_v2_p)
        elif belongs_to_parent and self.allow_refresh_rewind_post_v2_p is self.__undef__:
            dct["allowRefreshRewindPostV2P"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._allow_refresh_rewind_post_v2_p = (self._allow_refresh_rewind_post_v2_p[0], True)

    def is_dirty(self):
        return any([self._allow_refresh_rewind_post_v2_p[1]])

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
        if not isinstance(other, OracleExportOperationsPostV2P):
            return False
        return super().__eq__(other) and \
               self.allow_refresh_rewind_post_v2_p == other.allow_refresh_rewind_post_v2_p

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def allow_refresh_rewind_post_v2_p(self):
        """
        Indicates whether refresh/rewind operation allowed on virtual source
        post V2P.

        :rtype: ``bool``
        """
        return self._allow_refresh_rewind_post_v2_p[0]

    @allow_refresh_rewind_post_v2_p.setter
    def allow_refresh_rewind_post_v2_p(self, value):
        self._allow_refresh_rewind_post_v2_p = (value, True)

