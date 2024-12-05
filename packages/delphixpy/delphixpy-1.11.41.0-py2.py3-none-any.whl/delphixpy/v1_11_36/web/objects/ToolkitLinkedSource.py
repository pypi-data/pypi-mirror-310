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
#     /delphix-toolkit-linked-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ToolkitLinkedSource(TypedObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TypedObject` *)* A linked source
    definition for toolkits.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ToolkitLinkedSource", True)
        self._parameters = (self.__undef__, True)
        self._pre_snapshot = (self.__undef__, True)
        self._post_snapshot = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "parameters" not in data:
            raise ValueError("Missing required property \"parameters\".")
        if "parameters" in data and data["parameters"] is not None:
            obj._parameters = (data["parameters"], dirty)
        else:
            obj._parameters = (obj.__undef__, dirty)
        if "preSnapshot" not in data:
            raise ValueError("Missing required property \"preSnapshot\".")
        obj._pre_snapshot = (data.get("preSnapshot", obj.__undef__), dirty)
        if obj._pre_snapshot[0] is not None and obj._pre_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._pre_snapshot[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pre_snapshot[0], type(obj._pre_snapshot[0])))
            common.validate_format(obj._pre_snapshot[0], "None", None, None)
        if "postSnapshot" not in data:
            raise ValueError("Missing required property \"postSnapshot\".")
        obj._post_snapshot = (data.get("postSnapshot", obj.__undef__), dirty)
        if obj._post_snapshot[0] is not None and obj._post_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._post_snapshot[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._post_snapshot[0], type(obj._post_snapshot[0])))
            common.validate_format(obj._post_snapshot[0], "None", None, None)
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
        if "parameters" == "type" or (self.parameters is not self.__undef__ and (not (dirty and not self._parameters[1]) or self.is_dirty_list(self.parameters, self._parameters) or belongs_to_parent)):
            dct["parameters"] = dictify(self.parameters, prop_is_list_or_vo=True)
        if "pre_snapshot" == "type" or (self.pre_snapshot is not self.__undef__ and (not (dirty and not self._pre_snapshot[1]) or self.is_dirty_list(self.pre_snapshot, self._pre_snapshot) or belongs_to_parent)):
            dct["preSnapshot"] = dictify(self.pre_snapshot)
        if "post_snapshot" == "type" or (self.post_snapshot is not self.__undef__ and (not (dirty and not self._post_snapshot[1]) or self.is_dirty_list(self.post_snapshot, self._post_snapshot) or belongs_to_parent)):
            dct["postSnapshot"] = dictify(self.post_snapshot)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._parameters = (self._parameters[0], True)
        self._pre_snapshot = (self._pre_snapshot[0], True)
        self._post_snapshot = (self._post_snapshot[0], True)

    def is_dirty(self):
        return any([self._parameters[1], self._pre_snapshot[1], self._post_snapshot[1]])

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
        if not isinstance(other, ToolkitLinkedSource):
            return False
        return super().__eq__(other) and \
               self.parameters == other.parameters and \
               self.pre_snapshot == other.pre_snapshot and \
               self.post_snapshot == other.post_snapshot

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def parameters(self):
        """
        A user defined schema for the linking parameters.

        :rtype: :py:class:`v1_11_36.web.vo.SchemaDraftV4`
        """
        return self._parameters[0]

    @parameters.setter
    def parameters(self, value):
        self._parameters = (value, True)

    @property
    def pre_snapshot(self):
        """
        A workflow script to run just prior to snapshotting the staged source.

        :rtype: ``str``
        """
        return self._pre_snapshot[0]

    @pre_snapshot.setter
    def pre_snapshot(self, value):
        self._pre_snapshot = (value, True)

    @property
    def post_snapshot(self):
        """
        A workflow script to run immediately after snapshotting the staged
        source.

        :rtype: ``str``
        """
        return self._post_snapshot[0]

    @post_snapshot.setter
    def post_snapshot(self, value):
        self._post_snapshot = (value, True)

