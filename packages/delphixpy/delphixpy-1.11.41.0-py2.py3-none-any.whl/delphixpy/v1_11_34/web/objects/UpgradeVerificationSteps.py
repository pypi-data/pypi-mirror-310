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
#     /delphix-upgrade-verification-steps.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_34.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_34 import factory
from delphixpy.v1_11_34 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class UpgradeVerificationSteps(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_34.web.vo.NamedUserObject` *)* Describes the
    verification steps of an upgrade verification report.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("UpgradeVerificationSteps", True)
        self._class_name = (self.__undef__, True)
        self._run_status = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._start_timestamp = (self.__undef__, True)
        self._end_timestamp = (self.__undef__, True)
        self._duration = (self.__undef__, True)
        self._run_status_message = (self.__undef__, True)
        self._notifications = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._class_name = (data.get("className", obj.__undef__), dirty)
        if obj._class_name[0] is not None and obj._class_name[0] is not obj.__undef__:
            assert isinstance(obj._class_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._class_name[0], type(obj._class_name[0])))
            common.validate_format(obj._class_name[0], "None", None, None)
        obj._run_status = (data.get("runStatus", obj.__undef__), dirty)
        if obj._run_status[0] is not None and obj._run_status[0] is not obj.__undef__:
            assert isinstance(obj._run_status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._run_status[0], type(obj._run_status[0])))
            assert obj._run_status[0] in ['SUCCESS', 'FAILURE', 'SKIPPED'], "Expected enum ['SUCCESS', 'FAILURE', 'SKIPPED'] but got %s" % obj._run_status[0]
            common.validate_format(obj._run_status[0], "None", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        obj._start_timestamp = (data.get("startTimestamp", obj.__undef__), dirty)
        if obj._start_timestamp[0] is not None and obj._start_timestamp[0] is not obj.__undef__:
            assert isinstance(obj._start_timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_timestamp[0], type(obj._start_timestamp[0])))
            common.validate_format(obj._start_timestamp[0], "None", None, None)
        obj._end_timestamp = (data.get("endTimestamp", obj.__undef__), dirty)
        if obj._end_timestamp[0] is not None and obj._end_timestamp[0] is not obj.__undef__:
            assert isinstance(obj._end_timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._end_timestamp[0], type(obj._end_timestamp[0])))
            common.validate_format(obj._end_timestamp[0], "None", None, None)
        obj._duration = (data.get("duration", obj.__undef__), dirty)
        if obj._duration[0] is not None and obj._duration[0] is not obj.__undef__:
            assert isinstance(obj._duration[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._duration[0], type(obj._duration[0])))
            common.validate_format(obj._duration[0], "None", None, None)
        obj._run_status_message = (data.get("runStatusMessage", obj.__undef__), dirty)
        if obj._run_status_message[0] is not None and obj._run_status_message[0] is not obj.__undef__:
            assert isinstance(obj._run_status_message[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._run_status_message[0], type(obj._run_status_message[0])))
            common.validate_format(obj._run_status_message[0], "None", None, None)
        obj._notifications = []
        for item in data.get("notifications") or []:
            obj._notifications.append(factory.create_object(item))
            factory.validate_type(obj._notifications[-1], "LocalizedUpgradeCheckResult")
        obj._notifications = (obj._notifications, dirty)
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
        if "class_name" == "type" or (self.class_name is not self.__undef__ and (not (dirty and not self._class_name[1]))):
            dct["className"] = dictify(self.class_name)
        if dirty and "className" in dct:
            del dct["className"]
        if "run_status" == "type" or (self.run_status is not self.__undef__ and (not (dirty and not self._run_status[1]))):
            dct["runStatus"] = dictify(self.run_status)
        if dirty and "runStatus" in dct:
            del dct["runStatus"]
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]))):
            dct["description"] = dictify(self.description)
        if dirty and "description" in dct:
            del dct["description"]
        if "start_timestamp" == "type" or (self.start_timestamp is not self.__undef__ and (not (dirty and not self._start_timestamp[1]))):
            dct["startTimestamp"] = dictify(self.start_timestamp)
        if dirty and "startTimestamp" in dct:
            del dct["startTimestamp"]
        if "end_timestamp" == "type" or (self.end_timestamp is not self.__undef__ and (not (dirty and not self._end_timestamp[1]))):
            dct["endTimestamp"] = dictify(self.end_timestamp)
        if dirty and "endTimestamp" in dct:
            del dct["endTimestamp"]
        if "duration" == "type" or (self.duration is not self.__undef__ and (not (dirty and not self._duration[1]))):
            dct["duration"] = dictify(self.duration)
        if dirty and "duration" in dct:
            del dct["duration"]
        if "run_status_message" == "type" or (self.run_status_message is not self.__undef__ and (not (dirty and not self._run_status_message[1]))):
            dct["runStatusMessage"] = dictify(self.run_status_message)
        if dirty and "runStatusMessage" in dct:
            del dct["runStatusMessage"]
        if "notifications" == "type" or (self.notifications is not self.__undef__ and (not (dirty and not self._notifications[1]))):
            dct["notifications"] = dictify(self.notifications)
        if dirty and "notifications" in dct:
            del dct["notifications"]
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._class_name = (self._class_name[0], True)
        self._run_status = (self._run_status[0], True)
        self._description = (self._description[0], True)
        self._start_timestamp = (self._start_timestamp[0], True)
        self._end_timestamp = (self._end_timestamp[0], True)
        self._duration = (self._duration[0], True)
        self._run_status_message = (self._run_status_message[0], True)
        self._notifications = (self._notifications[0], True)

    def is_dirty(self):
        return any([self._class_name[1], self._run_status[1], self._description[1], self._start_timestamp[1], self._end_timestamp[1], self._duration[1], self._run_status_message[1], self._notifications[1]])

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
        if not isinstance(other, UpgradeVerificationSteps):
            return False
        return super().__eq__(other) and \
               self.class_name == other.class_name and \
               self.run_status == other.run_status and \
               self.description == other.description and \
               self.start_timestamp == other.start_timestamp and \
               self.end_timestamp == other.end_timestamp and \
               self.duration == other.duration and \
               self.run_status_message == other.run_status_message and \
               self.notifications == other.notifications

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.class_name,
            self.run_status,
            self.description,
            self.start_timestamp,
            self.end_timestamp,
            self.duration,
            self.run_status_message,
            self.notifications,
        ))

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def class_name(self):
        """
        A unique identifier for each step.

        :rtype: ``str``
        """
        return self._class_name[0]

    @property
    def run_status(self):
        """
        Result status of the step. *(permitted values: SUCCESS, FAILURE,
        SKIPPED)*

        :rtype: ``str``
        """
        return self._run_status[0]

    @property
    def description(self):
        """
        A brief description about the step.

        :rtype: ``str``
        """
        return self._description[0]

    @property
    def start_timestamp(self):
        """
        Start time of the step.

        :rtype: ``str``
        """
        return self._start_timestamp[0]

    @property
    def end_timestamp(self):
        """
        End time off the step.

        :rtype: ``str``
        """
        return self._end_timestamp[0]

    @property
    def duration(self):
        """
        The duration for which the step ran.

        :rtype: ``str``
        """
        return self._duration[0]

    @property
    def run_status_message(self):
        """
        An optional messages from the step.

        :rtype: ``str``
        """
        return self._run_status_message[0]

    @property
    def notifications(self):
        """
        Notification from the steps.

        :rtype: ``list`` of
            :py:class:`v1_11_34.web.vo.LocalizedUpgradeCheckResult`
        """
        return self._notifications[0]

