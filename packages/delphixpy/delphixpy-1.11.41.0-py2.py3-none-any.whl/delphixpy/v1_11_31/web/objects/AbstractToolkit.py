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
#     /delphix-abstract-toolkit.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_31.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_31 import factory
from delphixpy.v1_11_31 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class AbstractToolkit(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_31.web.vo.NamedUserObject` *)* An installed
    toolkit.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("AbstractToolkit", True)
        self._identifier = (self.__undef__, True)
        self._display_name = (self.__undef__, True)
        self._version = (self.__undef__, True)
        self._build_api = (self.__undef__, True)
        self._host_types = (self.__undef__, True)
        self._root_squash_enabled = (self.__undef__, True)
        self._default_locale = (self.__undef__, True)
        self._messages = (self.__undef__, True)
        self._snapshot_schema = (self.__undef__, True)
        self._status = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._identifier = (data.get("identifier", obj.__undef__), dirty)
        if obj._identifier[0] is not None and obj._identifier[0] is not obj.__undef__:
            assert isinstance(obj._identifier[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._identifier[0], type(obj._identifier[0])))
            common.validate_format(obj._identifier[0], "None", None, None)
        obj._display_name = (data.get("displayName", obj.__undef__), dirty)
        if obj._display_name[0] is not None and obj._display_name[0] is not obj.__undef__:
            assert isinstance(obj._display_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._display_name[0], type(obj._display_name[0])))
            common.validate_format(obj._display_name[0], "None", None, None)
        obj._version = (data.get("version", obj.__undef__), dirty)
        if obj._version[0] is not None and obj._version[0] is not obj.__undef__:
            assert isinstance(obj._version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._version[0], type(obj._version[0])))
            common.validate_format(obj._version[0], "None", None, None)
        if "buildApi" not in data:
            raise ValueError("Missing required property \"buildApi\".")
        if "buildApi" in data and data["buildApi"] is not None:
            obj._build_api = (factory.create_object(data["buildApi"], "APIVersion"), dirty)
            factory.validate_type(obj._build_api[0], "APIVersion")
        else:
            obj._build_api = (obj.__undef__, dirty)
        if "hostTypes" not in data:
            raise ValueError("Missing required property \"hostTypes\".")
        obj._host_types = []
        for item in data.get("hostTypes") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            assert item in ['UNIX', 'WINDOWS'], "Expected enum ['UNIX', 'WINDOWS'] but got %s" % item
            common.validate_format(item, "None", None, None)
            obj._host_types.append(item)
        obj._host_types = (obj._host_types, dirty)
        obj._root_squash_enabled = (data.get("rootSquashEnabled", obj.__undef__), dirty)
        if obj._root_squash_enabled[0] is not None and obj._root_squash_enabled[0] is not obj.__undef__:
            assert isinstance(obj._root_squash_enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._root_squash_enabled[0], type(obj._root_squash_enabled[0])))
            common.validate_format(obj._root_squash_enabled[0], "None", None, None)
        if "defaultLocale" not in data:
            raise ValueError("Missing required property \"defaultLocale\".")
        obj._default_locale = (data.get("defaultLocale", obj.__undef__), dirty)
        if obj._default_locale[0] is not None and obj._default_locale[0] is not obj.__undef__:
            assert isinstance(obj._default_locale[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._default_locale[0], type(obj._default_locale[0])))
            common.validate_format(obj._default_locale[0], "locale", None, None)
        obj._messages = []
        for item in data.get("messages") or []:
            obj._messages.append(factory.create_object(item))
            factory.validate_type(obj._messages[-1], "ToolkitLocale")
        obj._messages = (obj._messages, dirty)
        if "snapshotSchema" not in data:
            raise ValueError("Missing required property \"snapshotSchema\".")
        if "snapshotSchema" in data and data["snapshotSchema"] is not None:
            obj._snapshot_schema = (data["snapshotSchema"], dirty)
        else:
            obj._snapshot_schema = (obj.__undef__, dirty)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            assert obj._status[0] in ['ACTIVE', 'INACTIVE'], "Expected enum ['ACTIVE', 'INACTIVE'] but got %s" % obj._status[0]
            common.validate_format(obj._status[0], "None", None, None)
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
        if "identifier" == "type" or (self.identifier is not self.__undef__ and (not (dirty and not self._identifier[1]))):
            dct["identifier"] = dictify(self.identifier)
        if dirty and "identifier" in dct:
            del dct["identifier"]
        if "display_name" == "type" or (self.display_name is not self.__undef__ and (not (dirty and not self._display_name[1]))):
            dct["displayName"] = dictify(self.display_name)
        if dirty and "displayName" in dct:
            del dct["displayName"]
        if "version" == "type" or (self.version is not self.__undef__ and (not (dirty and not self._version[1]))):
            dct["version"] = dictify(self.version)
        if dirty and "version" in dct:
            del dct["version"]
        if "build_api" == "type" or (self.build_api is not self.__undef__ and (not (dirty and not self._build_api[1]) or self.is_dirty_list(self.build_api, self._build_api) or belongs_to_parent)):
            dct["buildApi"] = dictify(self.build_api, prop_is_list_or_vo=True)
        if "host_types" == "type" or (self.host_types is not self.__undef__ and (not (dirty and not self._host_types[1]) or self.is_dirty_list(self.host_types, self._host_types) or belongs_to_parent)):
            dct["hostTypes"] = dictify(self.host_types, prop_is_list_or_vo=True)
        if "root_squash_enabled" == "type" or (self.root_squash_enabled is not self.__undef__ and (not (dirty and not self._root_squash_enabled[1]))):
            dct["rootSquashEnabled"] = dictify(self.root_squash_enabled)
        if "default_locale" == "type" or (self.default_locale is not self.__undef__ and (not (dirty and not self._default_locale[1]) or self.is_dirty_list(self.default_locale, self._default_locale) or belongs_to_parent)):
            dct["defaultLocale"] = dictify(self.default_locale)
        if "messages" == "type" or (self.messages is not self.__undef__ and (not (dirty and not self._messages[1]))):
            dct["messages"] = dictify(self.messages)
        if "snapshot_schema" == "type" or (self.snapshot_schema is not self.__undef__ and (not (dirty and not self._snapshot_schema[1]) or self.is_dirty_list(self.snapshot_schema, self._snapshot_schema) or belongs_to_parent)):
            dct["snapshotSchema"] = dictify(self.snapshot_schema, prop_is_list_or_vo=True)
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        if dirty and "status" in dct:
            del dct["status"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._identifier = (self._identifier[0], True)
        self._display_name = (self._display_name[0], True)
        self._version = (self._version[0], True)
        self._build_api = (self._build_api[0], True)
        self._host_types = (self._host_types[0], True)
        self._root_squash_enabled = (self._root_squash_enabled[0], True)
        self._default_locale = (self._default_locale[0], True)
        self._messages = (self._messages[0], True)
        self._snapshot_schema = (self._snapshot_schema[0], True)
        self._status = (self._status[0], True)

    def is_dirty(self):
        return any([self._identifier[1], self._display_name[1], self._version[1], self._build_api[1], self._host_types[1], self._root_squash_enabled[1], self._default_locale[1], self._messages[1], self._snapshot_schema[1], self._status[1]])

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
        if not isinstance(other, AbstractToolkit):
            return False
        return super().__eq__(other) and \
               self.identifier == other.identifier and \
               self.display_name == other.display_name and \
               self.version == other.version and \
               self.build_api == other.build_api and \
               self.host_types == other.host_types and \
               self.root_squash_enabled == other.root_squash_enabled and \
               self.default_locale == other.default_locale and \
               self.messages == other.messages and \
               self.snapshot_schema == other.snapshot_schema and \
               self.status == other.status

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def identifier(self):
        """
        A unique identifier for the toolkit.

        :rtype: ``str``
        """
        return self._identifier[0]

    @property
    def display_name(self):
        """
        A human readable name for the toolkit.

        :rtype: ``str``
        """
        return self._display_name[0]

    @property
    def version(self):
        """
        The version of the toolkit.

        :rtype: ``str``
        """
        return self._version[0]

    @property
    def build_api(self):
        """
        The Delphix API version that the toolkit was built against.

        :rtype: :py:class:`v1_11_31.web.vo.APIVersion`
        """
        return self._build_api[0]

    @build_api.setter
    def build_api(self, value):
        self._build_api = (value, True)

    @property
    def host_types(self):
        """
        A list of host types compatible with this toolkit.

        :rtype: ``list`` of ``str``
        """
        return self._host_types[0]

    @host_types.setter
    def host_types(self, value):
        self._host_types = (value, True)

    @property
    def root_squash_enabled(self):
        """
        Determines if the toolkit supports root squash.

        :rtype: ``bool``
        """
        return self._root_squash_enabled[0]

    @root_squash_enabled.setter
    def root_squash_enabled(self, value):
        self._root_squash_enabled = (value, True)

    @property
    def default_locale(self):
        """
        The default locale for this toolkit. This locale defines the set of all
        message IDs for the toolkit and serves as the fallback locale when
        messages cannot be localized in a particular locale. If no messages are
        specified for the toolkit, the defaultLocale may be any locale.

        :rtype: ``str``
        """
        return self._default_locale[0]

    @default_locale.setter
    def default_locale(self, value):
        self._default_locale = (value, True)

    @property
    def messages(self):
        """
        The set of localizable messages for this toolkit.

        :rtype: ``list`` of :py:class:`v1_11_31.web.vo.ToolkitLocale`
        """
        return self._messages[0]

    @messages.setter
    def messages(self, value):
        self._messages = (value, True)

    @property
    def snapshot_schema(self):
        """
        Schema for metadata collected during snapshotting.

        :rtype: :py:class:`v1_11_31.web.vo.SchemaDraftV4`
        """
        return self._snapshot_schema[0]

    @snapshot_schema.setter
    def snapshot_schema(self, value):
        self._snapshot_schema = (value, True)

    @property
    def status(self):
        """
        The status of the toolkit. ACTIVE indicates toolkit is actively
        referenced and in use. INACTIVE means toolkit needs to go through a
        manual upgrade operation before it can be used. *(permitted values:
        ACTIVE, INACTIVE)*

        :rtype: ``str``
        """
        return self._status[0]

