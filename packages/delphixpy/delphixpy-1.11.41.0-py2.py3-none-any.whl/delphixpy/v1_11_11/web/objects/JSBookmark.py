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
#     /delphix-js-bookmark.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_11.web.objects.NamedUserObject import NamedUserObject
from delphixpy.v1_11_11 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSBookmark(NamedUserObject):
    """
    *(extends* :py:class:`v1_11_11.web.vo.NamedUserObject` *)* A named entity
    that represents a point in time for all of the data sources in a data
    layout.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSBookmark", True)
        self._branch = (self.__undef__, True)
        self._timestamp = (self.__undef__, True)
        self._description = (self.__undef__, True)
        self._tags = (self.__undef__, True)
        self._shared = (self.__undef__, True)
        self._container = (self.__undef__, True)
        self._template = (self.__undef__, True)
        self._container_name = (self.__undef__, True)
        self._template_name = (self.__undef__, True)
        self._usable = (self.__undef__, True)
        self._checkout_count = (self.__undef__, True)
        self._bookmark_type = (self.__undef__, True)
        self._expiration = (self.__undef__, True)
        self._creation_time = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._branch = (data.get("branch", obj.__undef__), dirty)
        if obj._branch[0] is not None and obj._branch[0] is not obj.__undef__:
            assert isinstance(obj._branch[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._branch[0], type(obj._branch[0])))
            common.validate_format(obj._branch[0], "objectReference", None, None)
        obj._timestamp = (data.get("timestamp", obj.__undef__), dirty)
        if obj._timestamp[0] is not None and obj._timestamp[0] is not obj.__undef__:
            assert isinstance(obj._timestamp[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._timestamp[0], type(obj._timestamp[0])))
            common.validate_format(obj._timestamp[0], "date", None, None)
        obj._description = (data.get("description", obj.__undef__), dirty)
        if obj._description[0] is not None and obj._description[0] is not obj.__undef__:
            assert isinstance(obj._description[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._description[0], type(obj._description[0])))
            common.validate_format(obj._description[0], "None", None, 4096)
        obj._tags = []
        for item in data.get("tags") or []:
            assert isinstance(item, str), ("Expected one of ['string'], but got %s of type %s" % (item, type(item)))
            common.validate_format(item, "None", None, None)
            obj._tags.append(item)
        obj._tags = (obj._tags, dirty)
        obj._shared = (data.get("shared", obj.__undef__), dirty)
        if obj._shared[0] is not None and obj._shared[0] is not obj.__undef__:
            assert isinstance(obj._shared[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._shared[0], type(obj._shared[0])))
            common.validate_format(obj._shared[0], "None", None, None)
        obj._container = (data.get("container", obj.__undef__), dirty)
        if obj._container[0] is not None and obj._container[0] is not obj.__undef__:
            assert isinstance(obj._container[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container[0], type(obj._container[0])))
            common.validate_format(obj._container[0], "objectReference", None, None)
        obj._template = (data.get("template", obj.__undef__), dirty)
        if obj._template[0] is not None and obj._template[0] is not obj.__undef__:
            assert isinstance(obj._template[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._template[0], type(obj._template[0])))
            common.validate_format(obj._template[0], "objectReference", None, None)
        obj._container_name = (data.get("containerName", obj.__undef__), dirty)
        if obj._container_name[0] is not None and obj._container_name[0] is not obj.__undef__:
            assert isinstance(obj._container_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._container_name[0], type(obj._container_name[0])))
            common.validate_format(obj._container_name[0], "None", None, None)
        obj._template_name = (data.get("templateName", obj.__undef__), dirty)
        if obj._template_name[0] is not None and obj._template_name[0] is not obj.__undef__:
            assert isinstance(obj._template_name[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._template_name[0], type(obj._template_name[0])))
            common.validate_format(obj._template_name[0], "None", None, None)
        obj._usable = (data.get("usable", obj.__undef__), dirty)
        if obj._usable[0] is not None and obj._usable[0] is not obj.__undef__:
            assert isinstance(obj._usable[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._usable[0], type(obj._usable[0])))
            common.validate_format(obj._usable[0], "None", None, None)
        obj._checkout_count = (data.get("checkoutCount", obj.__undef__), dirty)
        if obj._checkout_count[0] is not None and obj._checkout_count[0] is not obj.__undef__:
            assert isinstance(obj._checkout_count[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._checkout_count[0], type(obj._checkout_count[0])))
            common.validate_format(obj._checkout_count[0], "None", None, None)
        obj._bookmark_type = (data.get("bookmarkType", obj.__undef__), dirty)
        if obj._bookmark_type[0] is not None and obj._bookmark_type[0] is not obj.__undef__:
            assert isinstance(obj._bookmark_type[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._bookmark_type[0], type(obj._bookmark_type[0])))
            assert obj._bookmark_type[0] in ['DATA_CONTAINER', 'DATA_TEMPLATE'], "Expected enum ['DATA_CONTAINER', 'DATA_TEMPLATE'] but got %s" % obj._bookmark_type[0]
            common.validate_format(obj._bookmark_type[0], "None", None, None)
        obj._expiration = (data.get("expiration", obj.__undef__), dirty)
        if obj._expiration[0] is not None and obj._expiration[0] is not obj.__undef__:
            assert isinstance(obj._expiration[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._expiration[0], type(obj._expiration[0])))
            common.validate_format(obj._expiration[0], "date", None, None)
        obj._creation_time = (data.get("creationTime", obj.__undef__), dirty)
        if obj._creation_time[0] is not None and obj._creation_time[0] is not obj.__undef__:
            assert isinstance(obj._creation_time[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._creation_time[0], type(obj._creation_time[0])))
            common.validate_format(obj._creation_time[0], "date", None, None)
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
        if "branch" == "type" or (self.branch is not self.__undef__ and (not (dirty and not self._branch[1]) or self.is_dirty_list(self.branch, self._branch) or belongs_to_parent)):
            dct["branch"] = dictify(self.branch)
        if "timestamp" == "type" or (self.timestamp is not self.__undef__ and (not (dirty and not self._timestamp[1]))):
            dct["timestamp"] = dictify(self.timestamp)
        if "description" == "type" or (self.description is not self.__undef__ and (not (dirty and not self._description[1]) or self.is_dirty_list(self.description, self._description) or belongs_to_parent)):
            dct["description"] = dictify(self.description)
        if "tags" == "type" or (self.tags is not self.__undef__ and (not (dirty and not self._tags[1]) or self.is_dirty_list(self.tags, self._tags) or belongs_to_parent)):
            dct["tags"] = dictify(self.tags, prop_is_list_or_vo=True)
        if "shared" == "type" or (self.shared is not self.__undef__ and (not (dirty and not self._shared[1]) or self.is_dirty_list(self.shared, self._shared) or belongs_to_parent)):
            dct["shared"] = dictify(self.shared)
        if "container" == "type" or (self.container is not self.__undef__ and (not (dirty and not self._container[1]))):
            dct["container"] = dictify(self.container)
        if "template" == "type" or (self.template is not self.__undef__ and (not (dirty and not self._template[1]))):
            dct["template"] = dictify(self.template)
        if "container_name" == "type" or (self.container_name is not self.__undef__ and (not (dirty and not self._container_name[1]))):
            dct["containerName"] = dictify(self.container_name)
        if "template_name" == "type" or (self.template_name is not self.__undef__ and (not (dirty and not self._template_name[1]))):
            dct["templateName"] = dictify(self.template_name)
        if "usable" == "type" or (self.usable is not self.__undef__ and (not (dirty and not self._usable[1]))):
            dct["usable"] = dictify(self.usable)
        if "checkout_count" == "type" or (self.checkout_count is not self.__undef__ and (not (dirty and not self._checkout_count[1]))):
            dct["checkoutCount"] = dictify(self.checkout_count)
        if "bookmark_type" == "type" or (self.bookmark_type is not self.__undef__ and (not (dirty and not self._bookmark_type[1]))):
            dct["bookmarkType"] = dictify(self.bookmark_type)
        if "expiration" == "type" or (self.expiration is not self.__undef__ and (not (dirty and not self._expiration[1]) or self.is_dirty_list(self.expiration, self._expiration) or belongs_to_parent)):
            dct["expiration"] = dictify(self.expiration)
        if "creation_time" == "type" or (self.creation_time is not self.__undef__ and (not (dirty and not self._creation_time[1]))):
            dct["creationTime"] = dictify(self.creation_time)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._branch = (self._branch[0], True)
        self._timestamp = (self._timestamp[0], True)
        self._description = (self._description[0], True)
        self._tags = (self._tags[0], True)
        self._shared = (self._shared[0], True)
        self._container = (self._container[0], True)
        self._template = (self._template[0], True)
        self._container_name = (self._container_name[0], True)
        self._template_name = (self._template_name[0], True)
        self._usable = (self._usable[0], True)
        self._checkout_count = (self._checkout_count[0], True)
        self._bookmark_type = (self._bookmark_type[0], True)
        self._expiration = (self._expiration[0], True)
        self._creation_time = (self._creation_time[0], True)

    def is_dirty(self):
        return any([self._branch[1], self._timestamp[1], self._description[1], self._tags[1], self._shared[1], self._container[1], self._template[1], self._container_name[1], self._template_name[1], self._usable[1], self._checkout_count[1], self._bookmark_type[1], self._expiration[1], self._creation_time[1]])

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
        if not isinstance(other, JSBookmark):
            return False
        return super().__eq__(other) and \
               self.branch == other.branch and \
               self.timestamp == other.timestamp and \
               self.description == other.description and \
               self.tags == other.tags and \
               self.shared == other.shared and \
               self.container == other.container and \
               self.template == other.template and \
               self.container_name == other.container_name and \
               self.template_name == other.template_name and \
               self.usable == other.usable and \
               self.checkout_count == other.checkout_count and \
               self.bookmark_type == other.bookmark_type and \
               self.expiration == other.expiration and \
               self.creation_time == other.creation_time

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def branch(self):
        """
        A reference to the branch this bookmark applies to.

        :rtype: ``str``
        """
        return self._branch[0]

    @branch.setter
    def branch(self, value):
        self._branch = (value, True)

    @property
    def timestamp(self):
        """
        The timestamp for the data that the bookmark refers to.

        :rtype: ``str``
        """
        return self._timestamp[0]

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = (value, True)

    @property
    def description(self):
        """
        Description of this bookmark.

        :rtype: ``str``
        """
        return self._description[0]

    @description.setter
    def description(self, value):
        self._description = (value, True)

    @property
    def tags(self):
        """
        A set of user-defined labels for this bookmark.

        :rtype: ``list`` of ``str``
        """
        return self._tags[0]

    @tags.setter
    def tags(self, value):
        self._tags = (value, True)

    @property
    def shared(self):
        """
        True if this bookmark is shared.

        :rtype: ``bool``
        """
        return self._shared[0]

    @shared.setter
    def shared(self, value):
        self._shared = (value, True)

    @property
    def container(self):
        """
        The data container this bookmark was created on. This will be null if
        the bookmark was created on a data template.

        :rtype: ``str``
        """
        return self._container[0]

    @container.setter
    def container(self, value):
        self._container = (value, True)

    @property
    def template(self):
        """
        The data template this bookmark was created on or the template of the
        data container this bookmark was created on.

        :rtype: ``str``
        """
        return self._template[0]

    @template.setter
    def template(self, value):
        self._template = (value, True)

    @property
    def container_name(self):
        """
        The name of the data container this bookmark was created on. This will
        be null if the bookmark was created on a data template.

        :rtype: ``str``
        """
        return self._container_name[0]

    @container_name.setter
    def container_name(self, value):
        self._container_name = (value, True)

    @property
    def template_name(self):
        """
        The name of the data template this bookmark was created on or the
        template of the data container this bookmark was created on.

        :rtype: ``str``
        """
        return self._template_name[0]

    @template_name.setter
    def template_name(self, value):
        self._template_name = (value, True)

    @property
    def usable(self):
        """
        True if this bookmark is usable as input to a data operation (e.g.,
        CREATE_BRANCH or RESTORE).

        :rtype: ``bool``
        """
        return self._usable[0]

    @usable.setter
    def usable(self, value):
        self._usable = (value, True)

    @property
    def checkout_count(self):
        """
        The number of times this bookmark has been checked out. This means it
        was used as input to a RESTORE, CREATE_BRANCH, or RESET operation.

        :rtype: ``int``
        """
        return self._checkout_count[0]

    @checkout_count.setter
    def checkout_count(self, value):
        self._checkout_count = (value, True)

    @property
    def bookmark_type(self):
        """
        Denotes whether or not this bookmark was created on a data container or
        a data template. *(permitted values: DATA_CONTAINER, DATA_TEMPLATE)*

        :rtype: ``str``
        """
        return self._bookmark_type[0]

    @bookmark_type.setter
    def bookmark_type(self, value):
        self._bookmark_type = (value, True)

    @property
    def expiration(self):
        """
        A policy will automatically delete this bookmark at this time. If the
        value is null, then the bookmark will be kept until manually deleted.

        :rtype: ``str`` *or* ``null``
        """
        return self._expiration[0]

    @expiration.setter
    def expiration(self, value):
        self._expiration = (value, True)

    @property
    def creation_time(self):
        """
        The time at which the bookmark was created.

        :rtype: ``str``
        """
        return self._creation_time[0]

    @creation_time.setter
    def creation_time(self, value):
        self._creation_time = (value, True)

