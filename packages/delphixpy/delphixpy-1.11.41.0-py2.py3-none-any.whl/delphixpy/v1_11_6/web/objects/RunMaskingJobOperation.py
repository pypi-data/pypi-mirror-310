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
#     /delphix-run-masking-job-operation.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_6.web.objects.Operation import Operation
from delphixpy.v1_11_6 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RunMaskingJobOperation(Operation):
    """
    *(extends* :py:class:`v1_11_6.web.vo.Operation` *)* An operation that runs
    a Masking Job on the local Delphix Masking Engine instance.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RunMaskingJobOperation", True)
        self._host = (self.__undef__, True)
        self._masking_job_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._host = (data.get("host", obj.__undef__), dirty)
        if obj._host[0] is not None and obj._host[0] is not obj.__undef__:
            assert isinstance(obj._host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._host[0], type(obj._host[0])))
            common.validate_format(obj._host[0], "None", None, None)
        obj._masking_job_id = (data.get("maskingJobId", obj.__undef__), dirty)
        if obj._masking_job_id[0] is not None and obj._masking_job_id[0] is not obj.__undef__:
            assert isinstance(obj._masking_job_id[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._masking_job_id[0], type(obj._masking_job_id[0])))
            common.validate_format(obj._masking_job_id[0], "None", None, None)
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
        if "host" == "type" or (self.host is not self.__undef__ and (not (dirty and not self._host[1]))):
            dct["host"] = dictify(self.host)
        if dirty and "host" in dct:
            del dct["host"]
        if "masking_job_id" == "type" or (self.masking_job_id is not self.__undef__ and (not (dirty and not self._masking_job_id[1]))):
            dct["maskingJobId"] = dictify(self.masking_job_id)
        if dirty and "maskingJobId" in dct:
            del dct["maskingJobId"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._host = (self._host[0], True)
        self._masking_job_id = (self._masking_job_id[0], True)

    def is_dirty(self):
        return any([self._host[1], self._masking_job_id[1]])

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
        if not isinstance(other, RunMaskingJobOperation):
            return False
        return super().__eq__(other) and \
               self.host == other.host and \
               self.masking_job_id == other.masking_job_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.host,
            self.masking_job_id,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def host(self):
        """
        The location this Masking Job will be executed on.

        :rtype: ``str``
        """
        return self._host[0]

    @property
    def masking_job_id(self):
        """
        The Masking Job ID of the Masking Job to be executed.

        :rtype: ``str``
        """
        return self._masking_job_id[0]

