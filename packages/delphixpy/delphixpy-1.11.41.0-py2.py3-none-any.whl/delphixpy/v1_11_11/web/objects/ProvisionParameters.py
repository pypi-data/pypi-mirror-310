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
#     /delphix-provision-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.VirtualDatasetCreationParameters import VirtualDatasetCreationParameters
from delphixpy.v1_11_11 import factory
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ProvisionParameters(VirtualDatasetCreationParameters):
    """
    *(extends* :py:class:`v1_11_11.web.vo.VirtualDatasetCreationParameters` *)*
    The parameters to use as input when creating a new virtual dataset by
    provisioning.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ProvisionParameters", True)
        self._timeflow_point_parameters = (self.__undef__, True)
        self._masking_job = (self.__undef__, True)
        self._masked = (self.__undef__, True)


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
        obj._masking_job = (data.get("maskingJob", obj.__undef__), dirty)
        if obj._masking_job[0] is not None and obj._masking_job[0] is not obj.__undef__:
            assert isinstance(obj._masking_job[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._masking_job[0], type(obj._masking_job[0])))
            common.validate_format(obj._masking_job[0], "objectReference", None, None)
        obj._masked = (data.get("masked", obj.__undef__), dirty)
        if obj._masked[0] is not None and obj._masked[0] is not obj.__undef__:
            assert isinstance(obj._masked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._masked[0], type(obj._masked[0])))
            common.validate_format(obj._masked[0], "None", None, None)
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
        if "masking_job" == "type" or (self.masking_job is not self.__undef__ and (not (dirty and not self._masking_job[1]) or self.is_dirty_list(self.masking_job, self._masking_job) or belongs_to_parent)):
            dct["maskingJob"] = dictify(self.masking_job)
        if "masked" == "type" or (self.masked is not self.__undef__ and (not (dirty and not self._masked[1]) or self.is_dirty_list(self.masked, self._masked) or belongs_to_parent)):
            dct["masked"] = dictify(self.masked)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._timeflow_point_parameters = (self._timeflow_point_parameters[0], True)
        self._masking_job = (self._masking_job[0], True)
        self._masked = (self._masked[0], True)

    def is_dirty(self):
        return any([self._timeflow_point_parameters[1], self._masking_job[1], self._masked[1]])

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
        if not isinstance(other, ProvisionParameters):
            return False
        return super().__eq__(other) and \
               self.timeflow_point_parameters == other.timeflow_point_parameters and \
               self.masking_job == other.masking_job and \
               self.masked == other.masked

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def timeflow_point_parameters(self):
        """
        The TimeFlow point, bookmark, or semantic location to base provisioning
        on.

        :rtype: :py:class:`v1_11_11.web.vo.TimeflowPointParameters`
        """
        return self._timeflow_point_parameters[0]

    @timeflow_point_parameters.setter
    def timeflow_point_parameters(self, value):
        self._timeflow_point_parameters = (value, True)

    @property
    def masking_job(self):
        """
        The Masking Job to be run when this dataset is provisioned or
        refreshed.

        :rtype: ``str``
        """
        return self._masking_job[0]

    @masking_job.setter
    def masking_job(self, value):
        self._masking_job = (value, True)

    @property
    def masked(self):
        """
        Whether or not to mark this VDB as a masked VDB. It will be marked as
        masked if this flag or the masking job are set.

        :rtype: ``bool``
        """
        return self._masked[0]

    @masked.setter
    def masked(self, value):
        self._masked = (value, True)

