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
#     /delphix-ase-db-container.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_26.web.objects.DatabaseContainer import DatabaseContainer
from delphixpy.v1_11_26 import factory
from delphixpy.v1_11_26 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ASEDBContainer(DatabaseContainer):
    """
    *(extends* :py:class:`v1_11_26.web.vo.DatabaseContainer` *)* An SAP ASE
    Database Container.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ASEDBContainer", True)
        self._os = (self.__undef__, True)
        self._processor = (self.__undef__, True)
        self._sourcing_policy = (self.__undef__, True)
        self._runtime = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._os = (data.get("os", obj.__undef__), dirty)
        if obj._os[0] is not None and obj._os[0] is not obj.__undef__:
            assert isinstance(obj._os[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._os[0], type(obj._os[0])))
            common.validate_format(obj._os[0], "None", None, None)
        obj._processor = (data.get("processor", obj.__undef__), dirty)
        if obj._processor[0] is not None and obj._processor[0] is not obj.__undef__:
            assert isinstance(obj._processor[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._processor[0], type(obj._processor[0])))
            common.validate_format(obj._processor[0], "None", None, None)
        if "sourcingPolicy" in data and data["sourcingPolicy"] is not None:
            obj._sourcing_policy = (factory.create_object(data["sourcingPolicy"], "SourcingPolicy"), dirty)
            factory.validate_type(obj._sourcing_policy[0], "SourcingPolicy")
        else:
            obj._sourcing_policy = (obj.__undef__, dirty)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "ASEDBContainerRuntime"), dirty)
            factory.validate_type(obj._runtime[0], "ASEDBContainerRuntime")
        else:
            obj._runtime = (obj.__undef__, dirty)
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
        if "os" == "type" or (self.os is not self.__undef__ and (not (dirty and not self._os[1]))):
            dct["os"] = dictify(self.os)
        if "processor" == "type" or (self.processor is not self.__undef__ and (not (dirty and not self._processor[1]))):
            dct["processor"] = dictify(self.processor)
        if "sourcing_policy" == "type" or (self.sourcing_policy is not self.__undef__ and (not (dirty and not self._sourcing_policy[1]) or self.is_dirty_list(self.sourcing_policy, self._sourcing_policy) or belongs_to_parent)):
            dct["sourcingPolicy"] = dictify(self.sourcing_policy, prop_is_list_or_vo=True)
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._os = (self._os[0], True)
        self._processor = (self._processor[0], True)
        self._sourcing_policy = (self._sourcing_policy[0], True)
        self._runtime = (self._runtime[0], True)

    def is_dirty(self):
        return any([self._os[1], self._processor[1], self._sourcing_policy[1], self._runtime[1]])

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
        if not isinstance(other, ASEDBContainer):
            return False
        return super().__eq__(other) and \
               self.os == other.os and \
               self.processor == other.processor and \
               self.sourcing_policy == other.sourcing_policy and \
               self.runtime == other.runtime

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def os(self):
        """
        The operating system for the source database.

        :rtype: ``str``
        """
        return self._os[0]

    @os.setter
    def os(self, value):
        self._os = (value, True)

    @property
    def processor(self):
        """
        The processor type for the source database.

        :rtype: ``str``
        """
        return self._processor[0]

    @processor.setter
    def processor(self, value):
        self._processor = (value, True)

    @property
    def sourcing_policy(self):
        """
        Policies for managing LogSync and SnapSync across sources for an SAP
        ASE container.

        :rtype: :py:class:`v1_11_26.web.vo.SourcingPolicy`
        """
        return self._sourcing_policy[0]

    @sourcing_policy.setter
    def sourcing_policy(self, value):
        self._sourcing_policy = (value, True)

    @property
    def runtime(self):
        """
        Runtime properties of this container.

        :rtype: :py:class:`v1_11_26.web.vo.ASEDBContainerRuntime`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

