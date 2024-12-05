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
#     /delphix-job.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_7.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_7 import factory
from delphixpy.v1_11_7 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class Job(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_7.web.vo.NamedUserObject` *)* Represents a job
    object.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("Job", True)
        self._action_type = (self.__undef__, True)
        self._target = (self.__undef__, True)
        self._target_object_type = (self.__undef__, True)
        self._job_state = (self.__undef__, True)
        self._start_time = (self.__undef__, True)
        self._update_time = (self.__undef__, True)
        self._suspendable = (self.__undef__, True)
        self._cancelable = (self.__undef__, True)
        self._queued = (self.__undef__, True)
        self._user = (self.__undef__, True)
        self._email_addresses = (self.__undef__, True)
        self._title = (self.__undef__, True)
        self._cancel_reason = (self.__undef__, True)
        self._percent_complete = (self.__undef__, True)
        self._target_name = (self.__undef__, True)
        self._events = (self.__undef__, True)
        self._parent_action_state = (self.__undef__, True)
        self._parent_action = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._action_type = (data.get("actionType", obj.__undef__), dirty)
        if obj._action_type[0] is not None and obj._action_type[0] is not obj.__undef__:
            assert isinstance(obj._action_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._action_type[0], type(obj._action_type[0])))
            common.validate_format(obj._action_type[0], "None", None, None)
        obj._target = (data.get("target", obj.__undef__), dirty)
        if obj._target[0] is not None and obj._target[0] is not obj.__undef__:
            assert isinstance(obj._target[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target[0], type(obj._target[0])))
            common.validate_format(obj._target[0], "objectReference", None, None)
        obj._target_object_type = (data.get("targetObjectType", obj.__undef__), dirty)
        if obj._target_object_type[0] is not None and obj._target_object_type[0] is not obj.__undef__:
            assert isinstance(obj._target_object_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_object_type[0], type(obj._target_object_type[0])))
            common.validate_format(obj._target_object_type[0], "type", None, None)
        obj._job_state = (data.get("jobState", obj.__undef__), dirty)
        if obj._job_state[0] is not None and obj._job_state[0] is not obj.__undef__:
            assert isinstance(obj._job_state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._job_state[0], type(obj._job_state[0])))
            assert obj._job_state[0] in ['RUNNING', 'SUSPENDED', 'CANCELED', 'COMPLETED', 'FAILED'], "Expected enum ['RUNNING', 'SUSPENDED', 'CANCELED', 'COMPLETED', 'FAILED'] but got %s" % obj._job_state[0]
            common.validate_format(obj._job_state[0], "None", None, None)
        obj._start_time = (data.get("startTime", obj.__undef__), dirty)
        if obj._start_time[0] is not None and obj._start_time[0] is not obj.__undef__:
            assert isinstance(obj._start_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start_time[0], type(obj._start_time[0])))
            common.validate_format(obj._start_time[0], "date", None, None)
        obj._update_time = (data.get("updateTime", obj.__undef__), dirty)
        if obj._update_time[0] is not None and obj._update_time[0] is not obj.__undef__:
            assert isinstance(obj._update_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._update_time[0], type(obj._update_time[0])))
            common.validate_format(obj._update_time[0], "date", None, None)
        obj._suspendable = (data.get("suspendable", obj.__undef__), dirty)
        if obj._suspendable[0] is not None and obj._suspendable[0] is not obj.__undef__:
            assert isinstance(obj._suspendable[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._suspendable[0], type(obj._suspendable[0])))
            common.validate_format(obj._suspendable[0], "None", None, None)
        obj._cancelable = (data.get("cancelable", obj.__undef__), dirty)
        if obj._cancelable[0] is not None and obj._cancelable[0] is not obj.__undef__:
            assert isinstance(obj._cancelable[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._cancelable[0], type(obj._cancelable[0])))
            common.validate_format(obj._cancelable[0], "None", None, None)
        obj._queued = (data.get("queued", obj.__undef__), dirty)
        if obj._queued[0] is not None and obj._queued[0] is not obj.__undef__:
            assert isinstance(obj._queued[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._queued[0], type(obj._queued[0])))
            common.validate_format(obj._queued[0], "None", None, None)
        obj._user = (data.get("user", obj.__undef__), dirty)
        if obj._user[0] is not None and obj._user[0] is not obj.__undef__:
            assert isinstance(obj._user[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._user[0], type(obj._user[0])))
            common.validate_format(obj._user[0], "objectReference", None, None)
        obj._email_addresses = []
        for item in data.get("emailAddresses") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "email", None, None)
            obj._email_addresses.append(item)
        obj._email_addresses = (obj._email_addresses, dirty)
        obj._title = (data.get("title", obj.__undef__), dirty)
        if obj._title[0] is not None and obj._title[0] is not obj.__undef__:
            assert isinstance(obj._title[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._title[0], type(obj._title[0])))
            common.validate_format(obj._title[0], "None", None, None)
        obj._cancel_reason = (data.get("cancelReason", obj.__undef__), dirty)
        if obj._cancel_reason[0] is not None and obj._cancel_reason[0] is not obj.__undef__:
            assert isinstance(obj._cancel_reason[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._cancel_reason[0], type(obj._cancel_reason[0])))
            common.validate_format(obj._cancel_reason[0], "None", None, None)
        obj._percent_complete = (data.get("percentComplete", obj.__undef__), dirty)
        if obj._percent_complete[0] is not None and obj._percent_complete[0] is not obj.__undef__:
            assert isinstance(obj._percent_complete[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._percent_complete[0], type(obj._percent_complete[0])))
            common.validate_format(obj._percent_complete[0], "None", None, None)
        obj._target_name = (data.get("targetName", obj.__undef__), dirty)
        if obj._target_name[0] is not None and obj._target_name[0] is not obj.__undef__:
            assert isinstance(obj._target_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_name[0], type(obj._target_name[0])))
            common.validate_format(obj._target_name[0], "None", None, None)
        obj._events = []
        for item in data.get("events") or []:
            obj._events.append(factory.create_object(item))
            factory.validate_type(obj._events[-1], "JobEvent")
        obj._events = (obj._events, dirty)
        obj._parent_action_state = (data.get("parentActionState", obj.__undef__), dirty)
        if obj._parent_action_state[0] is not None and obj._parent_action_state[0] is not obj.__undef__:
            assert isinstance(obj._parent_action_state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent_action_state[0], type(obj._parent_action_state[0])))
            assert obj._parent_action_state[0] in ['EXECUTING', 'WAITING', 'COMPLETED', 'FAILED', 'CANCELED'], "Expected enum ['EXECUTING', 'WAITING', 'COMPLETED', 'FAILED', 'CANCELED'] but got %s" % obj._parent_action_state[0]
            common.validate_format(obj._parent_action_state[0], "None", None, None)
        obj._parent_action = (data.get("parentAction", obj.__undef__), dirty)
        if obj._parent_action[0] is not None and obj._parent_action[0] is not obj.__undef__:
            assert isinstance(obj._parent_action[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._parent_action[0], type(obj._parent_action[0])))
            common.validate_format(obj._parent_action[0], "objectReference", None, None)
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
        if "action_type" == "type" or (self.action_type is not self.__undef__ and (not (dirty and not self._action_type[1]))):
            dct["actionType"] = dictify(self.action_type)
        if "target" == "type" or (self.target is not self.__undef__ and (not (dirty and not self._target[1]))):
            dct["target"] = dictify(self.target)
        if "target_object_type" == "type" or (self.target_object_type is not self.__undef__ and (not (dirty and not self._target_object_type[1]))):
            dct["targetObjectType"] = dictify(self.target_object_type)
        if "job_state" == "type" or (self.job_state is not self.__undef__ and (not (dirty and not self._job_state[1]))):
            dct["jobState"] = dictify(self.job_state)
        if "start_time" == "type" or (self.start_time is not self.__undef__ and (not (dirty and not self._start_time[1]))):
            dct["startTime"] = dictify(self.start_time)
        if "update_time" == "type" or (self.update_time is not self.__undef__ and (not (dirty and not self._update_time[1]))):
            dct["updateTime"] = dictify(self.update_time)
        if "suspendable" == "type" or (self.suspendable is not self.__undef__ and (not (dirty and not self._suspendable[1]))):
            dct["suspendable"] = dictify(self.suspendable)
        if "cancelable" == "type" or (self.cancelable is not self.__undef__ and (not (dirty and not self._cancelable[1]))):
            dct["cancelable"] = dictify(self.cancelable)
        if "queued" == "type" or (self.queued is not self.__undef__ and (not (dirty and not self._queued[1]))):
            dct["queued"] = dictify(self.queued)
        if "user" == "type" or (self.user is not self.__undef__ and (not (dirty and not self._user[1]))):
            dct["user"] = dictify(self.user)
        if "email_addresses" == "type" or (self.email_addresses is not self.__undef__ and (not (dirty and not self._email_addresses[1]) or self.is_dirty_list(self.email_addresses, self._email_addresses) or belongs_to_parent)):
            dct["emailAddresses"] = dictify(self.email_addresses, prop_is_list_or_vo=True)
        if "title" == "type" or (self.title is not self.__undef__ and (not (dirty and not self._title[1]))):
            dct["title"] = dictify(self.title)
        if "cancel_reason" == "type" or (self.cancel_reason is not self.__undef__ and (not (dirty and not self._cancel_reason[1]))):
            dct["cancelReason"] = dictify(self.cancel_reason)
        if "percent_complete" == "type" or (self.percent_complete is not self.__undef__ and (not (dirty and not self._percent_complete[1]))):
            dct["percentComplete"] = dictify(self.percent_complete)
        if "target_name" == "type" or (self.target_name is not self.__undef__ and (not (dirty and not self._target_name[1]))):
            dct["targetName"] = dictify(self.target_name)
        if "events" == "type" or (self.events is not self.__undef__ and (not (dirty and not self._events[1]))):
            dct["events"] = dictify(self.events)
        if "parent_action_state" == "type" or (self.parent_action_state is not self.__undef__ and (not (dirty and not self._parent_action_state[1]))):
            dct["parentActionState"] = dictify(self.parent_action_state)
        if "parent_action" == "type" or (self.parent_action is not self.__undef__ and (not (dirty and not self._parent_action[1]))):
            dct["parentAction"] = dictify(self.parent_action)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._action_type = (self._action_type[0], True)
        self._target = (self._target[0], True)
        self._target_object_type = (self._target_object_type[0], True)
        self._job_state = (self._job_state[0], True)
        self._start_time = (self._start_time[0], True)
        self._update_time = (self._update_time[0], True)
        self._suspendable = (self._suspendable[0], True)
        self._cancelable = (self._cancelable[0], True)
        self._queued = (self._queued[0], True)
        self._user = (self._user[0], True)
        self._email_addresses = (self._email_addresses[0], True)
        self._title = (self._title[0], True)
        self._cancel_reason = (self._cancel_reason[0], True)
        self._percent_complete = (self._percent_complete[0], True)
        self._target_name = (self._target_name[0], True)
        self._events = (self._events[0], True)
        self._parent_action_state = (self._parent_action_state[0], True)
        self._parent_action = (self._parent_action[0], True)

    def is_dirty(self):
        return any([self._action_type[1], self._target[1], self._target_object_type[1], self._job_state[1], self._start_time[1], self._update_time[1], self._suspendable[1], self._cancelable[1], self._queued[1], self._user[1], self._email_addresses[1], self._title[1], self._cancel_reason[1], self._percent_complete[1], self._target_name[1], self._events[1], self._parent_action_state[1], self._parent_action[1]])

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
        if not isinstance(other, Job):
            return False
        return super().__eq__(other) and \
               self.action_type == other.action_type and \
               self.target == other.target and \
               self.target_object_type == other.target_object_type and \
               self.job_state == other.job_state and \
               self.start_time == other.start_time and \
               self.update_time == other.update_time and \
               self.suspendable == other.suspendable and \
               self.cancelable == other.cancelable and \
               self.queued == other.queued and \
               self.user == other.user and \
               self.email_addresses == other.email_addresses and \
               self.title == other.title and \
               self.cancel_reason == other.cancel_reason and \
               self.percent_complete == other.percent_complete and \
               self.target_name == other.target_name and \
               self.events == other.events and \
               self.parent_action_state == other.parent_action_state and \
               self.parent_action == other.parent_action

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def action_type(self):
        """
        Action type of the Job.

        :rtype: ``str``
        """
        return self._action_type[0]

    @action_type.setter
    def action_type(self, value):
        self._action_type = (value, True)

    @property
    def target(self):
        """
        Object reference of the target.

        :rtype: ``str``
        """
        return self._target[0]

    @target.setter
    def target(self, value):
        self._target = (value, True)

    @property
    def target_object_type(self):
        """
        Object type of the target.

        :rtype: ``str``
        """
        return self._target_object_type[0]

    @target_object_type.setter
    def target_object_type(self, value):
        self._target_object_type = (value, True)

    @property
    def job_state(self):
        """
        State of the job. *(permitted values: RUNNING, SUSPENDED, CANCELED,
        COMPLETED, FAILED)*

        :rtype: ``str``
        """
        return self._job_state[0]

    @job_state.setter
    def job_state(self, value):
        self._job_state = (value, True)

    @property
    def start_time(self):
        """
        Time the job was created. Note that this is not the time when the job
        started executing.

        :rtype: ``str``
        """
        return self._start_time[0]

    @start_time.setter
    def start_time(self, value):
        self._start_time = (value, True)

    @property
    def update_time(self):
        """
        Time the job was last updated.

        :rtype: ``str``
        """
        return self._update_time[0]

    @update_time.setter
    def update_time(self, value):
        self._update_time = (value, True)

    @property
    def suspendable(self):
        """
        Whether this job can be suspended.

        :rtype: ``bool``
        """
        return self._suspendable[0]

    @suspendable.setter
    def suspendable(self, value):
        self._suspendable = (value, True)

    @property
    def cancelable(self):
        """
        Whether this job can be canceled.

        :rtype: ``bool``
        """
        return self._cancelable[0]

    @cancelable.setter
    def cancelable(self, value):
        self._cancelable = (value, True)

    @property
    def queued(self):
        """
        Whether this job is waiting for resources to be available for its
        execution.

        :rtype: ``bool``
        """
        return self._queued[0]

    @queued.setter
    def queued(self, value):
        self._queued = (value, True)

    @property
    def user(self):
        """
        User that initiated the action.

        :rtype: ``str``
        """
        return self._user[0]

    @user.setter
    def user(self, value):
        self._user = (value, True)

    @property
    def email_addresses(self):
        """
        Email addresses to be notified on job notification alerts.

        :rtype: ``list`` of ``str``
        """
        return self._email_addresses[0]

    @email_addresses.setter
    def email_addresses(self, value):
        self._email_addresses = (value, True)

    @property
    def title(self):
        """
        Title of the job.

        :rtype: ``str``
        """
        return self._title[0]

    @title.setter
    def title(self, value):
        self._title = (value, True)

    @property
    def cancel_reason(self):
        """
        A description of why the job was canceled.

        :rtype: ``str`` *or* ``null``
        """
        return self._cancel_reason[0]

    @cancel_reason.setter
    def cancel_reason(self, value):
        self._cancel_reason = (value, True)

    @property
    def percent_complete(self):
        """
        Completion percentage. This value is a copy of the last event's
        percentComplete. It will be 0 if there are no job events or if the
        events field is not populated while fetching the job.

        :rtype: ``float``
        """
        return self._percent_complete[0]

    @percent_complete.setter
    def percent_complete(self, value):
        self._percent_complete = (value, True)

    @property
    def target_name(self):
        """
        A cached copy of the target object name.

        :rtype: ``str``
        """
        return self._target_name[0]

    @target_name.setter
    def target_name(self, value):
        self._target_name = (value, True)

    @property
    def events(self):
        """
        A list of time-sorted past JobEvent objects associated with this job.

        :rtype: ``list`` of :py:class:`v1_11_7.web.vo.JobEvent`
        """
        return self._events[0]

    @events.setter
    def events(self, value):
        self._events = (value, True)

    @property
    def parent_action_state(self):
        """
        State of this job's parent action. This value is populated only if the
        job is fetched via the plain get API call. *(permitted values:
        EXECUTING, WAITING, COMPLETED, FAILED, CANCELED)*

        :rtype: ``str``
        """
        return self._parent_action_state[0]

    @parent_action_state.setter
    def parent_action_state(self, value):
        self._parent_action_state = (value, True)

    @property
    def parent_action(self):
        """
        This job's parent action.

        :rtype: ``str``
        """
        return self._parent_action[0]

    @parent_action.setter
    def parent_action(self, value):
        self._parent_action = (value, True)

