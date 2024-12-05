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
#     /delphix-source-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.ReadonlyNamedUserObject import ReadonlyNamedUserObject
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SourceConfig(ReadonlyNamedUserObject):
    """
    *(extends* :py:class:`v1_11_14.web.vo.ReadonlyNamedUserObject` *)* The
    source config represents the dynamically discovered attributes of a source.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SourceConfig", True)
        self._linking_enabled = (self.__undef__, True)
        self._discovered = (self.__undef__, True)
        self._environment_user = (self.__undef__, True)
        self._repository = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._linking_enabled = (data.get("linkingEnabled", obj.__undef__), dirty)
        if obj._linking_enabled[0] is not None and obj._linking_enabled[0] is not obj.__undef__:
            assert isinstance(obj._linking_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._linking_enabled[0], type(obj._linking_enabled[0])))
            common.validate_format(obj._linking_enabled[0], "None", None, None)
        obj._discovered = (data.get("discovered", obj.__undef__), dirty)
        if obj._discovered[0] is not None and obj._discovered[0] is not obj.__undef__:
            assert isinstance(obj._discovered[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._discovered[0], type(obj._discovered[0])))
            common.validate_format(obj._discovered[0], "None", None, None)
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
        if "linking_enabled" == "type" or (self.linking_enabled is not self.__undef__ and (not (dirty and not self._linking_enabled[1]) or self.is_dirty_list(self.linking_enabled, self._linking_enabled) or belongs_to_parent)):
            dct["linkingEnabled"] = dictify(self.linking_enabled)
        elif belongs_to_parent and self.linking_enabled is self.__undef__:
            dct["linkingEnabled"] = True
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        if "environment_user" == "type" or (self.environment_user is not self.__undef__ and (not (dirty and not self._environment_user[1]) or self.is_dirty_list(self.environment_user, self._environment_user) or belongs_to_parent)):
            dct["environmentUser"] = dictify(self.environment_user)
        if "repository" == "type" or (self.repository is not self.__undef__ and (not (dirty and not self._repository[1]) or self.is_dirty_list(self.repository, self._repository) or belongs_to_parent)):
            dct["repository"] = dictify(self.repository)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._linking_enabled = (self._linking_enabled[0], True)
        self._discovered = (self._discovered[0], True)
        self._environment_user = (self._environment_user[0], True)
        self._repository = (self._repository[0], True)

    def is_dirty(self):
        return any([self._linking_enabled[1], self._discovered[1], self._environment_user[1], self._repository[1]])

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
        if not isinstance(other, SourceConfig):
            return False
        return super().__eq__(other) and \
               self.linking_enabled == other.linking_enabled and \
               self.discovered == other.discovered and \
               self.environment_user == other.environment_user and \
               self.repository == other.repository

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def linking_enabled(self):
        """
        *(default value: True)* Whether this source should be used for linking.

        :rtype: ``bool``
        """
        return self._linking_enabled[0]

    @linking_enabled.setter
    def linking_enabled(self, value):
        self._linking_enabled = (value, True)

    @property
    def discovered(self):
        """
        Whether this source was discovered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

    @property
    def environment_user(self):
        """
        The user used to create and manage the configuration.

        :rtype: ``str``
        """
        return self._environment_user[0]

    @environment_user.setter
    def environment_user(self, value):
        self._environment_user = (value, True)

    @property
    def repository(self):
        """
        The object reference of the source repository.

        :rtype: ``str``
        """
        return self._repository[0]

    @repository.setter
    def repository(self, value):
        self._repository = (value, True)

