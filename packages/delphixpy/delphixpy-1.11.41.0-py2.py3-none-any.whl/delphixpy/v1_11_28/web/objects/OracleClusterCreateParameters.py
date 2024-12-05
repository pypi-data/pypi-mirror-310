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
#     /delphix-oracle-cluster-create-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_28.web.objects.SourceEnvironmentCreateParameters import SourceEnvironmentCreateParameters
from delphixpy.v1_11_28 import factory
from delphixpy.v1_11_28 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class OracleClusterCreateParameters(SourceEnvironmentCreateParameters):
    """
    *(extends* :py:class:`v1_11_28.web.vo.SourceEnvironmentCreateParameters`
    *)* The parameters used for the oracle cluster create operation.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("OracleClusterCreateParameters", True)
        self._cluster = (self.__undef__, True)
        self._node = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "cluster" in data and data["cluster"] is not None:
            obj._cluster = (factory.create_object(data["cluster"], "OracleCluster"), dirty)
            factory.validate_type(obj._cluster[0], "OracleCluster")
        else:
            obj._cluster = (obj.__undef__, dirty)
        if "node" in data and data["node"] is not None:
            obj._node = (factory.create_object(data["node"], "OracleClusterNodeCreateParameters"), dirty)
            factory.validate_type(obj._node[0], "OracleClusterNodeCreateParameters")
        else:
            obj._node = (obj.__undef__, dirty)
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
        if "cluster" == "type" or (self.cluster is not self.__undef__ and (not (dirty and not self._cluster[1]) or self.is_dirty_list(self.cluster, self._cluster) or belongs_to_parent)):
            dct["cluster"] = dictify(self.cluster, prop_is_list_or_vo=True)
        if "node" == "type" or (self.node is not self.__undef__ and (not (dirty and not self._node[1]) or self.is_dirty_list(self.node, self._node) or belongs_to_parent)):
            dct["node"] = dictify(self.node, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._cluster = (self._cluster[0], True)
        self._node = (self._node[0], True)

    def is_dirty(self):
        return any([self._cluster[1], self._node[1]])

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
        if not isinstance(other, OracleClusterCreateParameters):
            return False
        return super().__eq__(other) and \
               self.cluster == other.cluster and \
               self.node == other.node

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def cluster(self):
        """
        The representation of the cluster object.

        :rtype: :py:class:`v1_11_28.web.vo.OracleCluster`
        """
        return self._cluster[0]

    @cluster.setter
    def cluster(self, value):
        self._cluster = (value, True)

    @property
    def node(self):
        """
        Only one node is allowed for the add cluster operation. Additional
        nodes will be discovered automatically. Any nodes not discovered by
        Delphix can be manually added after cluster creation.

        :rtype: :py:class:`v1_11_28.web.vo.OracleClusterNodeCreateParameters`
        """
        return self._node[0]

    @node.setter
    def node(self, value):
        self._node = (value, True)

