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
#     /delphix-deletion-dependency.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_9.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_9 import factory
from delphixpy.v1_11_9 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class DeletionDependency(TypedObject):
    """
    *(extends* :py:class:`v1_11_9.web.vo.TypedObject` *)* Representation of an
    object that needs to be deleted before the object it depended on can be
    deleted.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("DeletionDependency", True)
        self._target_type = (self.__undef__, True)
        self._target_reference = (self.__undef__, True)
        self._namespace_name = (self.__undef__, True)
        self._display_name = (self.__undef__, True)
        self._prerequisites = (self.__undef__, True)
        self._dependencies = (self.__undef__, True)
        self._size = (self.__undef__, True)
        self._locked = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "targetType" not in data:
            raise ValueError("Missing required property \"targetType\".")
        obj._target_type = (data.get("targetType", obj.__undef__), dirty)
        if obj._target_type[0] is not None and obj._target_type[0] is not obj.__undef__:
            assert isinstance(obj._target_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_type[0], type(obj._target_type[0])))
            assert obj._target_type[0] in ['Timeflow', 'TimeflowSnapshot', 'AllSnapshots', 'JSBookmark', 'TimeflowBookmark', 'HeldSpace', 'JSBranch', 'Container'], "Expected enum ['Timeflow', 'TimeflowSnapshot', 'AllSnapshots', 'JSBookmark', 'TimeflowBookmark', 'HeldSpace', 'JSBranch', 'Container'] but got %s" % obj._target_type[0]
            common.validate_format(obj._target_type[0], "None", None, None)
        if "targetReference" not in data:
            raise ValueError("Missing required property \"targetReference\".")
        obj._target_reference = (data.get("targetReference", obj.__undef__), dirty)
        if obj._target_reference[0] is not None and obj._target_reference[0] is not obj.__undef__:
            assert isinstance(obj._target_reference[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._target_reference[0], type(obj._target_reference[0])))
            common.validate_format(obj._target_reference[0], "None", None, None)
        obj._namespace_name = (data.get("namespaceName", obj.__undef__), dirty)
        if obj._namespace_name[0] is not None and obj._namespace_name[0] is not obj.__undef__:
            assert isinstance(obj._namespace_name[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._namespace_name[0], type(obj._namespace_name[0])))
            common.validate_format(obj._namespace_name[0], "None", None, None)
        obj._display_name = (data.get("displayName", obj.__undef__), dirty)
        if obj._display_name[0] is not None and obj._display_name[0] is not obj.__undef__:
            assert isinstance(obj._display_name[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._display_name[0], type(obj._display_name[0])))
            common.validate_format(obj._display_name[0], "None", None, None)
        obj._prerequisites = []
        for item in data.get("prerequisites") or []:
            obj._prerequisites.append(factory.create_object(item))
            factory.validate_type(obj._prerequisites[-1], "DeletionDependencyPrerequisite")
        obj._prerequisites = (obj._prerequisites, dirty)
        obj._dependencies = []
        for item in data.get("dependencies") or []:
            obj._dependencies.append(factory.create_object(item))
            factory.validate_type(obj._dependencies[-1], "TypedObject")
        obj._dependencies = (obj._dependencies, dirty)
        obj._size = (data.get("size", obj.__undef__), dirty)
        if obj._size[0] is not None and obj._size[0] is not obj.__undef__:
            assert isinstance(obj._size[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._size[0], type(obj._size[0])))
            common.validate_format(obj._size[0], "None", None, None)
        obj._locked = (data.get("locked", obj.__undef__), dirty)
        if obj._locked[0] is not None and obj._locked[0] is not obj.__undef__:
            assert isinstance(obj._locked[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._locked[0], type(obj._locked[0])))
            common.validate_format(obj._locked[0], "None", None, None)
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
        if "target_type" == "type" or (self.target_type is not self.__undef__ and (not (dirty and not self._target_type[1]) or self.is_dirty_list(self.target_type, self._target_type) or belongs_to_parent)):
            dct["targetType"] = dictify(self.target_type)
        if "target_reference" == "type" or (self.target_reference is not self.__undef__ and (not (dirty and not self._target_reference[1]) or self.is_dirty_list(self.target_reference, self._target_reference) or belongs_to_parent)):
            dct["targetReference"] = dictify(self.target_reference)
        if "namespace_name" == "type" or (self.namespace_name is not self.__undef__ and (not (dirty and not self._namespace_name[1]))):
            dct["namespaceName"] = dictify(self.namespace_name)
        if "display_name" == "type" or (self.display_name is not self.__undef__ and (not (dirty and not self._display_name[1]))):
            dct["displayName"] = dictify(self.display_name)
        if "prerequisites" == "type" or (self.prerequisites is not self.__undef__ and (not (dirty and not self._prerequisites[1]))):
            dct["prerequisites"] = dictify(self.prerequisites)
        if "dependencies" == "type" or (self.dependencies is not self.__undef__ and (not (dirty and not self._dependencies[1]))):
            dct["dependencies"] = dictify(self.dependencies)
        if "size" == "type" or (self.size is not self.__undef__ and (not (dirty and not self._size[1]))):
            dct["size"] = dictify(self.size)
        if "locked" == "type" or (self.locked is not self.__undef__ and (not (dirty and not self._locked[1]))):
            dct["locked"] = dictify(self.locked)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._target_type = (self._target_type[0], True)
        self._target_reference = (self._target_reference[0], True)
        self._namespace_name = (self._namespace_name[0], True)
        self._display_name = (self._display_name[0], True)
        self._prerequisites = (self._prerequisites[0], True)
        self._dependencies = (self._dependencies[0], True)
        self._size = (self._size[0], True)
        self._locked = (self._locked[0], True)

    def is_dirty(self):
        return any([self._target_type[1], self._target_reference[1], self._namespace_name[1], self._display_name[1], self._prerequisites[1], self._dependencies[1], self._size[1], self._locked[1]])

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
        if not isinstance(other, DeletionDependency):
            return False
        return super().__eq__(other) and \
               self.target_type == other.target_type and \
               self.target_reference == other.target_reference and \
               self.namespace_name == other.namespace_name and \
               self.display_name == other.display_name and \
               self.prerequisites == other.prerequisites and \
               self.dependencies == other.dependencies and \
               self.size == other.size and \
               self.locked == other.locked

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def target_type(self):
        """
        The type of the dependency object. *(permitted values: Timeflow,
        TimeflowSnapshot, AllSnapshots, JSBookmark, TimeflowBookmark,
        HeldSpace, JSBranch, Container)*

        :rtype: ``str``
        """
        return self._target_type[0]

    @target_type.setter
    def target_type(self, value):
        self._target_type = (value, True)

    @property
    def target_reference(self):
        """
        The reference of the dependency object.

        :rtype: ``str``
        """
        return self._target_reference[0]

    @target_reference.setter
    def target_reference(self, value):
        self._target_reference = (value, True)

    @property
    def namespace_name(self):
        """
        The name of the Namespace this object belongs to.

        :rtype: ``str`` *or* ``null``
        """
        return self._namespace_name[0]

    @namespace_name.setter
    def namespace_name(self, value):
        self._namespace_name = (value, True)

    @property
    def display_name(self):
        """
        The user-facing display name of the dependency object.

        :rtype: ``str`` *or* ``null``
        """
        return self._display_name[0]

    @display_name.setter
    def display_name(self, value):
        self._display_name = (value, True)

    @property
    def prerequisites(self):
        """
        The list of operations that needs to be performed before this object
        can be deleted.

        :rtype: ``list`` of
            :py:class:`v1_11_9.web.vo.DeletionDependencyPrerequisite`
        """
        return self._prerequisites[0]

    @prerequisites.setter
    def prerequisites(self, value):
        self._prerequisites = (value, True)

    @property
    def dependencies(self):
        """
        The list of objects that depends on this object.

        :rtype: ``list`` of :py:class:`v1_11_9.web.vo.TypedObject`
        """
        return self._dependencies[0]

    @dependencies.setter
    def dependencies(self, value):
        self._dependencies = (value, True)

    @property
    def size(self):
        """
        The size of this object.

        :rtype: ``float``
        """
        return self._size[0]

    @size.setter
    def size(self, value):
        self._size = (value, True)

    @property
    def locked(self):
        """
        Whether this object is locked. Set it to true to prevent this object
        from being deleted.

        :rtype: ``bool``
        """
        return self._locked[0]

    @locked.setter
    def locked(self, value):
        self._locked = (value, True)

