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
#     /delphix-ase-instance.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_33.web.objects.SourceRepository import SourceRepository
from delphixpy.v1_11_33 import factory
from delphixpy.v1_11_33 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ASEInstance(SourceRepository):
    """
    *(extends* :py:class:`v1_11_33.web.vo.SourceRepository` *)* The SAP ASE
    source repository.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ASEInstance", True)
        self._instance_name = (self.__undef__, True)
        self._installation_path = (self.__undef__, True)
        self._ports = (self.__undef__, True)
        self._instance_owner = (self.__undef__, True)
        self._instance_owner_uid = (self.__undef__, True)
        self._instance_owner_gid = (self.__undef__, True)
        self._page_size = (self.__undef__, True)
        self._service_principal_name = (self.__undef__, True)
        self._db_user = (self.__undef__, True)
        self._isql_path = (self.__undef__, True)
        self._dump_history_file = (self.__undef__, True)
        self._credentials = (self.__undef__, True)
        self._discovered = (self.__undef__, True)
        self._tls_enabled = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._instance_name = (data.get("instanceName", obj.__undef__), dirty)
        if obj._instance_name[0] is not None and obj._instance_name[0] is not obj.__undef__:
            assert isinstance(obj._instance_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._instance_name[0], type(obj._instance_name[0])))
            common.validate_format(obj._instance_name[0], "None", None, None)
        obj._installation_path = (data.get("installationPath", obj.__undef__), dirty)
        if obj._installation_path[0] is not None and obj._installation_path[0] is not obj.__undef__:
            assert isinstance(obj._installation_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._installation_path[0], type(obj._installation_path[0])))
            common.validate_format(obj._installation_path[0], "None", None, None)
        obj._ports = []
        for item in data.get("ports") or []:
            assert isinstance(item, int), ("Expected one of ['integer'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._ports.append(item)
        obj._ports = (obj._ports, dirty)
        obj._instance_owner = (data.get("instanceOwner", obj.__undef__), dirty)
        if obj._instance_owner[0] is not None and obj._instance_owner[0] is not obj.__undef__:
            assert isinstance(obj._instance_owner[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._instance_owner[0], type(obj._instance_owner[0])))
            common.validate_format(obj._instance_owner[0], "None", None, None)
        obj._instance_owner_uid = (data.get("instanceOwnerUid", obj.__undef__), dirty)
        if obj._instance_owner_uid[0] is not None and obj._instance_owner_uid[0] is not obj.__undef__:
            assert isinstance(obj._instance_owner_uid[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._instance_owner_uid[0], type(obj._instance_owner_uid[0])))
            common.validate_format(obj._instance_owner_uid[0], "None", None, None)
        obj._instance_owner_gid = (data.get("instanceOwnerGid", obj.__undef__), dirty)
        if obj._instance_owner_gid[0] is not None and obj._instance_owner_gid[0] is not obj.__undef__:
            assert isinstance(obj._instance_owner_gid[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._instance_owner_gid[0], type(obj._instance_owner_gid[0])))
            common.validate_format(obj._instance_owner_gid[0], "None", None, None)
        obj._page_size = (data.get("pageSize", obj.__undef__), dirty)
        if obj._page_size[0] is not None and obj._page_size[0] is not obj.__undef__:
            assert isinstance(obj._page_size[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._page_size[0], type(obj._page_size[0])))
            common.validate_format(obj._page_size[0], "None", None, None)
        obj._service_principal_name = (data.get("servicePrincipalName", obj.__undef__), dirty)
        if obj._service_principal_name[0] is not None and obj._service_principal_name[0] is not obj.__undef__:
            assert isinstance(obj._service_principal_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._service_principal_name[0], type(obj._service_principal_name[0])))
            common.validate_format(obj._service_principal_name[0], "None", None, None)
        obj._db_user = (data.get("dbUser", obj.__undef__), dirty)
        if obj._db_user[0] is not None and obj._db_user[0] is not obj.__undef__:
            assert isinstance(obj._db_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._db_user[0], type(obj._db_user[0])))
            common.validate_format(obj._db_user[0], "None", None, 256)
        obj._isql_path = (data.get("isqlPath", obj.__undef__), dirty)
        if obj._isql_path[0] is not None and obj._isql_path[0] is not obj.__undef__:
            assert isinstance(obj._isql_path[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._isql_path[0], type(obj._isql_path[0])))
            common.validate_format(obj._isql_path[0], "None", None, None)
        obj._dump_history_file = (data.get("dumpHistoryFile", obj.__undef__), dirty)
        if obj._dump_history_file[0] is not None and obj._dump_history_file[0] is not obj.__undef__:
            assert isinstance(obj._dump_history_file[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._dump_history_file[0], type(obj._dump_history_file[0])))
            common.validate_format(obj._dump_history_file[0], "None", None, None)
        if "credentials" in data and data["credentials"] is not None:
            obj._credentials = (factory.create_object(data["credentials"], "Credential"), dirty)
            factory.validate_type(obj._credentials[0], "Credential")
        else:
            obj._credentials = (obj.__undef__, dirty)
        obj._discovered = (data.get("discovered", obj.__undef__), dirty)
        if obj._discovered[0] is not None and obj._discovered[0] is not obj.__undef__:
            assert isinstance(obj._discovered[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._discovered[0], type(obj._discovered[0])))
            common.validate_format(obj._discovered[0], "None", None, None)
        obj._tls_enabled = (data.get("tlsEnabled", obj.__undef__), dirty)
        if obj._tls_enabled[0] is not None and obj._tls_enabled[0] is not obj.__undef__:
            assert isinstance(obj._tls_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._tls_enabled[0], type(obj._tls_enabled[0])))
            common.validate_format(obj._tls_enabled[0], "None", None, None)
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
        if "instance_name" == "type" or (self.instance_name is not self.__undef__ and (not (dirty and not self._instance_name[1]) or self.is_dirty_list(self.instance_name, self._instance_name) or belongs_to_parent)):
            dct["instanceName"] = dictify(self.instance_name)
        if "installation_path" == "type" or (self.installation_path is not self.__undef__ and (not (dirty and not self._installation_path[1]) or self.is_dirty_list(self.installation_path, self._installation_path) or belongs_to_parent)):
            dct["installationPath"] = dictify(self.installation_path)
        if "ports" == "type" or (self.ports is not self.__undef__ and (not (dirty and not self._ports[1]) or self.is_dirty_list(self.ports, self._ports) or belongs_to_parent)):
            dct["ports"] = dictify(self.ports, prop_is_list_or_vo=True)
        if "instance_owner" == "type" or (self.instance_owner is not self.__undef__ and (not (dirty and not self._instance_owner[1]) or self.is_dirty_list(self.instance_owner, self._instance_owner) or belongs_to_parent)):
            dct["instanceOwner"] = dictify(self.instance_owner)
        if "instance_owner_uid" == "type" or (self.instance_owner_uid is not self.__undef__ and (not (dirty and not self._instance_owner_uid[1]))):
            dct["instanceOwnerUid"] = dictify(self.instance_owner_uid)
        if dirty and "instanceOwnerUid" in dct:
            del dct["instanceOwnerUid"]
        if "instance_owner_gid" == "type" or (self.instance_owner_gid is not self.__undef__ and (not (dirty and not self._instance_owner_gid[1]))):
            dct["instanceOwnerGid"] = dictify(self.instance_owner_gid)
        if dirty and "instanceOwnerGid" in dct:
            del dct["instanceOwnerGid"]
        if "page_size" == "type" or (self.page_size is not self.__undef__ and (not (dirty and not self._page_size[1]))):
            dct["pageSize"] = dictify(self.page_size)
        if "service_principal_name" == "type" or (self.service_principal_name is not self.__undef__ and (not (dirty and not self._service_principal_name[1]) or self.is_dirty_list(self.service_principal_name, self._service_principal_name) or belongs_to_parent)):
            dct["servicePrincipalName"] = dictify(self.service_principal_name)
        if "db_user" == "type" or (self.db_user is not self.__undef__ and (not (dirty and not self._db_user[1]) or self.is_dirty_list(self.db_user, self._db_user) or belongs_to_parent)):
            dct["dbUser"] = dictify(self.db_user)
        if "isql_path" == "type" or (self.isql_path is not self.__undef__ and (not (dirty and not self._isql_path[1]) or self.is_dirty_list(self.isql_path, self._isql_path) or belongs_to_parent)):
            dct["isqlPath"] = dictify(self.isql_path)
        if "dump_history_file" == "type" or (self.dump_history_file is not self.__undef__ and (not (dirty and not self._dump_history_file[1]) or self.is_dirty_list(self.dump_history_file, self._dump_history_file) or belongs_to_parent)):
            dct["dumpHistoryFile"] = dictify(self.dump_history_file)
        if "credentials" == "type" or (self.credentials is not self.__undef__ and (not (dirty and not self._credentials[1]) or self.is_dirty_list(self.credentials, self._credentials) or belongs_to_parent)):
            dct["credentials"] = dictify(self.credentials, prop_is_list_or_vo=True)
        if "discovered" == "type" or (self.discovered is not self.__undef__ and (not (dirty and not self._discovered[1]))):
            dct["discovered"] = dictify(self.discovered)
        if "tls_enabled" == "type" or (self.tls_enabled is not self.__undef__ and (not (dirty and not self._tls_enabled[1]))):
            dct["tlsEnabled"] = dictify(self.tls_enabled)
        if dirty and "tlsEnabled" in dct:
            del dct["tlsEnabled"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._instance_name = (self._instance_name[0], True)
        self._installation_path = (self._installation_path[0], True)
        self._ports = (self._ports[0], True)
        self._instance_owner = (self._instance_owner[0], True)
        self._instance_owner_uid = (self._instance_owner_uid[0], True)
        self._instance_owner_gid = (self._instance_owner_gid[0], True)
        self._page_size = (self._page_size[0], True)
        self._service_principal_name = (self._service_principal_name[0], True)
        self._db_user = (self._db_user[0], True)
        self._isql_path = (self._isql_path[0], True)
        self._dump_history_file = (self._dump_history_file[0], True)
        self._credentials = (self._credentials[0], True)
        self._discovered = (self._discovered[0], True)
        self._tls_enabled = (self._tls_enabled[0], True)

    def is_dirty(self):
        return any([self._instance_name[1], self._installation_path[1], self._ports[1], self._instance_owner[1], self._instance_owner_uid[1], self._instance_owner_gid[1], self._page_size[1], self._service_principal_name[1], self._db_user[1], self._isql_path[1], self._dump_history_file[1], self._credentials[1], self._discovered[1], self._tls_enabled[1]])

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
        if not isinstance(other, ASEInstance):
            return False
        return super().__eq__(other) and \
               self.instance_name == other.instance_name and \
               self.installation_path == other.installation_path and \
               self.ports == other.ports and \
               self.instance_owner == other.instance_owner and \
               self.instance_owner_uid == other.instance_owner_uid and \
               self.instance_owner_gid == other.instance_owner_gid and \
               self.page_size == other.page_size and \
               self.service_principal_name == other.service_principal_name and \
               self.db_user == other.db_user and \
               self.isql_path == other.isql_path and \
               self.dump_history_file == other.dump_history_file and \
               self.credentials == other.credentials and \
               self.discovered == other.discovered and \
               self.tls_enabled == other.tls_enabled

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def instance_name(self):
        """
        The name of the SAP ASE instance.

        :rtype: ``str``
        """
        return self._instance_name[0]

    @instance_name.setter
    def instance_name(self, value):
        self._instance_name = (value, True)

    @property
    def installation_path(self):
        """
        The SAP ASE instance home.

        :rtype: ``str``
        """
        return self._installation_path[0]

    @installation_path.setter
    def installation_path(self, value):
        self._installation_path = (value, True)

    @property
    def ports(self):
        """
        The network ports for connecting to the SAP ASE instance.

        :rtype: ``list`` of ``int``
        """
        return self._ports[0]

    @ports.setter
    def ports(self, value):
        self._ports = (value, True)

    @property
    def instance_owner(self):
        """
        The username of the account the SAP ASE instance is running as.

        :rtype: ``str``
        """
        return self._instance_owner[0]

    @instance_owner.setter
    def instance_owner(self, value):
        self._instance_owner = (value, True)

    @property
    def instance_owner_uid(self):
        """
        The uid of the account the SAP ASE instance is running as.

        :rtype: ``int``
        """
        return self._instance_owner_uid[0]

    @property
    def instance_owner_gid(self):
        """
        The gid of the account the SAP ASE instance is running as.

        :rtype: ``int``
        """
        return self._instance_owner_gid[0]

    @property
    def page_size(self):
        """
        Database page size for the SAP ASE instance.

        :rtype: ``int``
        """
        return self._page_size[0]

    @page_size.setter
    def page_size(self, value):
        self._page_size = (value, True)

    @property
    def service_principal_name(self):
        """
        The Kerberos SPN of the database.

        :rtype: ``str``
        """
        return self._service_principal_name[0]

    @service_principal_name.setter
    def service_principal_name(self, value):
        self._service_principal_name = (value, True)

    @property
    def db_user(self):
        """
        The username of the database user.

        :rtype: ``str``
        """
        return self._db_user[0]

    @db_user.setter
    def db_user(self, value):
        self._db_user = (value, True)

    @property
    def isql_path(self):
        """
        The path to the isql binary to use for this SAP ASE instance.

        :rtype: ``str``
        """
        return self._isql_path[0]

    @isql_path.setter
    def isql_path(self, value):
        self._isql_path = (value, True)

    @property
    def dump_history_file(self):
        """
        Fully qualified name of the dump history file.

        :rtype: ``str``
        """
        return self._dump_history_file[0]

    @dump_history_file.setter
    def dump_history_file(self, value):
        self._dump_history_file = (value, True)

    @property
    def credentials(self):
        """
        The credentials of the database user.

        :rtype: :py:class:`v1_11_33.web.vo.Credential`
        """
        return self._credentials[0]

    @credentials.setter
    def credentials(self, value):
        self._credentials = (value, True)

    @property
    def discovered(self):
        """
        True if the SAP ASE instance was automatically discovered.

        :rtype: ``bool``
        """
        return self._discovered[0]

    @discovered.setter
    def discovered(self, value):
        self._discovered = (value, True)

    @property
    def tls_enabled(self):
        """
        True if the SAP ASE instance is TLS/SSL enabled on the given port.

        :rtype: ``bool``
        """
        return self._tls_enabled[0]

