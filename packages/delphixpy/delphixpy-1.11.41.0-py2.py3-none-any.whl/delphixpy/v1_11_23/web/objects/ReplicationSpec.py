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
#     /delphix-replicationspec.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_23.web.objects.UserObject import UserObject
from delphixpy.v1_11_23 import factory
from delphixpy.v1_11_23 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ReplicationSpec(UserObject):
    """
    *(extends* :py:class:`v1_11_23.web.vo.UserObject` *)* Replication setup.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ReplicationSpec", True)
        self._target_host = (self.__undef__, True)
        self._target_port = (self.__undef__, True)
        self._target_principal = (self.__undef__, True)
        self._target_credential = (self.__undef__, True)
        self._object_specification = (self.__undef__, True)
        self._schedule = (self.__undef__, True)
        self._automatic_replication = (self.__undef__, True)
        self._tag = (self.__undef__, True)
        self._encrypted = (self.__undef__, True)
        self._bandwidth_limit = (self.__undef__, True)
        self._number_of_connections = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._runtime = (self.__undef__, True)
        self._use_system_socks_setting = (self.__undef__, True)
        self._locked_profile = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._target_host = (data.get("targetHost", obj.__undef__), dirty)
        if obj._target_host[0] is not None and obj._target_host[0] is not obj.__undef__:
            assert isinstance(obj._target_host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_host[0], type(obj._target_host[0])))
            common.validate_format(obj._target_host[0], "host", None, None)
        obj._target_port = (data.get("targetPort", obj.__undef__), dirty)
        if obj._target_port[0] is not None and obj._target_port[0] is not obj.__undef__:
            assert isinstance(obj._target_port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._target_port[0], type(obj._target_port[0])))
            common.validate_format(obj._target_port[0], "None", None, None)
        obj._target_principal = (data.get("targetPrincipal", obj.__undef__), dirty)
        if obj._target_principal[0] is not None and obj._target_principal[0] is not obj.__undef__:
            assert isinstance(obj._target_principal[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_principal[0], type(obj._target_principal[0])))
            common.validate_format(obj._target_principal[0], "None", None, None)
        if "targetCredential" in data and data["targetCredential"] is not None:
            obj._target_credential = (factory.create_object(data["targetCredential"], "PasswordCredential"), dirty)
            factory.validate_type(obj._target_credential[0], "PasswordCredential")
        else:
            obj._target_credential = (obj.__undef__, dirty)
        if "objectSpecification" in data and data["objectSpecification"] is not None:
            obj._object_specification = (factory.create_object(data["objectSpecification"], "ReplicationObjectSpecification"), dirty)
            factory.validate_type(obj._object_specification[0], "ReplicationObjectSpecification")
        else:
            obj._object_specification = (obj.__undef__, dirty)
        obj._schedule = (data.get("schedule", obj.__undef__), dirty)
        if obj._schedule[0] is not None and obj._schedule[0] is not obj.__undef__:
            assert isinstance(obj._schedule[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._schedule[0], type(obj._schedule[0])))
            common.validate_format(obj._schedule[0], "None", 1, 256)
        obj._automatic_replication = (data.get("automaticReplication", obj.__undef__), dirty)
        if obj._automatic_replication[0] is not None and obj._automatic_replication[0] is not obj.__undef__:
            assert isinstance(obj._automatic_replication[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._automatic_replication[0], type(obj._automatic_replication[0])))
            common.validate_format(obj._automatic_replication[0], "None", None, None)
        obj._tag = (data.get("tag", obj.__undef__), dirty)
        if obj._tag[0] is not None and obj._tag[0] is not obj.__undef__:
            assert isinstance(obj._tag[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._tag[0], type(obj._tag[0])))
            common.validate_format(obj._tag[0], "None", 1, 256)
        obj._encrypted = (data.get("encrypted", obj.__undef__), dirty)
        if obj._encrypted[0] is not None and obj._encrypted[0] is not obj.__undef__:
            assert isinstance(obj._encrypted[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._encrypted[0], type(obj._encrypted[0])))
            common.validate_format(obj._encrypted[0], "None", None, None)
        obj._bandwidth_limit = (data.get("bandwidthLimit", obj.__undef__), dirty)
        if obj._bandwidth_limit[0] is not None and obj._bandwidth_limit[0] is not obj.__undef__:
            assert isinstance(obj._bandwidth_limit[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._bandwidth_limit[0], type(obj._bandwidth_limit[0])))
            common.validate_format(obj._bandwidth_limit[0], "None", None, None)
        obj._number_of_connections = (data.get("numberOfConnections", obj.__undef__), dirty)
        if obj._number_of_connections[0] is not None and obj._number_of_connections[0] is not obj.__undef__:
            assert isinstance(obj._number_of_connections[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._number_of_connections[0], type(obj._number_of_connections[0])))
            common.validate_format(obj._number_of_connections[0], "None", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, 4096)
        if "runtime" in data and data["runtime"] is not None:
            obj._runtime = (factory.create_object(data["runtime"], "ReplicationSpecRuntime"), dirty)
            factory.validate_type(obj._runtime[0], "ReplicationSpecRuntime")
        else:
            obj._runtime = (obj.__undef__, dirty)
        obj._use_system_socks_setting = (data.get("useSystemSocksSetting", obj.__undef__), dirty)
        if obj._use_system_socks_setting[0] is not None and obj._use_system_socks_setting[0] is not obj.__undef__:
            assert isinstance(obj._use_system_socks_setting[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._use_system_socks_setting[0], type(obj._use_system_socks_setting[0])))
            common.validate_format(obj._use_system_socks_setting[0], "None", None, None)
        obj._locked_profile = (data.get("lockedProfile", obj.__undef__), dirty)
        if obj._locked_profile[0] is not None and obj._locked_profile[0] is not obj.__undef__:
            assert isinstance(obj._locked_profile[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._locked_profile[0], type(obj._locked_profile[0])))
            common.validate_format(obj._locked_profile[0], "None", None, None)
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
        if "target_host" == "type" or (self.target_host is not self.__undef__ and (not (dirty and not self._target_host[1]) or self.is_dirty_list(self.target_host, self._target_host) or belongs_to_parent)):
            dct["targetHost"] = dictify(self.target_host)
        if "target_port" == "type" or (self.target_port is not self.__undef__ and (not (dirty and not self._target_port[1]) or self.is_dirty_list(self.target_port, self._target_port) or belongs_to_parent)):
            dct["targetPort"] = dictify(self.target_port)
        elif belongs_to_parent and self.target_port is self.__undef__:
            dct["targetPort"] = 8415
        if "target_principal" == "type" or (self.target_principal is not self.__undef__ and (not (dirty and not self._target_principal[1]) or self.is_dirty_list(self.target_principal, self._target_principal) or belongs_to_parent)):
            dct["targetPrincipal"] = dictify(self.target_principal)
        if "target_credential" == "type" or (self.target_credential is not self.__undef__ and (not (dirty and not self._target_credential[1]) or self.is_dirty_list(self.target_credential, self._target_credential) or belongs_to_parent)):
            dct["targetCredential"] = dictify(self.target_credential, prop_is_list_or_vo=True)
        if "object_specification" == "type" or (self.object_specification is not self.__undef__ and (not (dirty and not self._object_specification[1]) or self.is_dirty_list(self.object_specification, self._object_specification) or belongs_to_parent)):
            dct["objectSpecification"] = dictify(self.object_specification, prop_is_list_or_vo=True)
        if "schedule" == "type" or (self.schedule is not self.__undef__ and (not (dirty and not self._schedule[1]) or self.is_dirty_list(self.schedule, self._schedule) or belongs_to_parent)):
            dct["schedule"] = dictify(self.schedule)
        if "automatic_replication" == "type" or (self.automatic_replication is not self.__undef__ and (not (dirty and not self._automatic_replication[1]) or self.is_dirty_list(self.automatic_replication, self._automatic_replication) or belongs_to_parent)):
            dct["automaticReplication"] = dictify(self.automatic_replication)
        elif belongs_to_parent and self.automatic_replication is self.__undef__:
            dct["automaticReplication"] = False
        if "tag" == "type" or (self.tag is not self.__undef__ and (not (dirty and not self._tag[1]))):
            dct["tag"] = dictify(self.tag)
        if "encrypted" == "type" or (self.encrypted is not self.__undef__ and (not (dirty and not self._encrypted[1]) or self.is_dirty_list(self.encrypted, self._encrypted) or belongs_to_parent)):
            dct["encrypted"] = dictify(self.encrypted)
        elif belongs_to_parent and self.encrypted is self.__undef__:
            dct["encrypted"] = False
        if "bandwidth_limit" == "type" or (self.bandwidth_limit is not self.__undef__ and (not (dirty and not self._bandwidth_limit[1]) or self.is_dirty_list(self.bandwidth_limit, self._bandwidth_limit) or belongs_to_parent)):
            dct["bandwidthLimit"] = dictify(self.bandwidth_limit)
        elif belongs_to_parent and self.bandwidth_limit is self.__undef__:
            dct["bandwidthLimit"] = 0
        if "number_of_connections" == "type" or (self.number_of_connections is not self.__undef__ and (not (dirty and not self._number_of_connections[1]) or self.is_dirty_list(self.number_of_connections, self._number_of_connections) or belongs_to_parent)):
            dct["numberOfConnections"] = dictify(self.number_of_connections)
        elif belongs_to_parent and self.number_of_connections is self.__undef__:
            dct["numberOfConnections"] = 1
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]) or self.is_dirty_list(self.description, self._description) or belongs_to_parent)):
            dct["description"] = dictify(self.description)
        if "runtime" == "type" or (self.runtime is not self.__undef__ and (not (dirty and not self._runtime[1]))):
            dct["runtime"] = dictify(self.runtime)
        if "use_system_socks_setting" == "type" or (self.use_system_socks_setting is not self.__undef__ and (not (dirty and not self._use_system_socks_setting[1]) or self.is_dirty_list(self.use_system_socks_setting, self._use_system_socks_setting) or belongs_to_parent)):
            dct["useSystemSocksSetting"] = dictify(self.use_system_socks_setting)
        elif belongs_to_parent and self.use_system_socks_setting is self.__undef__:
            dct["useSystemSocksSetting"] = False
        if "locked_profile" == "type" or (self.locked_profile is not self.__undef__ and (not (dirty and not self._locked_profile[1]) or self.is_dirty_list(self.locked_profile, self._locked_profile) or belongs_to_parent)):
            dct["lockedProfile"] = dictify(self.locked_profile)
        elif belongs_to_parent and self.locked_profile is self.__undef__:
            dct["lockedProfile"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._target_host = (self._target_host[0], True)
        self._target_port = (self._target_port[0], True)
        self._target_principal = (self._target_principal[0], True)
        self._target_credential = (self._target_credential[0], True)
        self._object_specification = (self._object_specification[0], True)
        self._schedule = (self._schedule[0], True)
        self._automatic_replication = (self._automatic_replication[0], True)
        self._tag = (self._tag[0], True)
        self._encrypted = (self._encrypted[0], True)
        self._bandwidth_limit = (self._bandwidth_limit[0], True)
        self._number_of_connections = (self._number_of_connections[0], True)
        self._description = (self._description[0], True)
        self._runtime = (self._runtime[0], True)
        self._use_system_socks_setting = (self._use_system_socks_setting[0], True)
        self._locked_profile = (self._locked_profile[0], True)

    def is_dirty(self):
        return any([self._target_host[1], self._target_port[1], self._target_principal[1], self._target_credential[1], self._object_specification[1], self._schedule[1], self._automatic_replication[1], self._tag[1], self._encrypted[1], self._bandwidth_limit[1], self._number_of_connections[1], self._description[1], self._runtime[1], self._use_system_socks_setting[1], self._locked_profile[1]])

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
        if not isinstance(other, ReplicationSpec):
            return False
        return super().__eq__(other) and \
               self.target_host == other.target_host and \
               self.target_port == other.target_port and \
               self.target_principal == other.target_principal and \
               self.target_credential == other.target_credential and \
               self.object_specification == other.object_specification and \
               self.schedule == other.schedule and \
               self.automatic_replication == other.automatic_replication and \
               self.tag == other.tag and \
               self.encrypted == other.encrypted and \
               self.bandwidth_limit == other.bandwidth_limit and \
               self.number_of_connections == other.number_of_connections and \
               self.description == other.description and \
               self.runtime == other.runtime and \
               self.use_system_socks_setting == other.use_system_socks_setting and \
               self.locked_profile == other.locked_profile

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def target_host(self):
        """
        Replication target host address.

        :rtype: ``str``
        """
        return self._target_host[0]

    @target_host.setter
    def target_host(self, value):
        self._target_host = (value, True)

    @property
    def target_port(self):
        """
        *(default value: 8415)* Target TCP port number for the Delphix Session
        Protocol.

        :rtype: ``int``
        """
        return self._target_port[0]

    @target_port.setter
    def target_port(self, value):
        self._target_port = (value, True)

    @property
    def target_principal(self):
        """
        Principal name used to authenticate to the replication target host.

        :rtype: ``str``
        """
        return self._target_principal[0]

    @target_principal.setter
    def target_principal(self, value):
        self._target_principal = (value, True)

    @property
    def target_credential(self):
        """
        Credential used to authenticate to the replication target host.

        :rtype: :py:class:`v1_11_23.web.vo.PasswordCredential`
        """
        return self._target_credential[0]

    @target_credential.setter
    def target_credential(self, value):
        self._target_credential = (value, True)

    @property
    def object_specification(self):
        """
        Specification of the objects to replicate.

        :rtype: :py:class:`v1_11_23.web.vo.ReplicationObjectSpecification`
        """
        return self._object_specification[0]

    @object_specification.setter
    def object_specification(self, value):
        self._object_specification = (value, True)

    @property
    def schedule(self):
        """
        Replication schedule in the form of a quartz-formatted string.

        :rtype: ``str`` *or* ``null``
        """
        return self._schedule[0]

    @schedule.setter
    def schedule(self, value):
        self._schedule = (value, True)

    @property
    def automatic_replication(self):
        """
        Indication whether the replication spec schedule is enabled or not.

        :rtype: ``bool``
        """
        return self._automatic_replication[0]

    @automatic_replication.setter
    def automatic_replication(self, value):
        self._automatic_replication = (value, True)

    @property
    def tag(self):
        """
        Globally unique identifier for this replication spec.

        :rtype: ``str``
        """
        return self._tag[0]

    @tag.setter
    def tag(self, value):
        self._tag = (value, True)

    @property
    def encrypted(self):
        """
        Encrypt replication network traffic.

        :rtype: ``bool``
        """
        return self._encrypted[0]

    @encrypted.setter
    def encrypted(self, value):
        self._encrypted = (value, True)

    @property
    def bandwidth_limit(self):
        """
        Bandwidth limit (MB/s) for replication network traffic. A value of 0
        means no limit.

        :rtype: ``int``
        """
        return self._bandwidth_limit[0]

    @bandwidth_limit.setter
    def bandwidth_limit(self, value):
        self._bandwidth_limit = (value, True)

    @property
    def number_of_connections(self):
        """
        *(default value: 1)* Total number of transport connections to use.

        :rtype: ``int``
        """
        return self._number_of_connections[0]

    @number_of_connections.setter
    def number_of_connections(self, value):
        self._number_of_connections = (value, True)

    @property
    def description(self):
        """
        Description of this replication spec.

        :rtype: ``str`` *or* ``null``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def runtime(self):
        """
        Runtime properties of this replication spec.

        :rtype: :py:class:`v1_11_23.web.vo.ReplicationSpecRuntime`
        """
        return self._runtime[0]

    @runtime.setter
    def runtime(self, value):
        self._runtime = (value, True)

    @property
    def use_system_socks_setting(self):
        """
        Connect to the replication target host via the system-wide SOCKS proxy.

        :rtype: ``bool``
        """
        return self._use_system_socks_setting[0]

    @use_system_socks_setting.setter
    def use_system_socks_setting(self, value):
        self._use_system_socks_setting = (value, True)

    @property
    def locked_profile(self):
        """
        Indicates the replication profile is locked.

        :rtype: ``bool``
        """
        return self._locked_profile[0]

    @locked_profile.setter
    def locked_profile(self, value):
        self._locked_profile = (value, True)

