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
#     /delphix-oracle-sourcing-policy.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_39.web.objects.OracleBaseSourcingPolicy import OracleBaseSourcingPolicy
from delphixpy.v1_11_39 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleSourcingPolicy(OracleBaseSourcingPolicy):
    """
    *(extends* :py:class:`v1_11_39.web.vo.OracleBaseSourcingPolicy` *)*
    Database policies for managing SnapSync and LogSync across sources for an
    Oracle container.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleSourcingPolicy", True)
        self._logsync_mode = (self.__undef__, True)
        self._logsync_interval = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._logsync_mode = (data.get("logsyncMode", obj.__undef__), dirty)
        if obj._logsync_mode[0] is not None and obj._logsync_mode[0] is not obj.__undef__:
            assert isinstance(obj._logsync_mode[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._logsync_mode[0], type(obj._logsync_mode[0])))
            assert obj._logsync_mode[0] in ['ARCHIVE_ONLY_MODE', 'ARCHIVE_REDO_MODE', 'UNDEFINED'], "Expected enum ['ARCHIVE_ONLY_MODE', 'ARCHIVE_REDO_MODE', 'UNDEFINED'] but got %s" % obj._logsync_mode[0]
            common.validate_format(obj._logsync_mode[0], "None", None, None)
        obj._logsync_interval = (data.get("logsyncInterval", obj.__undef__), dirty)
        if obj._logsync_interval[0] is not None and obj._logsync_interval[0] is not obj.__undef__:
            assert isinstance(obj._logsync_interval[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._logsync_interval[0], type(obj._logsync_interval[0])))
            common.validate_format(obj._logsync_interval[0], "None", None, None)
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
        if "logsync_mode" == "type" or (self.logsync_mode is not self.__undef__ and (not (dirty and not self._logsync_mode[1]) or self.is_dirty_list(self.logsync_mode, self._logsync_mode) or belongs_to_parent)):
            dct["logsyncMode"] = dictify(self.logsync_mode)
        if "logsync_interval" == "type" or (self.logsync_interval is not self.__undef__ and (not (dirty and not self._logsync_interval[1]) or self.is_dirty_list(self.logsync_interval, self._logsync_interval) or belongs_to_parent)):
            dct["logsyncInterval"] = dictify(self.logsync_interval)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._logsync_mode = (self._logsync_mode[0], True)
        self._logsync_interval = (self._logsync_interval[0], True)

    def is_dirty(self):
        return any([self._logsync_mode[1], self._logsync_interval[1]])

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
        if not isinstance(other, OracleSourcingPolicy):
            return False
        return super().__eq__(other) and \
               self.logsync_mode == other.logsync_mode and \
               self.logsync_interval == other.logsync_interval

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def logsync_mode(self):
        """
        *(default value: UNDEFINED)* LogSync operation mode for this database.
        *(permitted values: ARCHIVE_ONLY_MODE, ARCHIVE_REDO_MODE, UNDEFINED)*

        :rtype: ``str``
        """
        return self._logsync_mode[0]

    @logsync_mode.setter
    def logsync_mode(self, value):
        self._logsync_mode = (value, True)

    @property
    def logsync_interval(self):
        """
        *(default value: 5)* Interval between LogSync requests, in seconds.

        :rtype: ``int``
        """
        return self._logsync_interval[0]

    @logsync_interval.setter
    def logsync_interval(self, value):
        self._logsync_interval = (value, True)

