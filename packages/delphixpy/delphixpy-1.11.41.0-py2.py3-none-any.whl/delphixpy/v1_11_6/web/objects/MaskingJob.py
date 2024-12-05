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
#     /delphix-masking-job.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_6.web.objects.UserObject import UserObject
from delphixpy.v1_11_6 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MaskingJob(UserObject):
    """
    *(extends* :py:class:`v1_11_6.web.vo.UserObject` *)* The Delphix Engine
    record of an existing Masking Job.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MaskingJob", True)
        self._name = (self.__undef__, True)
        self._associated_container = (self.__undef__, True)
        self._masking_job_id = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "objectName", None, 256)
        obj._associated_container = (data.get("associatedContainer", obj.__undef__), dirty)
        if obj._associated_container[0] is not None and obj._associated_container[0] is not obj.__undef__:
            assert isinstance(obj._associated_container[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._associated_container[0], type(obj._associated_container[0])))
            common.validate_format(obj._associated_container[0], "objectReference", None, None)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "associated_container" == "type" or (self.associated_container is not self.__undef__ and (not (dirty and not self._associated_container[1]) or self.is_dirty_list(self.associated_container, self._associated_container) or belongs_to_parent)):
            dct["associatedContainer"] = dictify(self.associated_container)
        if "masking_job_id" == "type" or (self.masking_job_id is not self.__undef__ and (not (dirty and not self._masking_job_id[1]) or self.is_dirty_list(self.masking_job_id, self._masking_job_id) or belongs_to_parent)):
            dct["maskingJobId"] = dictify(self.masking_job_id)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._associated_container = (self._associated_container[0], True)
        self._masking_job_id = (self._masking_job_id[0], True)

    def is_dirty(self):
        return any([self._name[1], self._associated_container[1], self._masking_job_id[1]])

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
        if not isinstance(other, MaskingJob):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.associated_container == other.associated_container and \
               self.masking_job_id == other.masking_job_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        Object name.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def associated_container(self):
        """
        A reference to the container that the Masking Job is intended to
        operate on.

        :rtype: ``str`` *or* ``null``
        """
        return self._associated_container[0]

    @associated_container.setter
    def associated_container(self, value):
        self._associated_container = (value, True)

    @property
    def masking_job_id(self):
        """
        The masking job id from the Delphix Masking Engine instance that
        specifies the desired Masking Job.

        :rtype: ``str``
        """
        return self._masking_job_id[0]

    @masking_job_id.setter
    def masking_job_id(self, value):
        self._masking_job_id = (value, True)

