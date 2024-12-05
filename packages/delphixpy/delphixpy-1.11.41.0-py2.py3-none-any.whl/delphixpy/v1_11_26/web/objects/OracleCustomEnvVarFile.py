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
#     /delphix-oracle-custom-env-var-file.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_26.web.objects.OracleCustomEnvVar import OracleCustomEnvVar
from delphixpy.v1_11_26 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleCustomEnvVarFile(OracleCustomEnvVar):
    """
    *(extends* :py:class:`v1_11_26.web.vo.OracleCustomEnvVar` *)* Dictates an
    environment file to be sourced when the Delphix Engine administers an
    Oracle virtual database. This environment file must be available on the
    target environment. This type also includes parameters which will be passed
    to the environment file when it is sourced.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleCustomEnvVarFile", True)
        self._path_parameters = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "pathParameters" not in data:
            raise ValueError("Missing required property \"pathParameters\".")
        obj._path_parameters = (data.get("pathParameters", obj.__undef__), dirty)
        if obj._path_parameters[0] is not None and obj._path_parameters[0] is not obj.__undef__:
            assert isinstance(obj._path_parameters[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._path_parameters[0], type(obj._path_parameters[0])))
            common.validate_format(obj._path_parameters[0], "None", None, None)
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
        if "path_parameters" == "type" or (self.path_parameters is not self.__undef__ and (not (dirty and not self._path_parameters[1]) or self.is_dirty_list(self.path_parameters, self._path_parameters) or belongs_to_parent)):
            dct["pathParameters"] = dictify(self.path_parameters)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._path_parameters = (self._path_parameters[0], True)

    def is_dirty(self):
        return any([self._path_parameters[1]])

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
        if not isinstance(other, OracleCustomEnvVarFile):
            return False
        return super().__eq__(other) and \
               self.path_parameters == other.path_parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def path_parameters(self):
        """
        A string of whitespace-separated parameters to be passed to the source
        command. The first parameter must be an absolute path to a file that
        exists on the target environment. Every subsequent parameter will be
        treated as an argument interpreted by the environment file.

        :rtype: ``str``
        """
        return self._path_parameters[0]

    @path_parameters.setter
    def path_parameters(self, value):
        self._path_parameters = (value, True)

