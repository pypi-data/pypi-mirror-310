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
#     /delphix-source-operation.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.Operation import Operation
from delphixpy.v1_11_23 import factory
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SourceOperation(Operation):
    """
    *(extends* :py:class:`v1_11_23.web.vo.Operation` *)* A user-specifiable
    operation that can be performed on sources.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SourceOperation", True)
        self._name = (self.__undef__, True)
        self._credentials_env_vars_list = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", None, None)
        obj._credentials_env_vars_list = []
        for item in data.get("credentialsEnvVarsList") or []:
            obj._credentials_env_vars_list.append(factory.create_object(item))
            factory.validate_type(obj._credentials_env_vars_list[-1], "CredentialsEnvVars")
        obj._credentials_env_vars_list = (obj._credentials_env_vars_list, dirty)
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
        if "credentials_env_vars_list" == "type" or (self.credentials_env_vars_list is not self.__undef__ and (not (dirty and not self._credentials_env_vars_list[1]) or self.is_dirty_list(self.credentials_env_vars_list, self._credentials_env_vars_list) or belongs_to_parent)):
            dct["credentialsEnvVarsList"] = dictify(self.credentials_env_vars_list, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._credentials_env_vars_list = (self._credentials_env_vars_list[0], True)

    def is_dirty(self):
        return any([self._name[1], self._credentials_env_vars_list[1]])

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
        if not isinstance(other, SourceOperation):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.credentials_env_vars_list == other.credentials_env_vars_list

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        A name for the source operation.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def credentials_env_vars_list(self):
        """
        List of environment variables that will contain credentials for this
        operation.

        :rtype: ``list`` of :py:class:`v1_11_23.web.vo.CredentialsEnvVars`
        """
        return self._credentials_env_vars_list[0]

    @credentials_env_vars_list.setter
    def credentials_env_vars_list(self, value):
        self._credentials_env_vars_list = (value, True)

