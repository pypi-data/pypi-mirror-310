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
#     /delphix-appdata-container.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_30.web.objects.DatabaseContainer import DatabaseContainer
from delphixpy.v1_11_30 import factory
from delphixpy.v1_11_30 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AppDataContainer(DatabaseContainer):
    """
    *(extends* :py:class:`v1_11_30.web.vo.DatabaseContainer` *)* Data container
    for AppData.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AppDataContainer", True)
        self._runtime = (self.__undef__, True)
        self._toolkit = (self.__undef__, True)
        self._guid = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "AppDataContainerRuntime"), dirty)
            factory.validate_type(obj._runtime[0], "AppDataContainerRuntime")
        else:
            obj._runtime = (obj.__undef__, dirty)
        obj._toolkit = (data.get("toolkit", obj.__undef__), dirty)
        if obj._toolkit[0] is not None and obj._toolkit[0] is not obj.__undef__:
            assert isinstance(obj._toolkit[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._toolkit[0], type(obj._toolkit[0])))
            common.validate_format(obj._toolkit[0], "None", None, None)
        obj._guid = (data.get("guid", obj.__undef__), dirty)
        if obj._guid[0] is not None and obj._guid[0] is not obj.__undef__:
            assert isinstance(obj._guid[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._guid[0], type(obj._guid[0])))
            common.validate_format(obj._guid[0], "None", None, None)
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
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        if "toolkit" == "type" or (self.toolkit is not self.__undef__ and (not (dirty and not self._toolkit[1]))):
            dct["toolkit"] = dictify(self.toolkit)
        if "guid" == "type" or (self.guid is not self.__undef__ and (not (dirty and not self._guid[1]))):
            dct["guid"] = dictify(self.guid)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._runtime = (self._runtime[0], True)
        self._toolkit = (self._toolkit[0], True)
        self._guid = (self._guid[0], True)

    def is_dirty(self):
        return any([self._runtime[1], self._toolkit[1], self._guid[1]])

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
        if not isinstance(other, AppDataContainer):
            return False
        return super().__eq__(other) and \
               self.runtime == other.runtime and \
               self.toolkit == other.toolkit and \
               self.guid == other.guid

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def runtime(self):
        """
        Runtime properties of this container.

        :rtype: :py:class:`v1_11_30.web.vo.AppDataContainerRuntime`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

    @property
    def toolkit(self):
        """
        The toolkit managing the data in the container.

        :rtype: ``str``
        """
        return self._toolkit[0]

    @toolkit.setter
    def toolkit(self, value):
        self._toolkit = (value, True)

    @property
    def guid(self):
        """
        A global identifier for this container, including across Delphix
        Engines.

        :rtype: ``str``
        """
        return self._guid[0]

    @guid.setter
    def guid(self, value):
        self._guid = (value, True)

