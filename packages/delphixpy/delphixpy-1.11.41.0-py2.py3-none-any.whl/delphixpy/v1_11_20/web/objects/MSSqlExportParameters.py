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
#     /delphix-mssql-export-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.DbExportParameters import DbExportParameters
from delphixpy.v1_11_20 import factory
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlExportParameters(DbExportParameters):
    """
    *(extends* :py:class:`v1_11_20.web.vo.DbExportParameters` *)* The
    parameters to use as input to export MSSQL databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlExportParameters", True)
        self._source_config = (self.__undef__, True)
        self._recovery_model = (self.__undef__, True)
        self._filesystem_layout = (self.__undef__, True)
        self._enable_cdc = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "sourceConfig" not in data:
            raise ValueError("Missing required property \"sourceConfig\".")
        if "sourceConfig" in data and data["sourceConfig"] is not None:
            obj._source_config = (factory.create_object(data["sourceConfig"], "MSSqlDBConfig"), dirty)
            factory.validate_type(obj._source_config[0], "MSSqlDBConfig")
        else:
            obj._source_config = (obj.__undef__, dirty)
        obj._recovery_model = (data.get("recoveryModel", obj.__undef__), dirty)
        if obj._recovery_model[0] is not None and obj._recovery_model[0] is not obj.__undef__:
            assert isinstance(obj._recovery_model[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._recovery_model[0], type(obj._recovery_model[0])))
            assert obj._recovery_model[0] in ['SIMPLE', 'BULK_LOGGED', 'FULL'], "Expected enum ['SIMPLE', 'BULK_LOGGED', 'FULL'] but got %s" % obj._recovery_model[0]
            common.validate_format(obj._recovery_model[0], "None", None, None)
        if "filesystemLayout" not in data:
            raise ValueError("Missing required property \"filesystemLayout\".")
        if "filesystemLayout" in data and data["filesystemLayout"] is not None:
            obj._filesystem_layout = (factory.create_object(data["filesystemLayout"], "MSSqlTimeflowFilesystemLayout"), dirty)
            factory.validate_type(obj._filesystem_layout[0], "MSSqlTimeflowFilesystemLayout")
        else:
            obj._filesystem_layout = (obj.__undef__, dirty)
        obj._enable_cdc = (data.get("enableCdc", obj.__undef__), dirty)
        if obj._enable_cdc[0] is not None and obj._enable_cdc[0] is not obj.__undef__:
            assert isinstance(obj._enable_cdc[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enable_cdc[0], type(obj._enable_cdc[0])))
            common.validate_format(obj._enable_cdc[0], "None", None, None)
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
        if "source_config" == "type" or (self.source_config is not self.__undef__ and (not (dirty and not self._source_config[1]) or self.is_dirty_list(self.source_config, self._source_config) or belongs_to_parent)):
            dct["sourceConfig"] = dictify(self.source_config, prop_is_list_or_vo=True)
        if "recovery_model" == "type" or (self.recovery_model is not self.__undef__ and (not (dirty and not self._recovery_model[1]) or self.is_dirty_list(self.recovery_model, self._recovery_model) or belongs_to_parent)):
            dct["recoveryModel"] = dictify(self.recovery_model)
        elif belongs_to_parent and self.recovery_model is self.__undef__:
            dct["recoveryModel"] = "FULL"
        if "filesystem_layout" == "type" or (self.filesystem_layout is not self.__undef__ and (not (dirty and not self._filesystem_layout[1]) or self.is_dirty_list(self.filesystem_layout, self._filesystem_layout) or belongs_to_parent)):
            dct["filesystemLayout"] = dictify(self.filesystem_layout, prop_is_list_or_vo=True)
        if "enable_cdc" == "type" or (self.enable_cdc is not self.__undef__ and (not (dirty and not self._enable_cdc[1]) or self.is_dirty_list(self.enable_cdc, self._enable_cdc) or belongs_to_parent)):
            dct["enableCdc"] = dictify(self.enable_cdc)
        elif belongs_to_parent and self.enable_cdc is self.__undef__:
            dct["enableCdc"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._source_config = (self._source_config[0], True)
        self._recovery_model = (self._recovery_model[0], True)
        self._filesystem_layout = (self._filesystem_layout[0], True)
        self._enable_cdc = (self._enable_cdc[0], True)

    def is_dirty(self):
        return any([self._source_config[1], self._recovery_model[1], self._filesystem_layout[1], self._enable_cdc[1]])

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
        if not isinstance(other, MSSqlExportParameters):
            return False
        return super().__eq__(other) and \
               self.source_config == other.source_config and \
               self.recovery_model == other.recovery_model and \
               self.filesystem_layout == other.filesystem_layout and \
               self.enable_cdc == other.enable_cdc

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def source_config(self):
        """
        The source config to use when creating the exported DB.

        :rtype: :py:class:`v1_11_20.web.vo.MSSqlDBConfig`
        """
        return self._source_config[0]

    @source_config.setter
    def source_config(self, value):
        self._source_config = (value, True)

    @property
    def recovery_model(self):
        """
        *(default value: FULL)* Recovery model of the database. *(permitted
        values: SIMPLE, BULK_LOGGED, FULL)*

        :rtype: ``str``
        """
        return self._recovery_model[0]

    @recovery_model.setter
    def recovery_model(self, value):
        self._recovery_model = (value, True)

    @property
    def filesystem_layout(self):
        """
        The filesystem configuration of the exported MSSQL database.

        :rtype: :py:class:`v1_11_20.web.vo.MSSqlTimeflowFilesystemLayout`
        """
        return self._filesystem_layout[0]

    @filesystem_layout.setter
    def filesystem_layout(self, value):
        self._filesystem_layout = (value, True)

    @property
    def enable_cdc(self):
        """
        Indicates whether to enable Change Data Capture (CDC) or not on
        exported database.

        :rtype: ``bool``
        """
        return self._enable_cdc[0]

    @enable_cdc.setter
    def enable_cdc(self, value):
        self._enable_cdc = (value, True)

