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
#     /delphix-timeflow.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_35.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_35 import factory
from delphixpy.v1_11_35 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Timeflow(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_35.web.vo.NamedUserObject` *)* Data for a
    particular historical timeline within a database.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Timeflow", True)
        self._container = (self.__undef__, True)
        self._parent_point = (self.__undef__, True)
        self._parent_snapshot = (self.__undef__, True)
        self._creation_type = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "objectReference", None, None)
        if "parentPoint" in data and data["parentPoint"] is not None:
            obj._parent_point = (factory.create_object(data["parentPoint"], "TimeflowPoint"), dirty)
            factory.validate_type(obj._parent_point[0], "TimeflowPoint")
        else:
            obj._parent_point = (obj.__undef__, dirty)
        obj._parent_snapshot = (data.get("parentSnapshot", obj.__undef__), dirty)
        if obj._parent_snapshot[0] is not None and obj._parent_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._parent_snapshot[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent_snapshot[0], type(obj._parent_snapshot[0])))
            common.validate_format(obj._parent_snapshot[0], "objectReference", None, None)
        obj._creation_type = (data.get("creationType", obj.__undef__), dirty)
        if obj._creation_type[0] is not None and obj._creation_type[0] is not obj.__undef__:
            assert isinstance(obj._creation_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._creation_type[0], type(obj._creation_type[0])))
            assert obj._creation_type[0] in ['INITIAL', 'INDETERMINATE', 'REFRESH', 'ROLLBACK', 'TEMPORARY', 'TRANSFORMATION', 'V2P', 'PDB_PLUG', 'ORACLE_LIVE_SOURCE_RESYNC', 'SOURCE_CONTINUITY'], "Expected enum ['INITIAL', 'INDETERMINATE', 'REFRESH', 'ROLLBACK', 'TEMPORARY', 'TRANSFORMATION', 'V2P', 'PDB_PLUG', 'ORACLE_LIVE_SOURCE_RESYNC', 'SOURCE_CONTINUITY'] but got %s" % obj._creation_type[0]
            common.validate_format(obj._creation_type[0], "None", None, None)
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
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]))):
            dct["container"] = dictify(self.container)
        if "parent_point" == "type" or (self.parent_point is not self.__undef__ and (not (dirty and not self._parent_point[1]))):
            dct["parentPoint"] = dictify(self.parent_point)
        if "parent_snapshot" == "type" or (self.parent_snapshot is not self.__undef__ and (not (dirty and not self._parent_snapshot[1]))):
            dct["parentSnapshot"] = dictify(self.parent_snapshot)
        if "creation_type" == "type" or (self.creation_type is not self.__undef__ and (not (dirty and not self._creation_type[1]))):
            dct["creationType"] = dictify(self.creation_type)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._container = (self._container[0], True)
        self._parent_point = (self._parent_point[0], True)
        self._parent_snapshot = (self._parent_snapshot[0], True)
        self._creation_type = (self._creation_type[0], True)

    def is_dirty(self):
        return any([self._container[1], self._parent_point[1], self._parent_snapshot[1], self._creation_type[1]])

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
        if not isinstance(other, Timeflow):
            return False
        return super().__eq__(other) and \
               self.container == other.container and \
               self.parent_point == other.parent_point and \
               self.parent_snapshot == other.parent_snapshot and \
               self.creation_type == other.creation_type

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def container(self):
        """
        Reference to the data container (database) for this TimeFlow.

        :rtype: ``str``
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def parent_point(self):
        """
        The origin point on the parent TimeFlow from which this TimeFlow was
        provisioned. This will not be present for TimeFlows derived from linked
        sources.

        :rtype: :py:class:`v1_11_35.web.vo.TimeflowPoint`
        """
        return self._parent_point[0]

    @parent_point.setter
    def parent_point(self, value):
        self._parent_point = (value, True)

    @property
    def parent_snapshot(self):
        """
        Reference to the parent snapshot that serves as the provisioning base
        for this object. This may be different from the snapshot within the
        parent point, and is only present for virtual TimeFlows.

        :rtype: ``str``
        """
        return self._parent_snapshot[0]

    @parent_snapshot.setter
    def parent_snapshot(self, value):
        self._parent_snapshot = (value, True)

    @property
    def creation_type(self):
        """
        The source action that created the TimeFlow. *(permitted values:
        INITIAL, INDETERMINATE, REFRESH, ROLLBACK, TEMPORARY, TRANSFORMATION,
        V2P, PDB_PLUG, ORACLE_LIVE_SOURCE_RESYNC, SOURCE_CONTINUITY)*

        :rtype: ``str``
        """
        return self._creation_type[0]

    @creation_type.setter
    def creation_type(self, value):
        self._creation_type = (value, True)

