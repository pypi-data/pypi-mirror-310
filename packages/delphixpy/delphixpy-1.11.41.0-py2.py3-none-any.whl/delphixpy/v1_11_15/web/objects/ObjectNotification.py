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
#     /delphix-object-notification.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_15.web.objects.Notification import Notification
from delphixpy.v1_11_15 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ObjectNotification(Notification):
    """
    *(extends* :py:class:`v1_11_15.web.vo.Notification` *)* An event indicating
    a change to an object on the system.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ObjectNotification", True)
        self._object = (self.__undef__, True)
        self._object_type = (self.__undef__, True)
        self._event_type = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._object = (data.get("object", obj.__undef__), dirty)
        if obj._object[0] is not None and obj._object[0] is not obj.__undef__:
            assert isinstance(obj._object[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._object[0], type(obj._object[0])))
            common.validate_format(obj._object[0], "objectReference", None, None)
        obj._object_type = (data.get("objectType", obj.__undef__), dirty)
        if obj._object_type[0] is not None and obj._object_type[0] is not obj.__undef__:
            assert isinstance(obj._object_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._object_type[0], type(obj._object_type[0])))
            common.validate_format(obj._object_type[0], "type", None, None)
        obj._event_type = (data.get("eventType", obj.__undef__), dirty)
        if obj._event_type[0] is not None and obj._event_type[0] is not obj.__undef__:
            assert isinstance(obj._event_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._event_type[0], type(obj._event_type[0])))
            assert obj._event_type[0] in ['CREATE', 'UPDATE', 'DELETE'], "Expected enum ['CREATE', 'UPDATE', 'DELETE'] but got %s" % obj._event_type[0]
            common.validate_format(obj._event_type[0], "None", None, None)
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
        if "object" == "type" or (self.object is not self.__undef__ and (not (dirty and not self._object[1]))):
            dct["object"] = dictify(self.object)
        if "object_type" == "type" or (self.object_type is not self.__undef__ and (not (dirty and not self._object_type[1]))):
            dct["objectType"] = dictify(self.object_type)
        if "event_type" == "type" or (self.event_type is not self.__undef__ and (not (dirty and not self._event_type[1]))):
            dct["eventType"] = dictify(self.event_type)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._object = (self._object[0], True)
        self._object_type = (self._object_type[0], True)
        self._event_type = (self._event_type[0], True)

    def is_dirty(self):
        return any([self._object[1], self._object_type[1], self._event_type[1]])

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
        if not isinstance(other, ObjectNotification):
            return False
        return super().__eq__(other) and \
               self.object == other.object and \
               self.object_type == other.object_type and \
               self.event_type == other.event_type

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def object(self):
        """
        Target object reference.

        :rtype: ``str``
        """
        return self._object[0]

    @object.setter
    def object(self, value):
        self._object = (value, True)

    @property
    def object_type(self):
        """
        Type of target object.

        :rtype: ``str``
        """
        return self._object_type[0]

    @object_type.setter
    def object_type(self, value):
        self._object_type = (value, True)

    @property
    def event_type(self):
        """
        Type of operation on the object. *(permitted values: CREATE, UPDATE,
        DELETE)*

        :rtype: ``str``
        """
        return self._event_type[0]

    @event_type.setter
    def event_type(self, value):
        self._event_type = (value, True)

