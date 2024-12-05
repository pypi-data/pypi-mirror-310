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
#     /delphix-host.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.ReadonlyNamedUserObject import ReadonlyNamedUserObject
from delphixpy.v1_11_20 import factory
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Host(ReadonlyNamedUserObject):
    """
    *(extends* :py:class:`v1_11_20.web.vo.ReadonlyNamedUserObject` *)* The
    representation of a host object.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Host", True)
        self._address = (self.__undef__, True)
        self._nfs_address_list = (self.__undef__, True)
        self._ssh_port = (self.__undef__, True)
        self._date_added = (self.__undef__, True)
        self._host_configuration = (self.__undef__, True)
        self._host_runtime = (self.__undef__, True)
        self._privilege_elevation_profile = (self.__undef__, True)
        self._dsp_keystore_alias = (self.__undef__, True)
        self._dsp_keystore_password = (self.__undef__, True)
        self._dsp_keystore_path = (self.__undef__, True)
        self._dsp_truststore_password = (self.__undef__, True)
        self._dsp_truststore_path = (self.__undef__, True)
        self._java_home = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._address = (data.get("address", obj.__undef__), dirty)
        if obj._address[0] is not None and obj._address[0] is not obj.__undef__:
            assert isinstance(obj._address[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._address[0], type(obj._address[0])))
            common.validate_format(obj._address[0], "host", None, None)
        obj._nfs_address_list = []
        for item in data.get("nfsAddressList") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "host", None, None)
            obj._nfs_address_list.append(item)
        obj._nfs_address_list = (obj._nfs_address_list, dirty)
        obj._ssh_port = (data.get("sshPort", obj.__undef__), dirty)
        if obj._ssh_port[0] is not None and obj._ssh_port[0] is not obj.__undef__:
            assert isinstance(obj._ssh_port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._ssh_port[0], type(obj._ssh_port[0])))
            common.validate_format(obj._ssh_port[0], "None", None, None)
        obj._date_added = (data.get("dateAdded", obj.__undef__), dirty)
        if obj._date_added[0] is not None and obj._date_added[0] is not obj.__undef__:
            assert isinstance(obj._date_added[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._date_added[0], type(obj._date_added[0])))
            common.validate_format(obj._date_added[0], "None", None, None)
        if "hostConfiguration" in data and data["hostConfiguration"] is not None:
            obj._host_configuration = (factory.create_object(data["hostConfiguration"], "HostConfiguration"), dirty)
            factory.validate_type(obj._host_configuration[0], "HostConfiguration")
        else:
            obj._host_configuration = (obj.__undef__, dirty)
        if "hostRuntime" in data and data["hostRuntime"] is not None:
            obj._host_runtime = (factory.create_object(data["hostRuntime"], "HostRuntime"), dirty)
            factory.validate_type(obj._host_runtime[0], "HostRuntime")
        else:
            obj._host_runtime = (obj.__undef__, dirty)
        obj._privilege_elevation_profile = (data.get("privilegeElevationProfile", obj.__undef__), dirty)
        if obj._privilege_elevation_profile[0] is not None and obj._privilege_elevation_profile[0] is not obj.__undef__:
            assert isinstance(obj._privilege_elevation_profile[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._privilege_elevation_profile[0], type(obj._privilege_elevation_profile[0])))
            common.validate_format(obj._privilege_elevation_profile[0], "objectReference", None, None)
        obj._dsp_keystore_alias = (data.get("dspKeystoreAlias", obj.__undef__), dirty)
        if obj._dsp_keystore_alias[0] is not None and obj._dsp_keystore_alias[0] is not obj.__undef__:
            assert isinstance(obj._dsp_keystore_alias[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._dsp_keystore_alias[0], type(obj._dsp_keystore_alias[0])))
            common.validate_format(obj._dsp_keystore_alias[0], "None", 1, None)
        obj._dsp_keystore_password = (data.get("dspKeystorePassword", obj.__undef__), dirty)
        if obj._dsp_keystore_password[0] is not None and obj._dsp_keystore_password[0] is not obj.__undef__:
            assert isinstance(obj._dsp_keystore_password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._dsp_keystore_password[0], type(obj._dsp_keystore_password[0])))
            common.validate_format(obj._dsp_keystore_password[0], "password", 1, None)
        obj._dsp_keystore_path = (data.get("dspKeystorePath", obj.__undef__), dirty)
        if obj._dsp_keystore_path[0] is not None and obj._dsp_keystore_path[0] is not obj.__undef__:
            assert isinstance(obj._dsp_keystore_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._dsp_keystore_path[0], type(obj._dsp_keystore_path[0])))
            common.validate_format(obj._dsp_keystore_path[0], "None", 1, None)
        obj._dsp_truststore_password = (data.get("dspTruststorePassword", obj.__undef__), dirty)
        if obj._dsp_truststore_password[0] is not None and obj._dsp_truststore_password[0] is not obj.__undef__:
            assert isinstance(obj._dsp_truststore_password[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._dsp_truststore_password[0], type(obj._dsp_truststore_password[0])))
            common.validate_format(obj._dsp_truststore_password[0], "password", 1, None)
        obj._dsp_truststore_path = (data.get("dspTruststorePath", obj.__undef__), dirty)
        if obj._dsp_truststore_path[0] is not None and obj._dsp_truststore_path[0] is not obj.__undef__:
            assert isinstance(obj._dsp_truststore_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._dsp_truststore_path[0], type(obj._dsp_truststore_path[0])))
            common.validate_format(obj._dsp_truststore_path[0], "None", 1, None)
        obj._java_home = (data.get("javaHome", obj.__undef__), dirty)
        if obj._java_home[0] is not None and obj._java_home[0] is not obj.__undef__:
            assert isinstance(obj._java_home[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._java_home[0], type(obj._java_home[0])))
            common.validate_format(obj._java_home[0], "None", 1, None)
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
        if "address" == "type" or (self.address is not self.__undef__ and (not (dirty and not self._address[1]) or self.is_dirty_list(self.address, self._address) or belongs_to_parent)):
            dct["address"] = dictify(self.address)
        if "nfs_address_list" == "type" or (self.nfs_address_list is not self.__undef__ and (not (dirty and not self._nfs_address_list[1]) or self.is_dirty_list(self.nfs_address_list, self._nfs_address_list) or belongs_to_parent)):
            dct["nfsAddressList"] = dictify(self.nfs_address_list, prop_is_list_or_vo=True)
        if "ssh_port" == "type" or (self.ssh_port is not self.__undef__ and (not (dirty and not self._ssh_port[1]) or self.is_dirty_list(self.ssh_port, self._ssh_port) or belongs_to_parent)):
            dct["sshPort"] = dictify(self.ssh_port)
        elif belongs_to_parent and self.ssh_port is self.__undef__:
            dct["sshPort"] = 22
        if "date_added" == "type" or (self.date_added is not self.__undef__ and (not (dirty and not self._date_added[1]))):
            dct["dateAdded"] = dictify(self.date_added)
        if "host_configuration" == "type" or (self.host_configuration is not self.__undef__ and (not (dirty and not self._host_configuration[1]))):
            dct["hostConfiguration"] = dictify(self.host_configuration)
        if "host_runtime" == "type" or (self.host_runtime is not self.__undef__ and (not (dirty and not self._host_runtime[1]))):
            dct["hostRuntime"] = dictify(self.host_runtime)
        if "privilege_elevation_profile" == "type" or (self.privilege_elevation_profile is not self.__undef__ and (not (dirty and not self._privilege_elevation_profile[1]) or self.is_dirty_list(self.privilege_elevation_profile, self._privilege_elevation_profile) or belongs_to_parent)):
            dct["privilegeElevationProfile"] = dictify(self.privilege_elevation_profile)
        if "dsp_keystore_alias" == "type" or (self.dsp_keystore_alias is not self.__undef__ and (not (dirty and not self._dsp_keystore_alias[1]) or self.is_dirty_list(self.dsp_keystore_alias, self._dsp_keystore_alias) or belongs_to_parent)):
            dct["dspKeystoreAlias"] = dictify(self.dsp_keystore_alias)
        if "dsp_keystore_password" == "type" or (self.dsp_keystore_password is not self.__undef__ and (not (dirty and not self._dsp_keystore_password[1]) or self.is_dirty_list(self.dsp_keystore_password, self._dsp_keystore_password) or belongs_to_parent)):
            dct["dspKeystorePassword"] = dictify(self.dsp_keystore_password)
        if "dsp_keystore_path" == "type" or (self.dsp_keystore_path is not self.__undef__ and (not (dirty and not self._dsp_keystore_path[1]) or self.is_dirty_list(self.dsp_keystore_path, self._dsp_keystore_path) or belongs_to_parent)):
            dct["dspKeystorePath"] = dictify(self.dsp_keystore_path)
        if "dsp_truststore_password" == "type" or (self.dsp_truststore_password is not self.__undef__ and (not (dirty and not self._dsp_truststore_password[1]) or self.is_dirty_list(self.dsp_truststore_password, self._dsp_truststore_password) or belongs_to_parent)):
            dct["dspTruststorePassword"] = dictify(self.dsp_truststore_password)
        if "dsp_truststore_path" == "type" or (self.dsp_truststore_path is not self.__undef__ and (not (dirty and not self._dsp_truststore_path[1]) or self.is_dirty_list(self.dsp_truststore_path, self._dsp_truststore_path) or belongs_to_parent)):
            dct["dspTruststorePath"] = dictify(self.dsp_truststore_path)
        if "java_home" == "type" or (self.java_home is not self.__undef__ and (not (dirty and not self._java_home[1]) or self.is_dirty_list(self.java_home, self._java_home) or belongs_to_parent)):
            dct["javaHome"] = dictify(self.java_home)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._address = (self._address[0], True)
        self._nfs_address_list = (self._nfs_address_list[0], True)
        self._ssh_port = (self._ssh_port[0], True)
        self._date_added = (self._date_added[0], True)
        self._host_configuration = (self._host_configuration[0], True)
        self._host_runtime = (self._host_runtime[0], True)
        self._privilege_elevation_profile = (self._privilege_elevation_profile[0], True)
        self._dsp_keystore_alias = (self._dsp_keystore_alias[0], True)
        self._dsp_keystore_password = (self._dsp_keystore_password[0], True)
        self._dsp_keystore_path = (self._dsp_keystore_path[0], True)
        self._dsp_truststore_password = (self._dsp_truststore_password[0], True)
        self._dsp_truststore_path = (self._dsp_truststore_path[0], True)
        self._java_home = (self._java_home[0], True)

    def is_dirty(self):
        return any([self._address[1], self._nfs_address_list[1], self._ssh_port[1], self._date_added[1], self._host_configuration[1], self._host_runtime[1], self._privilege_elevation_profile[1], self._dsp_keystore_alias[1], self._dsp_keystore_password[1], self._dsp_keystore_path[1], self._dsp_truststore_password[1], self._dsp_truststore_path[1], self._java_home[1]])

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
        if not isinstance(other, Host):
            return False
        return super().__eq__(other) and \
               self.address == other.address and \
               self.nfs_address_list == other.nfs_address_list and \
               self.ssh_port == other.ssh_port and \
               self.date_added == other.date_added and \
               self.host_configuration == other.host_configuration and \
               self.host_runtime == other.host_runtime and \
               self.privilege_elevation_profile == other.privilege_elevation_profile and \
               self.dsp_keystore_alias == other.dsp_keystore_alias and \
               self.dsp_keystore_password == other.dsp_keystore_password and \
               self.dsp_keystore_path == other.dsp_keystore_path and \
               self.dsp_truststore_password == other.dsp_truststore_password and \
               self.dsp_truststore_path == other.dsp_truststore_path and \
               self.java_home == other.java_home

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def address(self):
        """
        The address associated with the host.

        :rtype: ``str``
        """
        return self._address[0]

    @address.setter
    def address(self, value):
        self._address = (value, True)

    @property
    def nfs_address_list(self):
        """
        The list of host/IP addresses to use for NFS export.

        :rtype: ``list`` of ``str``
        """
        return self._nfs_address_list[0]

    @nfs_address_list.setter
    def nfs_address_list(self, value):
        self._nfs_address_list = (value, True)

    @property
    def ssh_port(self):
        """
        *(default value: 22)* The port number used to connect to the host via
        SSH.

        :rtype: ``int``
        """
        return self._ssh_port[0]

    @ssh_port.setter
    def ssh_port(self, value):
        self._ssh_port = (value, True)

    @property
    def date_added(self):
        """
        The date the host was added.

        :rtype: ``str``
        """
        return self._date_added[0]

    @date_added.setter
    def date_added(self, value):
        self._date_added = (value, True)

    @property
    def host_configuration(self):
        """
        The host configuration object associated with the host.

        :rtype: :py:class:`v1_11_20.web.vo.HostConfiguration`
        """
        return self._host_configuration[0]

    @host_configuration.setter
    def host_configuration(self, value):
        self._host_configuration = (value, True)

    @property
    def host_runtime(self):
        """
        Runtime properties for this host.

        :rtype: :py:class:`v1_11_20.web.vo.HostRuntime`
        """
        return self._host_runtime[0]

    @host_runtime.setter
    def host_runtime(self, value):
        self._host_runtime = (value, True)

    @property
    def privilege_elevation_profile(self):
        """
        Profile for escalating user privileges.

        :rtype: ``str``
        """
        return self._privilege_elevation_profile[0]

    @privilege_elevation_profile.setter
    def privilege_elevation_profile(self, value):
        self._privilege_elevation_profile = (value, True)

    @property
    def dsp_keystore_alias(self):
        """
        The lowercase alias to use inside the user managed DSP keystore.

        :rtype: ``str``
        """
        return self._dsp_keystore_alias[0]

    @dsp_keystore_alias.setter
    def dsp_keystore_alias(self, value):
        self._dsp_keystore_alias = (value, True)

    @property
    def dsp_keystore_password(self):
        """
        The password for the user managed DSP keystore.

        :rtype: ``str``
        """
        return self._dsp_keystore_password[0]

    @dsp_keystore_password.setter
    def dsp_keystore_password(self, value):
        self._dsp_keystore_password = (value, True)

    @property
    def dsp_keystore_path(self):
        """
        The path to the user managed DSP keystore.

        :rtype: ``str``
        """
        return self._dsp_keystore_path[0]

    @dsp_keystore_path.setter
    def dsp_keystore_path(self, value):
        self._dsp_keystore_path = (value, True)

    @property
    def dsp_truststore_password(self):
        """
        The password for the user managed DSP truststore.

        :rtype: ``str``
        """
        return self._dsp_truststore_password[0]

    @dsp_truststore_password.setter
    def dsp_truststore_password(self, value):
        self._dsp_truststore_password = (value, True)

    @property
    def dsp_truststore_path(self):
        """
        The path to the user managed DSP truststore.

        :rtype: ``str``
        """
        return self._dsp_truststore_path[0]

    @dsp_truststore_path.setter
    def dsp_truststore_path(self, value):
        self._dsp_truststore_path = (value, True)

    @property
    def java_home(self):
        """
        The path to the user managed Java Development Kit (JDK). If not
        specified, then the OpenJDK will be used.

        :rtype: ``str`` *or* ``null``
        """
        return self._java_home[0]

    @java_home.setter
    def java_home(self, value):
        self._java_home = (value, True)

