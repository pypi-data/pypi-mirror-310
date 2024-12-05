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
#     /delphix-fault-resolve-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_33.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_33 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class FaultResolveParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_33.web.vo.TypedObject` *)* The parameters to
    use as input when marking a fault as resolved.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("FaultResolveParameters", True)
        self._ignore = (self.__undef__, True)
        self._comments = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._ignore = (data.get("ignore", obj.__undef__), dirty)
        if obj._ignore[0] is not None and obj._ignore[0] is not obj.__undef__:
            assert isinstance(obj._ignore[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._ignore[0], type(obj._ignore[0])))
            common.validate_format(obj._ignore[0], "None", None, None)
        obj._comments = (data.get("comments", obj.__undef__), dirty)
        if obj._comments[0] is not None and obj._comments[0] is not obj.__undef__:
            assert isinstance(obj._comments[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._comments[0], type(obj._comments[0])))
            common.validate_format(obj._comments[0], "None", None, None)
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
        if "ignore" == "type" or (self.ignore is not self.__undef__ and (not (dirty and not self._ignore[1]) or self.is_dirty_list(self.ignore, self._ignore) or belongs_to_parent)):
            dct["ignore"] = dictify(self.ignore)
        elif belongs_to_parent and self.ignore is self.__undef__:
            dct["ignore"] = False
        if "comments" == "type" or (self.comments is not self.__undef__ and (not (dirty and not self._comments[1]) or self.is_dirty_list(self.comments, self._comments) or belongs_to_parent)):
            dct["comments"] = dictify(self.comments)
        elif belongs_to_parent and self.comments is self.__undef__:
            dct["comments"] = ""
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._ignore = (self._ignore[0], True)
        self._comments = (self._comments[0], True)

    def is_dirty(self):
        return any([self._ignore[1], self._comments[1]])

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
        if not isinstance(other, FaultResolveParameters):
            return False
        return super().__eq__(other) and \
               self.ignore == other.ignore and \
               self.comments == other.comments

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def ignore(self):
        """
        Flag indicating whether to ignore this fault if it is detected on the
        same object in the future.

        :rtype: ``bool``
        """
        return self._ignore[0]

    @ignore.setter
    def ignore(self, value):
        self._ignore = (value, True)

    @property
    def comments(self):
        """
        The comments describing the steps taken to resolve a fault.

        :rtype: ``str``
        """
        return self._comments[0]

    @comments.setter
    def comments(self, value):
        self._comments = (value, True)

