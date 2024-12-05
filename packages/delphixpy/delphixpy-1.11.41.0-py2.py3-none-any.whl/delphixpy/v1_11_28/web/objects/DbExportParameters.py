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
#     /delphix-db-export-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_28.web.objects.GenericExportParameters import GenericExportParameters
from delphixpy.v1_11_28 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class DbExportParameters(GenericExportParameters):
    """
    *(extends* :py:class:`v1_11_28.web.vo.GenericExportParameters` *)* The
    parameters to use as input for export requests.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("DbExportParameters", True)
        self._recover_database = (self.__undef__, True)
        self._config_params = (self.__undef__, True)
        self._file_mapping_rules = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._recover_database = (data.get("recoverDatabase", obj.__undef__), dirty)
        if obj._recover_database[0] is not None and obj._recover_database[0] is not obj.__undef__:
            assert isinstance(obj._recover_database[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._recover_database[0], type(obj._recover_database[0])))
            common.validate_format(obj._recover_database[0], "None", None, None)
        obj._config_params = (data.get("configParams", obj.__undef__), dirty)
        if obj._config_params[0] is not None and obj._config_params[0] is not obj.__undef__:
            assert isinstance(obj._config_params[0], dict), ("Expected one of ['object'], but got %s of type %s" % (obj._config_params[0], type(obj._config_params[0])))
            common.validate_format(obj._config_params[0], "None", None, None)
        obj._file_mapping_rules = (data.get("fileMappingRules", obj.__undef__), dirty)
        if obj._file_mapping_rules[0] is not None and obj._file_mapping_rules[0] is not obj.__undef__:
            assert isinstance(obj._file_mapping_rules[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._file_mapping_rules[0], type(obj._file_mapping_rules[0])))
            common.validate_format(obj._file_mapping_rules[0], "None", None, None)
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
        if "recover_database" == "type" or (self.recover_database is not self.__undef__ and (not (dirty and not self._recover_database[1]) or self.is_dirty_list(self.recover_database, self._recover_database) or belongs_to_parent)):
            dct["recoverDatabase"] = dictify(self.recover_database)
        elif belongs_to_parent and self.recover_database is self.__undef__:
            dct["recoverDatabase"] = True
        if "config_params" == "type" or (self.config_params is not self.__undef__ and (not (dirty and not self._config_params[1]) or self.is_dirty_list(self.config_params, self._config_params) or belongs_to_parent)):
            dct["configParams"] = dictify(self.config_params, prop_is_list_or_vo=True)
        if "file_mapping_rules" == "type" or (self.file_mapping_rules is not self.__undef__ and (not (dirty and not self._file_mapping_rules[1]) or self.is_dirty_list(self.file_mapping_rules, self._file_mapping_rules) or belongs_to_parent)):
            dct["fileMappingRules"] = dictify(self.file_mapping_rules)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._recover_database = (self._recover_database[0], True)
        self._config_params = (self._config_params[0], True)
        self._file_mapping_rules = (self._file_mapping_rules[0], True)

    def is_dirty(self):
        return any([self._recover_database[1], self._config_params[1], self._file_mapping_rules[1]])

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
        if not isinstance(other, DbExportParameters):
            return False
        return super().__eq__(other) and \
               self.recover_database == other.recover_database and \
               self.config_params == other.config_params and \
               self.file_mapping_rules == other.file_mapping_rules

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def recover_database(self):
        """
        *(default value: True)* If specified, then take the exported database
        through recovery procedures, if necessary, to reach a consistent point.

        :rtype: ``bool``
        """
        return self._recover_database[0]

    @recover_database.setter
    def recover_database(self, value):
        self._recover_database = (value, True)

    @property
    def config_params(self):
        """
        Database-specific configuration parameters.

        :rtype: ``dict``
        """
        return self._config_params[0]

    @config_params.setter
    def config_params(self, value):
        self._config_params = (value, True)

    @property
    def file_mapping_rules(self):
        """
        Database file mapping rules.

        :rtype: ``str``
        """
        return self._file_mapping_rules[0]

    @file_mapping_rules.setter
    def file_mapping_rules(self, value):
        self._file_mapping_rules = (value, True)

