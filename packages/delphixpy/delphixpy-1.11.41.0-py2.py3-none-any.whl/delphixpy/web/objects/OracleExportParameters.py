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
#     /delphix-oracle-export-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.DbExportParameters import DbExportParameters
from delphixpy import factory
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleExportParameters(DbExportParameters):
    """
    *(extends* :py:class:`delphixpy.web.vo.DbExportParameters` *)* The
    parameters to use as input to export Oracle databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleExportParameters", True)
        self._source_config = (self.__undef__, True)
        self._open_database = (self.__undef__, True)
        self._file_parallelism = (self.__undef__, True)
        self._dsp_options = (self.__undef__, True)
        self._filesystem_layout = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "sourceConfig" not in data:
            raise ValueError("Missing required property \"sourceConfig\".")
        if "sourceConfig" in data and data["sourceConfig"] is not None:
            obj._source_config = (factory.create_object(data["sourceConfig"], "OracleDBConfig"), dirty)
            factory.validate_type(obj._source_config[0], "OracleDBConfig")
        else:
            obj._source_config = (obj.__undef__, dirty)
        obj._open_database = (data.get("openDatabase", obj.__undef__), dirty)
        if obj._open_database[0] is not None and obj._open_database[0] is not obj.__undef__:
            assert isinstance(obj._open_database[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._open_database[0], type(obj._open_database[0])))
            common.validate_format(obj._open_database[0], "None", None, None)
        obj._file_parallelism = (data.get("fileParallelism", obj.__undef__), dirty)
        if obj._file_parallelism[0] is not None and obj._file_parallelism[0] is not obj.__undef__:
            assert isinstance(obj._file_parallelism[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._file_parallelism[0], type(obj._file_parallelism[0])))
            common.validate_format(obj._file_parallelism[0], "None", None, None)
        if "dspOptions" in data and data["dspOptions"] is not None:
            obj._dsp_options = (factory.create_object(data["dspOptions"], "DSPOptions"), dirty)
            factory.validate_type(obj._dsp_options[0], "DSPOptions")
        else:
            obj._dsp_options = (obj.__undef__, dirty)
        if "filesystemLayout" not in data:
            raise ValueError("Missing required property \"filesystemLayout\".")
        if "filesystemLayout" in data and data["filesystemLayout"] is not None:
            obj._filesystem_layout = (factory.create_object(data["filesystemLayout"], "OracleExportTimeflowFilesystemLayout"), dirty)
            factory.validate_type(obj._filesystem_layout[0], "OracleExportTimeflowFilesystemLayout")
        else:
            obj._filesystem_layout = (obj.__undef__, dirty)
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
        if "open_database" == "type" or (self.open_database is not self.__undef__ and (not (dirty and not self._open_database[1]) or self.is_dirty_list(self.open_database, self._open_database) or belongs_to_parent)):
            dct["openDatabase"] = dictify(self.open_database)
        elif belongs_to_parent and self.open_database is self.__undef__:
            dct["openDatabase"] = True
        if "file_parallelism" == "type" or (self.file_parallelism is not self.__undef__ and (not (dirty and not self._file_parallelism[1]) or self.is_dirty_list(self.file_parallelism, self._file_parallelism) or belongs_to_parent)):
            dct["fileParallelism"] = dictify(self.file_parallelism)
        elif belongs_to_parent and self.file_parallelism is self.__undef__:
            dct["fileParallelism"] = 3
        if "dsp_options" == "type" or (self.dsp_options is not self.__undef__ and (not (dirty and not self._dsp_options[1]) or self.is_dirty_list(self.dsp_options, self._dsp_options) or belongs_to_parent)):
            dct["dspOptions"] = dictify(self.dsp_options, prop_is_list_or_vo=True)
        if "filesystem_layout" == "type" or (self.filesystem_layout is not self.__undef__ and (not (dirty and not self._filesystem_layout[1]) or self.is_dirty_list(self.filesystem_layout, self._filesystem_layout) or belongs_to_parent)):
            dct["filesystemLayout"] = dictify(self.filesystem_layout, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._source_config = (self._source_config[0], True)
        self._open_database = (self._open_database[0], True)
        self._file_parallelism = (self._file_parallelism[0], True)
        self._dsp_options = (self._dsp_options[0], True)
        self._filesystem_layout = (self._filesystem_layout[0], True)

    def is_dirty(self):
        return any([self._source_config[1], self._open_database[1], self._file_parallelism[1], self._dsp_options[1], self._filesystem_layout[1]])

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
        if not isinstance(other, OracleExportParameters):
            return False
        return super().__eq__(other) and \
               self.source_config == other.source_config and \
               self.open_database == other.open_database and \
               self.file_parallelism == other.file_parallelism and \
               self.dsp_options == other.dsp_options and \
               self.filesystem_layout == other.filesystem_layout

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

        :rtype: :py:class:`delphixpy.web.vo.OracleDBConfig`
        """
        return self._source_config[0]

    @source_config.setter
    def source_config(self, value):
        self._source_config = (value, True)

    @property
    def open_database(self):
        """
        *(default value: True)* Open the database after recovery. This can have
        a true value only if 'recoverDatabase' is true.

        :rtype: ``bool``
        """
        return self._open_database[0]

    @open_database.setter
    def open_database(self, value):
        self._open_database = (value, True)

    @property
    def file_parallelism(self):
        """
        *(default value: 3)* Number of files to stream in parallel across the
        network.

        :rtype: ``int``
        """
        return self._file_parallelism[0]

    @file_parallelism.setter
    def file_parallelism(self, value):
        self._file_parallelism = (value, True)

    @property
    def dsp_options(self):
        """
        DSP options for export.

        :rtype: :py:class:`delphixpy.web.vo.DSPOptions`
        """
        return self._dsp_options[0]

    @dsp_options.setter
    def dsp_options(self, value):
        self._dsp_options = (value, True)

    @property
    def filesystem_layout(self):
        """
        The filesystem configuration of the exported database.

        :rtype:
            :py:class:`delphixpy.web.vo.OracleExportTimeflowFilesystemLayout`
        """
        return self._filesystem_layout[0]

    @filesystem_layout.setter
    def filesystem_layout(self, value):
        self._filesystem_layout = (value, True)

