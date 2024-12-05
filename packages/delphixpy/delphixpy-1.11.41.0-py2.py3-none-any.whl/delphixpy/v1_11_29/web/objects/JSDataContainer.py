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
#     /delphix-js-data-container.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_29.web.objects.JSDataLayout import JSDataLayout
from delphixpy.v1_11_29 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSDataContainer(JSDataLayout):
    """
    *(extends* :py:class:`v1_11_29.web.vo.JSDataLayout` *)* A container
    represents a data template provisioned for a specific user.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSDataContainer", True)
        self._template = (self.__undef__, True)
        self._state = (self.__undef__, True)
        self._operation_count = (self.__undef__, True)
        self._owner = (self.__undef__, True)
        self._lock_user_reference = (self.__undef__, True)
        self._lock_user_name = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._template = (data.get("template", obj.__undef__), dirty)
        if obj._template[0] is not None and obj._template[0] is not obj.__undef__:
            assert isinstance(obj._template[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._template[0], type(obj._template[0])))
            common.validate_format(obj._template[0], "objectReference", None, None)
        obj._state = (data.get("state", obj.__undef__), dirty)
        if obj._state[0] is not None and obj._state[0] is not obj.__undef__:
            assert isinstance(obj._state[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._state[0], type(obj._state[0])))
            assert obj._state[0] in ['ONLINE', 'OFFLINE', 'INCONSISTENT'], "Expected enum ['ONLINE', 'OFFLINE', 'INCONSISTENT'] but got %s" % obj._state[0]
            common.validate_format(obj._state[0], "None", None, None)
        obj._operation_count = (data.get("operationCount", obj.__undef__), dirty)
        if obj._operation_count[0] is not None and obj._operation_count[0] is not obj.__undef__:
            assert isinstance(obj._operation_count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._operation_count[0], type(obj._operation_count[0])))
            common.validate_format(obj._operation_count[0], "None", None, None)
        obj._owner = (data.get("owner", obj.__undef__), dirty)
        if obj._owner[0] is not None and obj._owner[0] is not obj.__undef__:
            assert isinstance(obj._owner[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._owner[0], type(obj._owner[0])))
            common.validate_format(obj._owner[0], "objectReference", None, None)
        obj._lock_user_reference = (data.get("lockUserReference", obj.__undef__), dirty)
        if obj._lock_user_reference[0] is not None and obj._lock_user_reference[0] is not obj.__undef__:
            assert isinstance(obj._lock_user_reference[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._lock_user_reference[0], type(obj._lock_user_reference[0])))
            common.validate_format(obj._lock_user_reference[0], "objectReference", None, None)
        obj._lock_user_name = (data.get("lockUserName", obj.__undef__), dirty)
        if obj._lock_user_name[0] is not None and obj._lock_user_name[0] is not obj.__undef__:
            assert isinstance(obj._lock_user_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._lock_user_name[0], type(obj._lock_user_name[0])))
            common.validate_format(obj._lock_user_name[0], "None", None, None)
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
        if "template" == "type" or (self.template is not self.__undef__ and (not (dirty and not self._template[1]))):
            dct["template"] = dictify(self.template)
        if "state" == "type" or (self.state is not self.__undef__ and (not (dirty and not self._state[1]))):
            dct["state"] = dictify(self.state)
        if "operation_count" == "type" or (self.operation_count is not self.__undef__ and (not (dirty and not self._operation_count[1]))):
            dct["operationCount"] = dictify(self.operation_count)
        if "owner" == "type" or (self.owner is not self.__undef__ and (not (dirty and not self._owner[1]) or self.is_dirty_list(self.owner, self._owner) or belongs_to_parent)):
            dct["owner"] = dictify(self.owner)
        if "lock_user_reference" == "type" or (self.lock_user_reference is not self.__undef__ and (not (dirty and not self._lock_user_reference[1]))):
            dct["lockUserReference"] = dictify(self.lock_user_reference)
        if "lock_user_name" == "type" or (self.lock_user_name is not self.__undef__ and (not (dirty and not self._lock_user_name[1]))):
            dct["lockUserName"] = dictify(self.lock_user_name)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._template = (self._template[0], True)
        self._state = (self._state[0], True)
        self._operation_count = (self._operation_count[0], True)
        self._owner = (self._owner[0], True)
        self._lock_user_reference = (self._lock_user_reference[0], True)
        self._lock_user_name = (self._lock_user_name[0], True)

    def is_dirty(self):
        return any([self._template[1], self._state[1], self._operation_count[1], self._owner[1], self._lock_user_reference[1], self._lock_user_name[1]])

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
        if not isinstance(other, JSDataContainer):
            return False
        return super().__eq__(other) and \
               self.template == other.template and \
               self.state == other.state and \
               self.operation_count == other.operation_count and \
               self.owner == other.owner and \
               self.lock_user_reference == other.lock_user_reference and \
               self.lock_user_name == other.lock_user_name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def template(self):
        """
        The data template that this data container was provisioned from.

        :rtype: ``str``
        """
        return self._template[0]

    @template.setter
    def template(self, value):
        self._template = (value, True)

    @property
    def state(self):
        """
        The state of the data container. *(permitted values: ONLINE, OFFLINE,
        INCONSISTENT)*

        :rtype: ``str``
        """
        return self._state[0]

    @state.setter
    def state(self, value):
        self._state = (value, True)

    @property
    def operation_count(self):
        """
        The number of operations performed on this data container.

        :rtype: ``int``
        """
        return self._operation_count[0]

    @operation_count.setter
    def operation_count(self, value):
        self._operation_count = (value, True)

    @property
    def owner(self):
        """
        For backward compatibility. The owner of the data container.

        :rtype: ``str`` *or* ``null``
        """
        return self._owner[0]

    @owner.setter
    def owner(self, value):
        self._owner = (value, True)

    @property
    def lock_user_reference(self):
        """
        The reference to the user who locked this data container.

        :rtype: ``str``
        """
        return self._lock_user_reference[0]

    @lock_user_reference.setter
    def lock_user_reference(self, value):
        self._lock_user_reference = (value, True)

    @property
    def lock_user_name(self):
        """
        Name of the user who locked this data container.

        :rtype: ``str``
        """
        return self._lock_user_name[0]

    @lock_user_name.setter
    def lock_user_name(self, value):
        self._lock_user_name = (value, True)

