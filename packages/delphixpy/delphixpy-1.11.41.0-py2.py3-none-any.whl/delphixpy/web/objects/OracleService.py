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
#     /delphix-oracle-service.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.TypedObject import TypedObject
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleService(TypedObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.TypedObject` *)* The representation
    of an oracle service object.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleService", True)
        self._jdbc_connection_string = (self.__undef__, True)
        self._discovered = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._jdbc_connection_string = (data.get("jdbcConnectionString", obj.__undef__), dirty)
        if obj._jdbc_connection_string[0] is not None and obj._jdbc_connection_string[0] is not obj.__undef__:
            assert isinstance(obj._jdbc_connection_string[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._jdbc_connection_string[0], type(obj._jdbc_connection_string[0])))
            common.validate_format(obj._jdbc_connection_string[0], "oracleJDBCConnectionString", None, None)
        obj._discovered = (data.get("discovered", obj.__undef__), dirty)
        if obj._discovered[0] is not None and obj._discovered[0] is not obj.__undef__:
            assert isinstance(obj._discovered[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._discovered[0], type(obj._discovered[0])))
            common.validate_format(obj._discovered[0], "None", None, None)
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
        if "jdbc_connection_string" == "type" or (self.jdbc_connection_string is not self.__undef__ and (not (dirty and not self._jdbc_connection_string[1]) or self.is_dirty_list(self.jdbc_connection_string, self._jdbc_connection_string) or belongs_to_parent)):
            dct["jdbcConnectionString"] = dictify(self.jdbc_connection_string)
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._jdbc_connection_string = (self._jdbc_connection_string[0], True)
        self._discovered = (self._discovered[0], True)

    def is_dirty(self):
        return any([self._jdbc_connection_string[1], self._discovered[1]])

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
        if not isinstance(other, OracleService):
            return False
        return super().__eq__(other) and \
               self.jdbc_connection_string == other.jdbc_connection_string and \
               self.discovered == other.discovered

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def jdbc_connection_string(self):
        """
        The connection string used to connect to JDBC.

        :rtype: ``str``
        """
        return self._jdbc_connection_string[0]

    @jdbc_connection_string.setter
    def jdbc_connection_string(self, value):
        self._jdbc_connection_string = (value, True)

    @property
    def discovered(self):
        """
        Whether this service was automatically discovered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

