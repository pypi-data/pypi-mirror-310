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
#     /delphix-connectivity-mssql-db-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_9.web.objects.AbstractSourceConfigConnectivity import AbstractSourceConfigConnectivity
from delphixpy.v1_11_9 import factory
from delphixpy.v1_11_9 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlSourceConfigConnectivity(AbstractSourceConfigConnectivity):
    """
    *(extends* :py:class:`v1_11_9.web.vo.AbstractSourceConfigConnectivity` *)*
    Mechanism to test JDBC connectivity to MSSQL source configs.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlSourceConfigConnectivity", True)
        self._mssql_user = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "mssqlUser" not in data:
            raise ValueError("Missing required property \"mssqlUser\".")
        if "mssqlUser" in data and data["mssqlUser"] is not None:
            obj._mssql_user = (factory.create_object(data["mssqlUser"], "MSSqlUser"), dirty)
            factory.validate_type(obj._mssql_user[0], "MSSqlUser")
        else:
            obj._mssql_user = (obj.__undef__, dirty)
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
        if "mssql_user" == "type" or (self.mssql_user is not self.__undef__ and (not (dirty and not self._mssql_user[1]) or self.is_dirty_list(self.mssql_user, self._mssql_user) or belongs_to_parent)):
            dct["mssqlUser"] = dictify(self.mssql_user, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._mssql_user = (self._mssql_user[0], True)

    def is_dirty(self):
        return any([self._mssql_user[1]])

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
        if not isinstance(other, MSSqlSourceConfigConnectivity):
            return False
        return super().__eq__(other) and \
               self.mssql_user == other.mssql_user

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def mssql_user(self):
        """
        Information about the mssql user for linking.

        :rtype: :py:class:`v1_11_9.web.vo.MSSqlUser`
        """
        return self._mssql_user[0]

    @mssql_user.setter
    def mssql_user(self, value):
        self._mssql_user = (value, True)

