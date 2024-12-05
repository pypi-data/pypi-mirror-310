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
#     /delphix-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_38.web.objects.UserObject import UserObject
from delphixpy.v1_11_38 import factory
from delphixpy.v1_11_38 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Source(UserObject):
    """
    *(extends* :py:class:`v1_11_38.web.vo.UserObject` *)* A source represents
    an external database instance outside the Delphix system.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Source", True)
        self._description = (self.__undef__, True)
        self._linked = (self.__undef__, True)
        self._virtual = (self.__undef__, True)
        self._staging = (self.__undef__, True)
        self._replica = (self.__undef__, True)
        self._container = (self.__undef__, True)
        self._status = (self.__undef__, True)
        self._runtime = (self.__undef__, True)
        self._hosts = (self.__undef__, True)
        self._log_collection_enabled = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        obj._linked = (data.get("linked", obj.__undef__), dirty)
        if obj._linked[0] is not None and obj._linked[0] is not obj.__undef__:
            assert isinstance(obj._linked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._linked[0], type(obj._linked[0])))
            common.validate_format(obj._linked[0], "None", None, None)
        obj._virtual = (data.get("virtual", obj.__undef__), dirty)
        if obj._virtual[0] is not None and obj._virtual[0] is not obj.__undef__:
            assert isinstance(obj._virtual[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._virtual[0], type(obj._virtual[0])))
            common.validate_format(obj._virtual[0], "None", None, None)
        obj._staging = (data.get("staging", obj.__undef__), dirty)
        if obj._staging[0] is not None and obj._staging[0] is not obj.__undef__:
            assert isinstance(obj._staging[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._staging[0], type(obj._staging[0])))
            common.validate_format(obj._staging[0], "None", None, None)
        obj._replica = (data.get("replica", obj.__undef__), dirty)
        if obj._replica[0] is not None and obj._replica[0] is not obj.__undef__:
            assert isinstance(obj._replica[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._replica[0], type(obj._replica[0])))
            common.validate_format(obj._replica[0], "None", None, None)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "objectReference", None, None)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            assert obj._status[0] in ['DEFAULT', 'PENDING_UPGRADE'], "Expected enum ['DEFAULT', 'PENDING_UPGRADE'] but got %s" % obj._status[0]
            common.validate_format(obj._status[0], "None", None, None)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "SourceRuntime"), dirty)
            factory.validate_type(obj._runtime[0], "SourceRuntime")
        else:
            obj._runtime = (obj.__undef__, dirty)
        obj._hosts = []
        for item in data.get("hosts") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "objectReference", None, None)
            obj._hosts.append(item)
        obj._hosts = (obj._hosts, dirty)
        obj._log_collection_enabled = (data.get("logCollectionEnabled", obj.__undef__), dirty)
        if obj._log_collection_enabled[0] is not None and obj._log_collection_enabled[0] is not obj.__undef__:
            assert isinstance(obj._log_collection_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._log_collection_enabled[0], type(obj._log_collection_enabled[0])))
            common.validate_format(obj._log_collection_enabled[0], "None", None, None)
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
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]))):
            dct["description"] = dictify(self.description)
        if "linked" == "type" or (self.linked is not self.__undef__ and (not (dirty and not self._linked[1]))):
            dct["linked"] = dictify(self.linked)
        if "virtual" == "type" or (self.virtual is not self.__undef__ and (not (dirty and not self._virtual[1]))):
            dct["virtual"] = dictify(self.virtual)
        if "staging" == "type" or (self.staging is not self.__undef__ and (not (dirty and not self._staging[1]))):
            dct["staging"] = dictify(self.staging)
        if "replica" == "type" or (self.replica is not self.__undef__ and (not (dirty and not self._replica[1]))):
            dct["replica"] = dictify(self.replica)
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]))):
            dct["container"] = dictify(self.container)
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        if "hosts" == "type" or (self.hosts is not self.__undef__ and (not (dirty and not self._hosts[1]))):
            dct["hosts"] = dictify(self.hosts)
        if "log_collection_enabled" == "type" or (self.log_collection_enabled is not self.__undef__ and (not (dirty and not self._log_collection_enabled[1]) or self.is_dirty_list(self.log_collection_enabled, self._log_collection_enabled) or belongs_to_parent)):
            dct["logCollectionEnabled"] = dictify(self.log_collection_enabled)
        elif belongs_to_parent and self.log_collection_enabled is self.__undef__:
            dct["logCollectionEnabled"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._description = (self._description[0], True)
        self._linked = (self._linked[0], True)
        self._virtual = (self._virtual[0], True)
        self._staging = (self._staging[0], True)
        self._replica = (self._replica[0], True)
        self._container = (self._container[0], True)
        self._status = (self._status[0], True)
        self._runtime = (self._runtime[0], True)
        self._hosts = (self._hosts[0], True)
        self._log_collection_enabled = (self._log_collection_enabled[0], True)

    def is_dirty(self):
        return any([self._description[1], self._linked[1], self._virtual[1], self._staging[1], self._replica[1], self._container[1], self._status[1], self._runtime[1], self._hosts[1], self._log_collection_enabled[1]])

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
        if not isinstance(other, Source):
            return False
        return super().__eq__(other) and \
               self.description == other.description and \
               self.linked == other.linked and \
               self.virtual == other.virtual and \
               self.staging == other.staging and \
               self.replica == other.replica and \
               self.container == other.container and \
               self.status == other.status and \
               self.runtime == other.runtime and \
               self.hosts == other.hosts and \
               self.log_collection_enabled == other.log_collection_enabled

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def description(self):
        """
        A user-provided description of the source.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def linked(self):
        """
        Flag indicating whether the source is a linked source in the Delphix
        system.

        :rtype: ``bool``
        """
        return self._linked[0]

    @linked.setter
    def linked(self, value):
        self._linked = (value, True)

    @property
    def virtual(self):
        """
        Flag indicating whether the source is a virtual source in the Delphix
        system.

        :rtype: ``bool``
        """
        return self._virtual[0]

    @virtual.setter
    def virtual(self, value):
        self._virtual = (value, True)

    @property
    def staging(self):
        """
        Flag indicating whether the source is used as a staging source for pre-
        provisioning. Staging sources are managed by the Delphix system.

        :rtype: ``bool``
        """
        return self._staging[0]

    @staging.setter
    def staging(self, value):
        self._staging = (value, True)

    @property
    def replica(self):
        """
        Flag indicating whether the source is a replica source in the Delphix
        system.

        :rtype: ``bool``
        """
        return self._replica[0]

    @replica.setter
    def replica(self, value):
        self._replica = (value, True)

    @property
    def container(self):
        """
        Reference to the container being fed by this source, if any.

        :rtype: ``str``
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def status(self):
        """
        Status of this source. *(permitted values: DEFAULT, PENDING_UPGRADE)*

        :rtype: ``str``
        """
        return self._status[0]

    @status.setter
    def status(self, value):
        self._status = (value, True)

    @property
    def runtime(self):
        """
        Runtime properties of this source.

        :rtype: :py:class:`v1_11_38.web.vo.SourceRuntime`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

    @property
    def hosts(self):
        """
        Hosts that might affect operations on this source. Property will be
        null unless the includeHosts parameter is set when listing sources.

        :rtype: ``list`` of ``str``
        """
        return self._hosts[0]

    @hosts.setter
    def hosts(self, value):
        self._hosts = (value, True)

    @property
    def log_collection_enabled(self):
        """
        Flag indicating whether it is allowed to collect logs, potentially
        containing sensitive information, related to this source.

        :rtype: ``bool``
        """
        return self._log_collection_enabled[0]

    @log_collection_enabled.setter
    def log_collection_enabled(self, value):
        self._log_collection_enabled = (value, True)

