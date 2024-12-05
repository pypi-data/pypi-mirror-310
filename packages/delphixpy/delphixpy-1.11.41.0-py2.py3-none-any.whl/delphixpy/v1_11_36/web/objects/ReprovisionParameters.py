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
#     /delphix-reprovision-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_36.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_36 import factory
from delphixpy.v1_11_36 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ReprovisionParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_36.web.vo.TypedObject` *)* The input parameters
    to refresh and rollback requests.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ReprovisionParameters", True)
        self._timeflow_point_parameters = (self.__undef__, True)
        self._instance_number = (self.__undef__, True)
        self._sync_after_reprovision = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "timeflowPointParameters" not in data:
            raise ValueError("Missing required property \"timeflowPointParameters\".")
        if "timeflowPointParameters" in data and data["timeflowPointParameters"] is not None:
            obj._timeflow_point_parameters = (factory.create_object(data["timeflowPointParameters"], "TimeflowPointParameters"), dirty)
            factory.validate_type(obj._timeflow_point_parameters[0], "TimeflowPointParameters")
        else:
            obj._timeflow_point_parameters = (obj.__undef__, dirty)
        obj._instance_number = (data.get("instanceNumber", obj.__undef__), dirty)
        if obj._instance_number[0] is not None and obj._instance_number[0] is not obj.__undef__:
            assert isinstance(obj._instance_number[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._instance_number[0], type(obj._instance_number[0])))
            common.validate_format(obj._instance_number[0], "None", None, None)
        obj._sync_after_reprovision = (data.get("syncAfterReprovision", obj.__undef__), dirty)
        if obj._sync_after_reprovision[0] is not None and obj._sync_after_reprovision[0] is not obj.__undef__:
            assert isinstance(obj._sync_after_reprovision[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._sync_after_reprovision[0], type(obj._sync_after_reprovision[0])))
            common.validate_format(obj._sync_after_reprovision[0], "None", None, None)
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
        if "timeflow_point_parameters" == "type" or (self.timeflow_point_parameters is not self.__undef__ and (not (dirty and not self._timeflow_point_parameters[1]) or self.is_dirty_list(self.timeflow_point_parameters, self._timeflow_point_parameters) or belongs_to_parent)):
            dct["timeflowPointParameters"] = dictify(self.timeflow_point_parameters, prop_is_list_or_vo=True)
        if "instance_number" == "type" or (self.instance_number is not self.__undef__ and (not (dirty and not self._instance_number[1]))):
            dct["instanceNumber"] = dictify(self.instance_number)
        if "sync_after_reprovision" == "type" or (self.sync_after_reprovision is not self.__undef__ and (not (dirty and not self._sync_after_reprovision[1]))):
            dct["syncAfterReprovision"] = dictify(self.sync_after_reprovision)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._timeflow_point_parameters = (self._timeflow_point_parameters[0], True)
        self._instance_number = (self._instance_number[0], True)
        self._sync_after_reprovision = (self._sync_after_reprovision[0], True)

    def is_dirty(self):
        return any([self._timeflow_point_parameters[1], self._instance_number[1], self._sync_after_reprovision[1]])

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
        if not isinstance(other, ReprovisionParameters):
            return False
        return super().__eq__(other) and \
               self.timeflow_point_parameters == other.timeflow_point_parameters and \
               self.instance_number == other.instance_number and \
               self.sync_after_reprovision == other.sync_after_reprovision

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def timeflow_point_parameters(self):
        """
        The TimeFlow point parameter to refresh or rollback the database to.

        :rtype: :py:class:`v1_11_36.web.vo.TimeflowPointParameters`
        """
        return self._timeflow_point_parameters[0]

    @timeflow_point_parameters.setter
    def timeflow_point_parameters(self, value):
        self._timeflow_point_parameters = (value, True)

    @property
    def instance_number(self):
        """
        The optional Oracle RAC instance number to run hooks on. When needed
        this will be returned by the call to deprovision.

        :rtype: ``int``
        """
        return self._instance_number[0]

    @instance_number.setter
    def instance_number(self, value):
        self._instance_number = (value, True)

    @property
    def sync_after_reprovision(self):
        """
        *(default value: True)* Whether a snapshot will be taken after the
        operation completes.

        :rtype: ``bool``
        """
        return self._sync_after_reprovision[0]

    @sync_after_reprovision.setter
    def sync_after_reprovision(self, value):
        self._sync_after_reprovision = (value, True)

