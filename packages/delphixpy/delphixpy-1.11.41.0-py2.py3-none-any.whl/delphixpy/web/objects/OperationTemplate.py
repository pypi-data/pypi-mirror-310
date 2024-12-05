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
#     /delphix-operation-template.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.NamedUserObject import NamedUserObject
from delphixpy import factory
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OperationTemplate(NamedUserObject):
    """
    *(extends* :py:class:`delphixpy.web.vo.NamedUserObject` *)* Template for
    commonly used operations.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OperationTemplate", True)
        self._name = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._operation = (self.__undef__, True)
        self._last_updated = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._name = (data.get("name", obj.__undef__), dirty)
        if obj._name[0] is not None and obj._name[0] is not obj.__undef__:
            assert isinstance(obj._name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._name[0], type(obj._name[0])))
            common.validate_format(obj._name[0], "None", 1, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, None)
        if "operation" in data and data["operation"] is not None:
            obj._operation = (factory.create_object(data["operation"], "SourceOperation"), dirty)
            factory.validate_type(obj._operation[0], "SourceOperation")
        else:
            obj._operation = (obj.__undef__, dirty)
        obj._last_updated = (data.get("lastUpdated", obj.__undef__), dirty)
        if obj._last_updated[0] is not None and obj._last_updated[0] is not obj.__undef__:
            assert isinstance(obj._last_updated[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._last_updated[0], type(obj._last_updated[0])))
            common.validate_format(obj._last_updated[0], "date", None, None)
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
        if "name" == "type" or (self.name is not self.__undef__ and (not (dirty and not self._name[1]) or self.is_dirty_list(self.name, self._name) or belongs_to_parent)):
            dct["name"] = dictify(self.name)
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]) or self.is_dirty_list(self.description, self._description) or belongs_to_parent)):
            dct["description"] = dictify(self.description)
        if "operation" == "type" or (self.operation is not self.__undef__ and (not (dirty and not self._operation[1]) or self.is_dirty_list(self.operation, self._operation) or belongs_to_parent)):
            dct["operation"] = dictify(self.operation, prop_is_list_or_vo=True)
        if "last_updated" == "type" or (self.last_updated is not self.__undef__ and (not (dirty and not self._last_updated[1]))):
            dct["lastUpdated"] = dictify(self.last_updated)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._name = (self._name[0], True)
        self._description = (self._description[0], True)
        self._operation = (self._operation[0], True)
        self._last_updated = (self._last_updated[0], True)

    def is_dirty(self):
        return any([self._name[1], self._description[1], self._operation[1], self._last_updated[1]])

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
        if not isinstance(other, OperationTemplate):
            return False
        return super().__eq__(other) and \
               self.name == other.name and \
               self.description == other.description and \
               self.operation == other.operation and \
               self.last_updated == other.last_updated

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def name(self):
        """
        The name clients should use when setting the parameter's value.

        :rtype: ``str``
        """
        return self._name[0]

    @name.setter
    def name(self, value):
        self._name = (value, True)

    @property
    def description(self):
        """
        User provided description for this template.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def operation(self):
        """
        Template contents.

        :rtype: :py:class:`delphixpy.web.vo.SourceOperation`
        """
        return self._operation[0]

    @operation.setter
    def operation(self, value):
        self._operation = (value, True)

    @property
    def last_updated(self):
        """
        Most recently modified time.

        :rtype: ``str``
        """
        return self._last_updated[0]

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated = (value, True)

