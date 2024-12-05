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
#     /delphix-oracle-timeflow.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.Timeflow import Timeflow
from delphixpy.v1_11_23 import factory
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleTimeflow(Timeflow):
    """
    *(extends* :py:class:`v1_11_23.web.vo.Timeflow` *)* TimeFlow representing
    historical data for a particular timeline within a data container.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleTimeflow", True)
        self._incarnation_id = (self.__undef__, True)
        self._cdb_timeflow = (self.__undef__, True)
        self._parent_point = (self.__undef__, True)
        self._tde_uuid = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._incarnation_id = (data.get("incarnationID", obj.__undef__), dirty)
        if obj._incarnation_id[0] is not None and obj._incarnation_id[0] is not obj.__undef__:
            assert isinstance(obj._incarnation_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._incarnation_id[0], type(obj._incarnation_id[0])))
            common.validate_format(obj._incarnation_id[0], "None", None, None)
        obj._cdb_timeflow = (data.get("cdbTimeflow", obj.__undef__), dirty)
        if obj._cdb_timeflow[0] is not None and obj._cdb_timeflow[0] is not obj.__undef__:
            assert isinstance(obj._cdb_timeflow[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._cdb_timeflow[0], type(obj._cdb_timeflow[0])))
            common.validate_format(obj._cdb_timeflow[0], "objectReference", None, None)
        if "parentPoint" in data and data["parentPoint"] is not None:
            obj._parent_point = (factory.create_object(data["parentPoint"], "OracleTimeflowPoint"), dirty)
            factory.validate_type(obj._parent_point[0], "OracleTimeflowPoint")
        else:
            obj._parent_point = (obj.__undef__, dirty)
        obj._tde_uuid = (data.get("tdeUUID", obj.__undef__), dirty)
        if obj._tde_uuid[0] is not None and obj._tde_uuid[0] is not obj.__undef__:
            assert isinstance(obj._tde_uuid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tde_uuid[0], type(obj._tde_uuid[0])))
            common.validate_format(obj._tde_uuid[0], "None", None, None)
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
        if "incarnation_id" == "type" or (self.incarnation_id is not self.__undef__ and (not (dirty and not self._incarnation_id[1]))):
            dct["incarnationID"] = dictify(self.incarnation_id)
        if "cdb_timeflow" == "type" or (self.cdb_timeflow is not self.__undef__ and (not (dirty and not self._cdb_timeflow[1]))):
            dct["cdbTimeflow"] = dictify(self.cdb_timeflow)
        if "parent_point" == "type" or (self.parent_point is not self.__undef__ and (not (dirty and not self._parent_point[1]))):
            dct["parentPoint"] = dictify(self.parent_point)
        if "tde_uuid" == "type" or (self.tde_uuid is not self.__undef__ and (not (dirty and not self._tde_uuid[1]))):
            dct["tdeUUID"] = dictify(self.tde_uuid)
        if dirty and "tdeUUID" in dct:
            del dct["tdeUUID"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._incarnation_id = (self._incarnation_id[0], True)
        self._cdb_timeflow = (self._cdb_timeflow[0], True)
        self._parent_point = (self._parent_point[0], True)
        self._tde_uuid = (self._tde_uuid[0], True)

    def is_dirty(self):
        return any([self._incarnation_id[1], self._cdb_timeflow[1], self._parent_point[1], self._tde_uuid[1]])

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
        if not isinstance(other, OracleTimeflow):
            return False
        return super().__eq__(other) and \
               self.incarnation_id == other.incarnation_id and \
               self.cdb_timeflow == other.cdb_timeflow and \
               self.parent_point == other.parent_point and \
               self.tde_uuid == other.tde_uuid

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def incarnation_id(self):
        """
        Oracle-specific incarnation identifier for this TimeFlow.

        :rtype: ``str``
        """
        return self._incarnation_id[0]

    @incarnation_id.setter
    def incarnation_id(self, value):
        self._incarnation_id = (value, True)

    @property
    def cdb_timeflow(self):
        """
        Reference to the mirror CDB TimeFlow if this is a PDB TimeFlow.

        :rtype: ``str``
        """
        return self._cdb_timeflow[0]

    @cdb_timeflow.setter
    def cdb_timeflow(self, value):
        self._cdb_timeflow = (value, True)

    @property
    def parent_point(self):
        """
        The origin point on the parent TimeFlow from which this TimeFlow was
        provisioned. This will not be present for TimeFlows derived from linked
        sources.

        :rtype: :py:class:`v1_11_23.web.vo.OracleTimeflowPoint`
        """
        return self._parent_point[0]

    @parent_point.setter
    def parent_point(self, value):
        self._parent_point = (value, True)

    @property
    def tde_uuid(self):
        """
        Unique identifier for TimeFlow-specific TDE objects that reside outside
        of Delphix storage.

        :rtype: ``str``
        """
        return self._tde_uuid[0]

