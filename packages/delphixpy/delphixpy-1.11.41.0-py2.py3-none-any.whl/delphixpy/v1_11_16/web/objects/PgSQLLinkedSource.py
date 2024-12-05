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
#     /delphix-pgsql-linked-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_16.web.objects.PgSQLSource import PgSQLSource
from delphixpy.v1_11_16 import factory
from delphixpy.v1_11_16 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class PgSQLLinkedSource(PgSQLSource):
    """
    *(extends* :py:class:`v1_11_16.web.vo.PgSQLSource` *)* A linked PostgreSQL
    source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("PgSQLLinkedSource", True)
        self._external_file_path = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._staging_source = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._external_file_path = (data.get("externalFilePath", obj.__undef__), dirty)
        if obj._external_file_path[0] is not None and obj._external_file_path[0] is not obj.__undef__:
            assert isinstance(obj._external_file_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._external_file_path[0], type(obj._external_file_path[0])))
            common.validate_format(obj._external_file_path[0], "None", None, 1024)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "LinkedSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "LinkedSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        obj._staging_source = (data.get("stagingSource", obj.__undef__), dirty)
        if obj._staging_source[0] is not None and obj._staging_source[0] is not obj.__undef__:
            assert isinstance(obj._staging_source[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_source[0], type(obj._staging_source[0])))
            common.validate_format(obj._staging_source[0], "objectReference", None, None)
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
        if "external_file_path" == "type" or (self.external_file_path is not self.__undef__ and (not (dirty and not self._external_file_path[1]) or self.is_dirty_list(self.external_file_path, self._external_file_path) or belongs_to_parent)):
            dct["externalFilePath"] = dictify(self.external_file_path)
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "staging_source" == "type" or (self.staging_source is not self.__undef__ and (not (dirty and not self._staging_source[1]))):
            dct["stagingSource"] = dictify(self.staging_source)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._external_file_path = (self._external_file_path[0], True)
        self._operations = (self._operations[0], True)
        self._staging_source = (self._staging_source[0], True)

    def is_dirty(self):
        return any([self._external_file_path[1], self._operations[1], self._staging_source[1]])

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
        if not isinstance(other, PgSQLLinkedSource):
            return False
        return super().__eq__(other) and \
               self.external_file_path == other.external_file_path and \
               self.operations == other.operations and \
               self.staging_source == other.staging_source

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def external_file_path(self):
        """
        The external file path.

        :rtype: ``str``
        """
        return self._external_file_path[0]

    @external_file_path.setter
    def external_file_path(self, value):
        self._external_file_path = (value, True)

    @property
    def operations(self):
        """
        User-specified operation hooks for this source.

        :rtype: :py:class:`v1_11_16.web.vo.LinkedSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

    @property
    def staging_source(self):
        """
        The staging source for pre-provisioning of the database.

        :rtype: ``str``
        """
        return self._staging_source[0]

    @staging_source.setter
    def staging_source(self, value):
        self._staging_source = (value, True)

