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
#     /delphix-s3-object-store.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_20.web.objects.ObjectStore import ObjectStore
from delphixpy.v1_11_20 import factory
from delphixpy.v1_11_20 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class S3ObjectStore(ObjectStore):
    """
    *(extends* :py:class:`v1_11_20.web.vo.ObjectStore` *)* An Amazon Simple
    Storage Service (Amazon S3) object store.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("S3ObjectStore", True)
        self._endpoint = (self.__undef__, True)
        self._region = (self.__undef__, True)
        self._bucket = (self.__undef__, True)
        self._access_credentials = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._endpoint = (data.get("endpoint", obj.__undef__), dirty)
        if obj._endpoint[0] is not None and obj._endpoint[0] is not obj.__undef__:
            assert isinstance(obj._endpoint[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._endpoint[0], type(obj._endpoint[0])))
            common.validate_format(obj._endpoint[0], "None", None, None)
        obj._region = (data.get("region", obj.__undef__), dirty)
        if obj._region[0] is not None and obj._region[0] is not obj.__undef__:
            assert isinstance(obj._region[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._region[0], type(obj._region[0])))
            common.validate_format(obj._region[0], "None", None, None)
        obj._bucket = (data.get("bucket", obj.__undef__), dirty)
        if obj._bucket[0] is not None and obj._bucket[0] is not obj.__undef__:
            assert isinstance(obj._bucket[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bucket[0], type(obj._bucket[0])))
            common.validate_format(obj._bucket[0], "None", 3, 63)
        if "accessCredentials" in data and data["accessCredentials"] is not None:
            obj._access_credentials = (factory.create_object(data["accessCredentials"], "S3ObjectStoreAccess"), dirty)
            factory.validate_type(obj._access_credentials[0], "S3ObjectStoreAccess")
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
        if "region" == "type" or (self.region is not self.__undef__ and (not (dirty and not self._region[1]) or self.is_dirty_list(self.region, self._region) or belongs_to_parent)):
            dct["region"] = dictify(self.region)
        if "bucket" == "type" or (self.bucket is not self.__undef__ and (not (dirty and not self._bucket[1]) or self.is_dirty_list(self.bucket, self._bucket) or belongs_to_parent)):
            dct["bucket"] = dictify(self.bucket)
        if "access_credentials" == "type" or (self.access_credentials is not self.__undef__ and (not (dirty and not self._access_credentials[1]) or self.is_dirty_list(self.access_credentials, self._access_credentials) or belongs_to_parent)):
            dct["accessCredentials"] = dictify(self.access_credentials, prop_is_list_or_vo=True)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._endpoint = (self._endpoint[0], True)
        self._region = (self._region[0], True)
        self._bucket = (self._bucket[0], True)
        self._access_credentials = (self._access_credentials[0], True)

    def is_dirty(self):
        return any([self._endpoint[1], self._region[1], self._bucket[1], self._access_credentials[1]])

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
        if not isinstance(other, S3ObjectStore):
            return False
        return super().__eq__(other) and \
               self.endpoint == other.endpoint and \
               self.region == other.region and \
               self.bucket == other.bucket and \
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
    def region(self):
        """
        The region of the object store.

        :rtype: ``str``
        """
        return self._region[0]

    @region.setter
    def region(self, value):
        self._region = (value, True)

    @property
    def bucket(self):
        """
        The s3 bucket.

        :rtype: ``str``
        """
        return self._bucket[0]

    @bucket.setter
    def bucket(self, value):
        self._bucket = (value, True)

    @property
    def access_credentials(self):
        """
        Access credentials.

        :rtype: :py:class:`v1_11_20.web.vo.S3ObjectStoreAccess`
        """
        return self._access_credentials[0]

    @access_credentials.setter
    def access_credentials(self, value):
        self._access_credentials = (value, True)

