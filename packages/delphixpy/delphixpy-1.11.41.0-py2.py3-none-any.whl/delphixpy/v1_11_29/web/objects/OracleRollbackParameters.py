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
#     /delphix-oracle-rollback-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_29.web.objects.RollbackParameters import RollbackParameters
from delphixpy.v1_11_29 import factory
from delphixpy.v1_11_29 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleRollbackParameters(RollbackParameters):
    """
    *(extends* :py:class:`v1_11_29.web.vo.RollbackParameters` *)* The
    parameters to use as input to roll back Oracle databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleRollbackParameters", True)
        self._username = (self.__undef__, True)
        self._credential = (self.__undef__, True)
        self._force = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._username = (data.get("username", obj.__undef__), dirty)
        if obj._username[0] is not None and obj._username[0] is not obj.__undef__:
            assert isinstance(obj._username[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._username[0], type(obj._username[0])))
            common.validate_format(obj._username[0], "None", None, None)
        if "credential" in data and data["credential"] is not None:
            obj._credential = (factory.create_object(data["credential"], "Credential"), dirty)
            factory.validate_type(obj._credential[0], "Credential")
        else:
            obj._credential = (obj.__undef__, dirty)
        obj._force = (data.get("force", obj.__undef__), dirty)
        if obj._force[0] is not None and obj._force[0] is not obj.__undef__:
            assert isinstance(obj._force[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._force[0], type(obj._force[0])))
            common.validate_format(obj._force[0], "None", None, None)
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
        if "username" == "type" or (self.username is not self.__undef__ and (not (dirty and not self._username[1]))):
            dct["username"] = dictify(self.username)
        if "credential" == "type" or (self.credential is not self.__undef__ and (not (dirty and not self._credential[1]))):
            dct["credential"] = dictify(self.credential)
        if "force" == "type" or (self.force is not self.__undef__ and (not (dirty and not self._force[1]) or self.is_dirty_list(self.force, self._force) or belongs_to_parent)):
            dct["force"] = dictify(self.force)
        elif belongs_to_parent and self.force is self.__undef__:
            dct["force"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._username = (self._username[0], True)
        self._credential = (self._credential[0], True)
        self._force = (self._force[0], True)

    def is_dirty(self):
        return any([self._username[1], self._credential[1], self._force[1]])

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
        if not isinstance(other, OracleRollbackParameters):
            return False
        return super().__eq__(other) and \
               self.username == other.username and \
               self.credential == other.credential and \
               self.force == other.force

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def username(self):
        """
        The name of the user who has the required privileges to perform the
        rollback operation.

        :rtype: ``str``
        """
        return self._username[0]

    @username.setter
    def username(self, value):
        self._username = (value, True)

    @property
    def credential(self):
        """
        The security credential of the user who has the required privileges to
        run the rollback operation.

        :rtype: :py:class:`v1_11_29.web.vo.Credential`
        """
        return self._credential[0]

    @credential.setter
    def credential(self, value):
        self._credential = (value, True)

    @property
    def force(self):
        """
        Whether to offline drop vPDB in case unplug fails.

        :rtype: ``bool``
        """
        return self._force[0]

    @force.setter
    def force(self, value):
        self._force = (value, True)

