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
#     /delphix-blob-object-store.json
#
# Do not edit this file manually!
#

from delphixpy.web.objects.ObjectStore import ObjectStore
from delphixpy import factory
from delphixpy import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class BlobObjectStore(ObjectStore):
    """
    *(extends* :py:class:`delphixpy.web.vo.ObjectStore` *)* An Azure blob
    object store.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("BlobObjectStore", True)
        self._endpoint = (self.__undef__, True)
        self._container = (self.__undef__, True)
        self._access_credentials = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._endpoint = (data.get("endpoint", obj.__undef__), dirty)
        if obj._endpoint[0] is not None and obj._endpoint[0] is not obj.__undef__:
            assert isinstance(obj._endpoint[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._endpoint[0], type(obj._endpoint[0])))
            common.validate_format(obj._endpoint[0], "None", None, None)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "None", 3, 63)
        if "accessCredentials" in data and data["accessCredentials"] is not None:
            obj._access_credentials = (factory.create_object(data["accessCredentials"], "BlobObjectStoreAccess"), dirty)
            factory.validate_type(obj._access_credentials[0], "BlobObjectStoreAccess")
        else:
            obj._access_credentials = (obj.__undef__, dirty)
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
        if "endpoint" == "type" or (self.endpoint is not self.__undef__ and (not (dirty and not self._endpoint[1]) or self.is_dirty_list(self.endpoint, self._endpoint) or belongs_to_parent)):
            dct["endpoint"] = dictify(self.endpoint)
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]) or self.is_dirty_list(self.container, self._container) or belongs_to_parent)):
            dct["container"] = dictify(self.container)
        if "access_credentials" == "type" or (self.access_credentials is not self.__undef__ and (not (dirty and not self._access_credentials[1]) or self.is_dirty_list(self.access_credentials, self._access_credentials) or belongs_to_parent)):
            dct["accessCredentials"] = dictify(self.access_credentials, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._endpoint = (self._endpoint[0], True)
        self._container = (self._container[0], True)
        self._access_credentials = (self._access_credentials[0], True)

    def is_dirty(self):
        return any([self._endpoint[1], self._container[1], self._access_credentials[1]])

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
        if not isinstance(other, BlobObjectStore):
            return False
        return super().__eq__(other) and \
               self.endpoint == other.endpoint and \
               self.container == other.container and \
               self.access_credentials == other.access_credentials

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def endpoint(self):
        """
        The endpoint of the object store.

        :rtype: ``str``
        """
        return self._endpoint[0]

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = (value, True)

    @property
    def container(self):
        """
        The blob container.

        :rtype: ``str``
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def access_credentials(self):
        """
        Access credentials.

        :rtype: :py:class:`delphixpy.web.vo.BlobObjectStoreAccess`
        """
        return self._access_credentials[0]

    @access_credentials.setter
    def access_credentials(self, value):
        self._access_credentials = (value, True)

