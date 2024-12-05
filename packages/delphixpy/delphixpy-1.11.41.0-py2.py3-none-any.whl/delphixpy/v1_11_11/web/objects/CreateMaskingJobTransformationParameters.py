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
#     /delphix-create-masking-job-transformation-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_11 import factory
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CreateMaskingJobTransformationParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_11.web.vo.TypedObject` *)* Represents the
    parameters to create a transformation for a provided Masking Job.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CreateMaskingJobTransformationParameters", True)
        self._container = (self.__undef__, True)
        self._environment_user = (self.__undef__, True)
        self._repository = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "container" in data and data["container"] is not None:
            obj._container = (factory.create_object(data["container"], "Container"), dirty)
            factory.validate_type(obj._container[0], "Container")
        else:
            obj._container = (obj.__undef__, dirty)
        obj._environment_user = (data.get("environmentUser", obj.__undef__), dirty)
        if obj._environment_user[0] is not None and obj._environment_user[0] is not obj.__undef__:
            assert isinstance(obj._environment_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._environment_user[0], type(obj._environment_user[0])))
            common.validate_format(obj._environment_user[0], "objectReference", None, None)
        obj._repository = (data.get("repository", obj.__undef__), dirty)
        if obj._repository[0] is not None and obj._repository[0] is not obj.__undef__:
            assert isinstance(obj._repository[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._repository[0], type(obj._repository[0])))
            common.validate_format(obj._repository[0], "objectReference", None, None)
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
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]) or self.is_dirty_list(self.container, self._container) or belongs_to_parent)):
            dct["container"] = dictify(self.container, prop_is_list_or_vo=True)
        if "environment_user" == "type" or (self.environment_user is not self.__undef__ and (not (dirty and not self._environment_user[1]) or self.is_dirty_list(self.environment_user, self._environment_user) or belongs_to_parent)):
            dct["environmentUser"] = dictify(self.environment_user)
        if "repository" == "type" or (self.repository is not self.__undef__ and (not (dirty and not self._repository[1]) or self.is_dirty_list(self.repository, self._repository) or belongs_to_parent)):
            dct["repository"] = dictify(self.repository)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._container = (self._container[0], True)
        self._environment_user = (self._environment_user[0], True)
        self._repository = (self._repository[0], True)

    def is_dirty(self):
        return any([self._container[1], self._environment_user[1], self._repository[1]])

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
        if not isinstance(other, CreateMaskingJobTransformationParameters):
            return False
        return super().__eq__(other) and \
               self.container == other.container and \
               self.environment_user == other.environment_user and \
               self.repository == other.repository

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def container(self):
        """
        The container that will contain the masked data associated with the
        newly created transformation; the "transformation container".

        :rtype: :py:class:`v1_11_11.web.vo.Container`
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def environment_user(self):
        """
        Reference to the user used during application of the transformation.

        :rtype: ``str``
        """
        return self._environment_user[0]

    @environment_user.setter
    def environment_user(self, value):
        self._environment_user = (value, True)

    @property
    def repository(self):
        """
        Reference to the repository used during application of the
        transformation.

        :rtype: ``str``
        """
        return self._repository[0]

    @repository.setter
    def repository(self, value):
        self._repository = (value, True)

