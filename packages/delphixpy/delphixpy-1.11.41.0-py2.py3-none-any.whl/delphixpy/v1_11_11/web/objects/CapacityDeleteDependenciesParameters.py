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
#     /delphix-capacity-delete-dependencies-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_11 import factory
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class CapacityDeleteDependenciesParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_11.web.vo.TypedObject` *)* The parameters to
    use as input to batch delete objects in a dependency tree.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("CapacityDeleteDependenciesParameters", True)
        self._dependency_tree = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "dependencyTree" not in data:
            raise ValueError("Missing required property \"dependencyTree\".")
        if "dependencyTree" in data and data["dependencyTree"] is not None:
            obj._dependency_tree = (factory.create_object(data["dependencyTree"], "DeletionDependency"), dirty)
            factory.validate_type(obj._dependency_tree[0], "DeletionDependency")
        else:
            obj._dependency_tree = (obj.__undef__, dirty)
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
        if "dependency_tree" == "type" or (self.dependency_tree is not self.__undef__ and (not (dirty and not self._dependency_tree[1]) or self.is_dirty_list(self.dependency_tree, self._dependency_tree) or belongs_to_parent)):
            dct["dependencyTree"] = dictify(self.dependency_tree, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._dependency_tree = (self._dependency_tree[0], True)

    def is_dirty(self):
        return any([self._dependency_tree[1]])

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
        if not isinstance(other, CapacityDeleteDependenciesParameters):
            return False
        return super().__eq__(other) and \
               self.dependency_tree == other.dependency_tree

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def dependency_tree(self):
        """
        Root of the object dependency tree to delete.

        :rtype: :py:class:`v1_11_11.web.vo.DeletionDependency`
        """
        return self._dependency_tree[0]

    @dependency_tree.setter
    def dependency_tree(self, value):
        self._dependency_tree = (value, True)

