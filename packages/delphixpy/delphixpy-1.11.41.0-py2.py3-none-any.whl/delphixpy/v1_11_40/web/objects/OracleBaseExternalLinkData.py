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
#     /delphix-oracle-base-external-link-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.OracleBaseLinkData import OracleBaseLinkData
from delphixpy.v1_11_40 import factory
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleBaseExternalLinkData(OracleBaseLinkData):
    """
    *(extends* :py:class:`v1_11_40.web.vo.OracleBaseLinkData` *)* Represents
    common parameters to link all externally managed Oracle databases.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleBaseExternalLinkData", True)
        self._sync_strategy = (self.__undef__, True)
        self._diagnose_no_logging_faults = (self.__undef__, True)
        self._pre_provisioning_enabled = (self.__undef__, True)
        self._link_now = (self.__undef__, True)
        self._environment_user = (self.__undef__, True)
        self._oracle_fallback_user = (self.__undef__, True)
        self._oracle_fallback_credentials = (self.__undef__, True)
        self._sync_parameters = (self.__undef__, True)
        self._sourcing_policy = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "syncStrategy" in data and data["syncStrategy"] is not None:
            obj._sync_strategy = (factory.create_object(data["syncStrategy"], "OracleSourceBasedSyncStrategy"), dirty)
            factory.validate_type(obj._sync_strategy[0], "OracleSourceBasedSyncStrategy")
        else:
            obj._sync_strategy = (obj.__undef__, dirty)
        obj._diagnose_no_logging_faults = (data.get("diagnoseNoLoggingFaults", obj.__undef__), dirty)
        if obj._diagnose_no_logging_faults[0] is not None and obj._diagnose_no_logging_faults[0] is not obj.__undef__:
            assert isinstance(obj._diagnose_no_logging_faults[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._diagnose_no_logging_faults[0], type(obj._diagnose_no_logging_faults[0])))
            common.validate_format(obj._diagnose_no_logging_faults[0], "None", None, None)
        obj._pre_provisioning_enabled = (data.get("preProvisioningEnabled", obj.__undef__), dirty)
        if obj._pre_provisioning_enabled[0] is not None and obj._pre_provisioning_enabled[0] is not obj.__undef__:
            assert isinstance(obj._pre_provisioning_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._pre_provisioning_enabled[0], type(obj._pre_provisioning_enabled[0])))
            common.validate_format(obj._pre_provisioning_enabled[0], "None", None, None)
        obj._link_now = (data.get("linkNow", obj.__undef__), dirty)
        if obj._link_now[0] is not None and obj._link_now[0] is not obj.__undef__:
            assert isinstance(obj._link_now[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._link_now[0], type(obj._link_now[0])))
            common.validate_format(obj._link_now[0], "None", None, None)
        if "environmentUser" not in data:
            raise ValueError("Missing required property \"environmentUser\".")
        obj._environment_user = (data.get("environmentUser", obj.__undef__), dirty)
        if obj._environment_user[0] is not None and obj._environment_user[0] is not obj.__undef__:
            assert isinstance(obj._environment_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._environment_user[0], type(obj._environment_user[0])))
            common.validate_format(obj._environment_user[0], "objectReference", None, None)
        obj._oracle_fallback_user = (data.get("oracleFallbackUser", obj.__undef__), dirty)
        if obj._oracle_fallback_user[0] is not None and obj._oracle_fallback_user[0] is not obj.__undef__:
            assert isinstance(obj._oracle_fallback_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._oracle_fallback_user[0], type(obj._oracle_fallback_user[0])))
            common.validate_format(obj._oracle_fallback_user[0], "None", None, None)
        if "oracleFallbackCredentials" in data and data["oracleFallbackCredentials"] is not None:
            obj._oracle_fallback_credentials = (factory.create_object(data["oracleFallbackCredentials"], "Credential"), dirty)
            factory.validate_type(obj._oracle_fallback_credentials[0], "Credential")
        else:
            obj._oracle_fallback_credentials = (obj.__undef__, dirty)
        if "syncParameters" in data and data["syncParameters"] is not None:
            obj._sync_parameters = (factory.create_object(data["syncParameters"], "OracleSyncFromExternalParameters"), dirty)
            factory.validate_type(obj._sync_parameters[0], "OracleSyncFromExternalParameters")
        else:
            obj._sync_parameters = (obj.__undef__, dirty)
        if "sourcingPolicy" in data and data["sourcingPolicy"] is not None:
            obj._sourcing_policy = (factory.create_object(data["sourcingPolicy"], "OracleSourcingPolicy"), dirty)
            factory.validate_type(obj._sourcing_policy[0], "OracleSourcingPolicy")
        else:
            obj._sourcing_policy = (obj.__undef__, dirty)
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
        if "sync_strategy" == "type" or (self.sync_strategy is not self.__undef__ and (not (dirty and not self._sync_strategy[1]) or self.is_dirty_list(self.sync_strategy, self._sync_strategy) or belongs_to_parent)):
            dct["syncStrategy"] = dictify(self.sync_strategy, prop_is_list_or_vo=True)
        if "diagnose_no_logging_faults" == "type" or (self.diagnose_no_logging_faults is not self.__undef__ and (not (dirty and not self._diagnose_no_logging_faults[1]) or self.is_dirty_list(self.diagnose_no_logging_faults, self._diagnose_no_logging_faults) or belongs_to_parent)):
            dct["diagnoseNoLoggingFaults"] = dictify(self.diagnose_no_logging_faults)
        elif belongs_to_parent and self.diagnose_no_logging_faults is self.__undef__:
            dct["diagnoseNoLoggingFaults"] = True
        if "pre_provisioning_enabled" == "type" or (self.pre_provisioning_enabled is not self.__undef__ and (not (dirty and not self._pre_provisioning_enabled[1]) or self.is_dirty_list(self.pre_provisioning_enabled, self._pre_provisioning_enabled) or belongs_to_parent)):
            dct["preProvisioningEnabled"] = dictify(self.pre_provisioning_enabled)
        elif belongs_to_parent and self.pre_provisioning_enabled is self.__undef__:
            dct["preProvisioningEnabled"] = False
        if "link_now" == "type" or (self.link_now is not self.__undef__ and (not (dirty and not self._link_now[1]) or self.is_dirty_list(self.link_now, self._link_now) or belongs_to_parent)):
            dct["linkNow"] = dictify(self.link_now)
        elif belongs_to_parent and self.link_now is self.__undef__:
            dct["linkNow"] = False
        if "environment_user" == "type" or (self.environment_user is not self.__undef__ and (not (dirty and not self._environment_user[1]) or self.is_dirty_list(self.environment_user, self._environment_user) or belongs_to_parent)):
            dct["environmentUser"] = dictify(self.environment_user)
        if "oracle_fallback_user" == "type" or (self.oracle_fallback_user is not self.__undef__ and (not (dirty and not self._oracle_fallback_user[1]) or self.is_dirty_list(self.oracle_fallback_user, self._oracle_fallback_user) or belongs_to_parent)):
            dct["oracleFallbackUser"] = dictify(self.oracle_fallback_user)
        if "oracle_fallback_credentials" == "type" or (self.oracle_fallback_credentials is not self.__undef__ and (not (dirty and not self._oracle_fallback_credentials[1]) or self.is_dirty_list(self.oracle_fallback_credentials, self._oracle_fallback_credentials) or belongs_to_parent)):
            dct["oracleFallbackCredentials"] = dictify(self.oracle_fallback_credentials, prop_is_list_or_vo=True)
        if "sync_parameters" == "type" or (self.sync_parameters is not self.__undef__ and (not (dirty and not self._sync_parameters[1]) or self.is_dirty_list(self.sync_parameters, self._sync_parameters) or belongs_to_parent)):
            dct["syncParameters"] = dictify(self.sync_parameters, prop_is_list_or_vo=True)
        if "sourcing_policy" == "type" or (self.sourcing_policy is not self.__undef__ and (not (dirty and not self._sourcing_policy[1]) or self.is_dirty_list(self.sourcing_policy, self._sourcing_policy) or belongs_to_parent)):
            dct["sourcingPolicy"] = dictify(self.sourcing_policy, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._sync_strategy = (self._sync_strategy[0], True)
        self._diagnose_no_logging_faults = (self._diagnose_no_logging_faults[0], True)
        self._pre_provisioning_enabled = (self._pre_provisioning_enabled[0], True)
        self._link_now = (self._link_now[0], True)
        self._environment_user = (self._environment_user[0], True)
        self._oracle_fallback_user = (self._oracle_fallback_user[0], True)
        self._oracle_fallback_credentials = (self._oracle_fallback_credentials[0], True)
        self._sync_parameters = (self._sync_parameters[0], True)
        self._sourcing_policy = (self._sourcing_policy[0], True)

    def is_dirty(self):
        return any([self._sync_strategy[1], self._diagnose_no_logging_faults[1], self._pre_provisioning_enabled[1], self._link_now[1], self._environment_user[1], self._oracle_fallback_user[1], self._oracle_fallback_credentials[1], self._sync_parameters[1], self._sourcing_policy[1]])

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
        if not isinstance(other, OracleBaseExternalLinkData):
            return False
        return super().__eq__(other) and \
               self.sync_strategy == other.sync_strategy and \
               self.diagnose_no_logging_faults == other.diagnose_no_logging_faults and \
               self.pre_provisioning_enabled == other.pre_provisioning_enabled and \
               self.link_now == other.link_now and \
               self.environment_user == other.environment_user and \
               self.oracle_fallback_user == other.oracle_fallback_user and \
               self.oracle_fallback_credentials == other.oracle_fallback_credentials and \
               self.sync_parameters == other.sync_parameters and \
               self.sourcing_policy == other.sourcing_policy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def sync_strategy(self):
        """
        Persistent parameters to sync the container.

        :rtype: :py:class:`v1_11_40.web.vo.OracleSourceBasedSyncStrategy`
        """
        return self._sync_strategy[0]

    @sync_strategy.setter
    def sync_strategy(self, value):
        self._sync_strategy = (value, True)

    @property
    def diagnose_no_logging_faults(self):
        """
        *(default value: True)* If true, NOLOGGING operations on this container
        are treated as faults and cannot be resolved manually. Otherwise, these
        operations are ignored.

        :rtype: ``bool``
        """
        return self._diagnose_no_logging_faults[0]

    @diagnose_no_logging_faults.setter
    def diagnose_no_logging_faults(self, value):
        self._diagnose_no_logging_faults = (value, True)

    @property
    def pre_provisioning_enabled(self):
        """
        If true, pre-provisioning will be performed after every sync.

        :rtype: ``bool``
        """
        return self._pre_provisioning_enabled[0]

    @pre_provisioning_enabled.setter
    def pre_provisioning_enabled(self, value):
        self._pre_provisioning_enabled = (value, True)

    @property
    def link_now(self):
        """
        True if initial load should be done immediately.

        :rtype: ``bool``
        """
        return self._link_now[0]

    @link_now.setter
    def link_now(self, value):
        self._link_now = (value, True)

    @property
    def environment_user(self):
        """
        Information about the OS user to use for linking.

        :rtype: ``str``
        """
        return self._environment_user[0]

    @environment_user.setter
    def environment_user(self, value):
        self._environment_user = (value, True)

    @property
    def oracle_fallback_user(self):
        """
        The database user. Optional if bequeath connections are enabled (to be
        used in case of bequeath connection failures).

        :rtype: ``str``
        """
        return self._oracle_fallback_user[0]

    @oracle_fallback_user.setter
    def oracle_fallback_user(self, value):
        self._oracle_fallback_user = (value, True)

    @property
    def oracle_fallback_credentials(self):
        """
        The credentials for the database user. Optional if bequeath connections
        are enabled (to be used in case of bequeath connection failures).

        :rtype: :py:class:`v1_11_40.web.vo.Credential`
        """
        return self._oracle_fallback_credentials[0]

    @oracle_fallback_credentials.setter
    def oracle_fallback_credentials(self, value):
        self._oracle_fallback_credentials = (value, True)

    @property
    def sync_parameters(self):
        """
        Parameters used to initially sync the database.

        :rtype: :py:class:`v1_11_40.web.vo.OracleSyncFromExternalParameters`
        """
        return self._sync_parameters[0]

    @sync_parameters.setter
    def sync_parameters(self, value):
        self._sync_parameters = (value, True)

    @property
    def sourcing_policy(self):
        """
        Policies for managing LogSync and SnapSync across sources.

        :rtype: :py:class:`v1_11_40.web.vo.OracleSourcingPolicy`
        """
        return self._sourcing_policy[0]

    @sourcing_policy.setter
    def sourcing_policy(self, value):
        self._sourcing_policy = (value, True)

