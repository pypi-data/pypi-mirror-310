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
#     /delphix-dds-component-info.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_22.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_22 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class DelphixDataServicesComponentInfo(TypedObject):
    """
    *(extends* :py:class:`v1_11_22.web.vo.TypedObject` *)* Describes the
    current state of the Delphix Central Management Connector.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("DelphixDataServicesComponentInfo", True)
        self._build_version = (self.__undef__, True)
        self._build_timestamp = (self.__undef__, True)
        self._status = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._build_version = (data.get("buildVersion", obj.__undef__), dirty)
        if obj._build_version[0] is not None and obj._build_version[0] is not obj.__undef__:
            assert isinstance(obj._build_version[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._build_version[0], type(obj._build_version[0])))
            common.validate_format(obj._build_version[0], "None", None, None)
        obj._build_timestamp = (data.get("buildTimestamp", obj.__undef__), dirty)
        if obj._build_timestamp[0] is not None and obj._build_timestamp[0] is not obj.__undef__:
            assert isinstance(obj._build_timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._build_timestamp[0], type(obj._build_timestamp[0])))
            common.validate_format(obj._build_timestamp[0], "date", None, None)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            assert obj._status[0] in ['REGISTERED', 'UNREGISTERED'], "Expected enum ['REGISTERED', 'UNREGISTERED'] but got %s" % obj._status[0]
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
        if "build_version" == "type" or (self.build_version is not self.__undef__ and (not (dirty and not self._build_version[1]))):
            dct["buildVersion"] = dictify(self.build_version)
        if "build_timestamp" == "type" or (self.build_timestamp is not self.__undef__ and (not (dirty and not self._build_timestamp[1]))):
            dct["buildTimestamp"] = dictify(self.build_timestamp)
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._build_version = (self._build_version[0], True)
        self._build_timestamp = (self._build_timestamp[0], True)
        self._status = (self._status[0], True)

    def is_dirty(self):
        return any([self._build_version[1], self._build_timestamp[1], self._status[1]])

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
        if not isinstance(other, DelphixDataServicesComponentInfo):
            return False
        return super().__eq__(other) and \
               self.build_version == other.build_version and \
               self.build_timestamp == other.build_timestamp and \
               self.status == other.status

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def build_version(self):
        """
        The version of the Delphix Central Management Connector.

        :rtype: ``str``
        """
        return self._build_version[0]

    @build_version.setter
    def build_version(self, value):
        self._build_version = (value, True)

    @property
    def build_timestamp(self):
        """
        The time at which the Delphix Central Management Connector was built.

        :rtype: ``str``
        """
        return self._build_timestamp[0]

    @build_timestamp.setter
    def build_timestamp(self, value):
        self._build_timestamp = (value, True)

    @property
    def status(self):
        """
        Indicates the status of the Delphix Central Management Connector.
        *(permitted values: REGISTERED, UNREGISTERED)*

        :rtype: ``str``
        """
        return self._status[0]

    @status.setter
    def status(self, value):
        self._status = (value, True)

