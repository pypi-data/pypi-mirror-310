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
#     /delphix-oracle-live-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_40.web.objects.OracleVirtualSource import OracleVirtualSource
from delphixpy.v1_11_40 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleLiveSource(OracleVirtualSource):
    """
    *(extends* :py:class:`v1_11_40.web.vo.OracleVirtualSource` *)* An Oracle
    LiveSource.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleLiveSource", True)
        self._data_age_warning_threshold = (self.__undef__, True)
        self._resync_status = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._data_age_warning_threshold = (data.get("dataAgeWarningThreshold", obj.__undef__), dirty)
        if obj._data_age_warning_threshold[0] is not None and obj._data_age_warning_threshold[0] is not obj.__undef__:
            assert isinstance(obj._data_age_warning_threshold[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._data_age_warning_threshold[0], type(obj._data_age_warning_threshold[0])))
            common.validate_format(obj._data_age_warning_threshold[0], "None", None, None)
        obj._resync_status = (data.get("resyncStatus", obj.__undef__), dirty)
        if obj._resync_status[0] is not None and obj._resync_status[0] is not obj.__undef__:
            assert isinstance(obj._resync_status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._resync_status[0], type(obj._resync_status[0])))
            assert obj._resync_status[0] in ['RESYNC_NOT_REQUIRED', 'RESYNC_NEEDED', 'RESYNC_IN_PROGRESS', 'APPLY_READY', 'APPLY_IN_PROGRESS', 'APPLY_FAILED'], "Expected enum ['RESYNC_NOT_REQUIRED', 'RESYNC_NEEDED', 'RESYNC_IN_PROGRESS', 'APPLY_READY', 'APPLY_IN_PROGRESS', 'APPLY_FAILED'] but got %s" % obj._resync_status[0]
            common.validate_format(obj._resync_status[0], "None", None, None)
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
        if "data_age_warning_threshold" == "type" or (self.data_age_warning_threshold is not self.__undef__ and (not (dirty and not self._data_age_warning_threshold[1]) or self.is_dirty_list(self.data_age_warning_threshold, self._data_age_warning_threshold) or belongs_to_parent)):
            dct["dataAgeWarningThreshold"] = dictify(self.data_age_warning_threshold)
        elif belongs_to_parent and self.data_age_warning_threshold is self.__undef__:
            dct["dataAgeWarningThreshold"] = 900
        if "resync_status" == "type" or (self.resync_status is not self.__undef__ and (not (dirty and not self._resync_status[1]))):
            dct["resyncStatus"] = dictify(self.resync_status)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._data_age_warning_threshold = (self._data_age_warning_threshold[0], True)
        self._resync_status = (self._resync_status[0], True)

    def is_dirty(self):
        return any([self._data_age_warning_threshold[1], self._resync_status[1]])

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
        if not isinstance(other, OracleLiveSource):
            return False
        return super().__eq__(other) and \
               self.data_age_warning_threshold == other.data_age_warning_threshold and \
               self.resync_status == other.resync_status

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def data_age_warning_threshold(self):
        """
        *(default value: 900)* Amount of tolerable delay for this Oracle
        LiveSource in seconds.

        :rtype: ``int``
        """
        return self._data_age_warning_threshold[0]

    @data_age_warning_threshold.setter
    def data_age_warning_threshold(self, value):
        self._data_age_warning_threshold = (value, True)

    @property
    def resync_status(self):
        """
        Resync status for this Oracle LiveSource. *(permitted values:
        RESYNC_NOT_REQUIRED, RESYNC_NEEDED, RESYNC_IN_PROGRESS, APPLY_READY,
        APPLY_IN_PROGRESS, APPLY_FAILED)*

        :rtype: ``str``
        """
        return self._resync_status[0]

    @resync_status.setter
    def resync_status(self, value):
        self._resync_status = (value, True)

