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
#     /delphix-mssql-link-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_14.web.objects.LinkData import LinkData
from delphixpy.v1_11_14 import factory
from delphixpy.v1_11_14 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlLinkData(LinkData):
    """
    *(extends* :py:class:`v1_11_14.web.vo.LinkData` *)* MSSQL specific
    parameters for a link request.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlLinkData", True)
        self._encryption_key = (self.__undef__, True)
        self._sync_parameters = (self.__undef__, True)
        self._operations = (self.__undef__, True)
        self._source_host_user = (self.__undef__, True)
        self._sync_strategy = (self.__undef__, True)
        self._ppt_repository = (self.__undef__, True)
        self._ppt_host_user = (self.__undef__, True)
        self._staging_pre_script = (self.__undef__, True)
        self._staging_post_script = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._encryption_key = (data.get("encryptionKey", obj.__undef__), dirty)
        if obj._encryption_key[0] is not None and obj._encryption_key[0] is not obj.__undef__:
            assert isinstance(obj._encryption_key[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._encryption_key[0], type(obj._encryption_key[0])))
            common.validate_format(obj._encryption_key[0], "None", None, None)
        if "syncParameters" not in data:
            raise ValueError("Missing required property \"syncParameters\".")
        if "syncParameters" in data and data["syncParameters"] is not None:
            obj._sync_parameters = (factory.create_object(data["syncParameters"], "MSSqlSyncParameters"), dirty)
            factory.validate_type(obj._sync_parameters[0], "MSSqlSyncParameters")
        else:
            obj._sync_parameters = (obj.__undef__, dirty)
        if "operations" in data and data["operations"] is not None:
            obj._operations = (factory.create_object(data["operations"], "LinkedSourceOperations"), dirty)
            factory.validate_type(obj._operations[0], "LinkedSourceOperations")
        else:
            obj._operations = (obj.__undef__, dirty)
        obj._source_host_user = (data.get("sourceHostUser", obj.__undef__), dirty)
        if obj._source_host_user[0] is not None and obj._source_host_user[0] is not obj.__undef__:
            assert isinstance(obj._source_host_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._source_host_user[0], type(obj._source_host_user[0])))
            common.validate_format(obj._source_host_user[0], "objectReference", None, None)
        if "syncStrategy" not in data:
            raise ValueError("Missing required property \"syncStrategy\".")
        if "syncStrategy" in data and data["syncStrategy"] is not None:
            obj._sync_strategy = (factory.create_object(data["syncStrategy"], "MSSqlSyncStrategy"), dirty)
            factory.validate_type(obj._sync_strategy[0], "MSSqlSyncStrategy")
        else:
            obj._sync_strategy = (obj.__undef__, dirty)
        if "pptRepository" not in data:
            raise ValueError("Missing required property \"pptRepository\".")
        obj._ppt_repository = (data.get("pptRepository", obj.__undef__), dirty)
        if obj._ppt_repository[0] is not None and obj._ppt_repository[0] is not obj.__undef__:
            assert isinstance(obj._ppt_repository[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ppt_repository[0], type(obj._ppt_repository[0])))
            common.validate_format(obj._ppt_repository[0], "objectReference", None, None)
        obj._ppt_host_user = (data.get("pptHostUser", obj.__undef__), dirty)
        if obj._ppt_host_user[0] is not None and obj._ppt_host_user[0] is not obj.__undef__:
            assert isinstance(obj._ppt_host_user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ppt_host_user[0], type(obj._ppt_host_user[0])))
            common.validate_format(obj._ppt_host_user[0], "objectReference", None, None)
        obj._staging_pre_script = (data.get("stagingPreScript", obj.__undef__), dirty)
        if obj._staging_pre_script[0] is not None and obj._staging_pre_script[0] is not obj.__undef__:
            assert isinstance(obj._staging_pre_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_pre_script[0], type(obj._staging_pre_script[0])))
            common.validate_format(obj._staging_pre_script[0], "None", None, 1024)
        obj._staging_post_script = (data.get("stagingPostScript", obj.__undef__), dirty)
        if obj._staging_post_script[0] is not None and obj._staging_post_script[0] is not obj.__undef__:
            assert isinstance(obj._staging_post_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._staging_post_script[0], type(obj._staging_post_script[0])))
            common.validate_format(obj._staging_post_script[0], "None", None, 1024)
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
        if "encryption_key" == "type" or (self.encryption_key is not self.__undef__ and (not (dirty and not self._encryption_key[1]) or self.is_dirty_list(self.encryption_key, self._encryption_key) or belongs_to_parent)):
            dct["encryptionKey"] = dictify(self.encryption_key)
        if "sync_parameters" == "type" or (self.sync_parameters is not self.__undef__ and (not (dirty and not self._sync_parameters[1]) or self.is_dirty_list(self.sync_parameters, self._sync_parameters) or belongs_to_parent)):
            dct["syncParameters"] = dictify(self.sync_parameters, prop_is_list_or_vo=True)
        if "operations" == "type" or (self.operations is not self.__undef__ and (not (dirty and not self._operations[1]) or self.is_dirty_list(self.operations, self._operations) or belongs_to_parent)):
            dct["operations"] = dictify(self.operations, prop_is_list_or_vo=True)
        if "source_host_user" == "type" or (self.source_host_user is not self.__undef__ and (not (dirty and not self._source_host_user[1]) or self.is_dirty_list(self.source_host_user, self._source_host_user) or belongs_to_parent)):
            dct["sourceHostUser"] = dictify(self.source_host_user)
        if "sync_strategy" == "type" or (self.sync_strategy is not self.__undef__ and (not (dirty and not self._sync_strategy[1]) or self.is_dirty_list(self.sync_strategy, self._sync_strategy) or belongs_to_parent)):
            dct["syncStrategy"] = dictify(self.sync_strategy, prop_is_list_or_vo=True)
        if "ppt_repository" == "type" or (self.ppt_repository is not self.__undef__ and (not (dirty and not self._ppt_repository[1]) or self.is_dirty_list(self.ppt_repository, self._ppt_repository) or belongs_to_parent)):
            dct["pptRepository"] = dictify(self.ppt_repository)
        if "ppt_host_user" == "type" or (self.ppt_host_user is not self.__undef__ and (not (dirty and not self._ppt_host_user[1]) or self.is_dirty_list(self.ppt_host_user, self._ppt_host_user) or belongs_to_parent)):
            dct["pptHostUser"] = dictify(self.ppt_host_user)
        if "staging_pre_script" == "type" or (self.staging_pre_script is not self.__undef__ and (not (dirty and not self._staging_pre_script[1]) or self.is_dirty_list(self.staging_pre_script, self._staging_pre_script) or belongs_to_parent)):
            dct["stagingPreScript"] = dictify(self.staging_pre_script)
        if "staging_post_script" == "type" or (self.staging_post_script is not self.__undef__ and (not (dirty and not self._staging_post_script[1]) or self.is_dirty_list(self.staging_post_script, self._staging_post_script) or belongs_to_parent)):
            dct["stagingPostScript"] = dictify(self.staging_post_script)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._encryption_key = (self._encryption_key[0], True)
        self._sync_parameters = (self._sync_parameters[0], True)
        self._operations = (self._operations[0], True)
        self._source_host_user = (self._source_host_user[0], True)
        self._sync_strategy = (self._sync_strategy[0], True)
        self._ppt_repository = (self._ppt_repository[0], True)
        self._ppt_host_user = (self._ppt_host_user[0], True)
        self._staging_pre_script = (self._staging_pre_script[0], True)
        self._staging_post_script = (self._staging_post_script[0], True)

    def is_dirty(self):
        return any([self._encryption_key[1], self._sync_parameters[1], self._operations[1], self._source_host_user[1], self._sync_strategy[1], self._ppt_repository[1], self._ppt_host_user[1], self._staging_pre_script[1], self._staging_post_script[1]])

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
        if not isinstance(other, MSSqlLinkData):
            return False
        return super().__eq__(other) and \
               self.encryption_key == other.encryption_key and \
               self.sync_parameters == other.sync_parameters and \
               self.operations == other.operations and \
               self.source_host_user == other.source_host_user and \
               self.sync_strategy == other.sync_strategy and \
               self.ppt_repository == other.ppt_repository and \
               self.ppt_host_user == other.ppt_host_user and \
               self.staging_pre_script == other.staging_pre_script and \
               self.staging_post_script == other.staging_post_script

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def encryption_key(self):
        """
        The encryption key to use when restoring encrypted backups.

        :rtype: ``str``
        """
        return self._encryption_key[0]

    @encryption_key.setter
    def encryption_key(self, value):
        self._encryption_key = (value, True)

    @property
    def sync_parameters(self):
        """
        Sync parameters for the container.

        :rtype: :py:class:`v1_11_14.web.vo.MSSqlSyncParameters`
        """
        return self._sync_parameters[0]

    @sync_parameters.setter
    def sync_parameters(self, value):
        self._sync_parameters = (value, True)

    @property
    def operations(self):
        """
        User-specified operation hooks for this source.

        :rtype: :py:class:`v1_11_14.web.vo.LinkedSourceOperations`
        """
        return self._operations[0]

    @operations.setter
    def operations(self, value):
        self._operations = (value, True)

    @property
    def source_host_user(self):
        """
        Information about the host OS user on the source to use for linking.

        :rtype: ``str``
        """
        return self._source_host_user[0]

    @source_host_user.setter
    def source_host_user(self, value):
        self._source_host_user = (value, True)

    @property
    def sync_strategy(self):
        """
        Configuration that determines what sync strategy the source will use
        for linking.

        :rtype: :py:class:`v1_11_14.web.vo.MSSqlSyncStrategy`
        """
        return self._sync_strategy[0]

    @sync_strategy.setter
    def sync_strategy(self, value):
        self._sync_strategy = (value, True)

    @property
    def ppt_repository(self):
        """
        The SQL instance on the PPT environment that we want to use for pre-
        provisioning.

        :rtype: ``str``
        """
        return self._ppt_repository[0]

    @ppt_repository.setter
    def ppt_repository(self, value):
        self._ppt_repository = (value, True)

    @property
    def ppt_host_user(self):
        """
        Information about the host OS user on the PPT host to use for linking.

        :rtype: ``str``
        """
        return self._ppt_host_user[0]

    @ppt_host_user.setter
    def ppt_host_user(self, value):
        self._ppt_host_user = (value, True)

    @property
    def staging_pre_script(self):
        """
        A user-provided PowerShell script or executable to run prior to
        restoring from a backup during pre-provisioning.

        :rtype: ``str``
        """
        return self._staging_pre_script[0]

    @staging_pre_script.setter
    def staging_pre_script(self, value):
        self._staging_pre_script = (value, True)

    @property
    def staging_post_script(self):
        """
        A user-provided PowerShell script or executable to run after restoring
        from a backup during pre-provisioning.

        :rtype: ``str``
        """
        return self._staging_post_script[0]

    @staging_post_script.setter
    def staging_post_script(self, value):
        self._staging_post_script = (value, True)

