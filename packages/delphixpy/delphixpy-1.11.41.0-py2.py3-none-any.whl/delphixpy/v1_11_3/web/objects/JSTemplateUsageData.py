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
#     /delphix-js-template-usage-data.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_3.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_3 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class JSTemplateUsageData(TypedObject):
    """
    *(extends* :py:class:`v1_11_3.web.vo.TypedObject` *)* The space usage
    information for a data template.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("JSTemplateUsageData", True)
        self._template = (self.__undef__, True)
        self._total = (self.__undef__, True)
        self._containers = (self.__undef__, True)
        self._bookmarks = (self.__undef__, True)
        self._unvirtualized = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._template = (data.get("template", obj.__undef__), dirty)
        if obj._template[0] is not None and obj._template[0] is not obj.__undef__:
            assert isinstance(obj._template[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._template[0], type(obj._template[0])))
            common.validate_format(obj._template[0], "objectReference", None, None)
        obj._total = (data.get("total", obj.__undef__), dirty)
        if obj._total[0] is not None and obj._total[0] is not obj.__undef__:
            assert isinstance(obj._total[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._total[0], type(obj._total[0])))
            common.validate_format(obj._total[0], "None", None, None)
        obj._containers = (data.get("containers", obj.__undef__), dirty)
        if obj._containers[0] is not None and obj._containers[0] is not obj.__undef__:
            assert isinstance(obj._containers[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._containers[0], type(obj._containers[0])))
            common.validate_format(obj._containers[0], "None", None, None)
        obj._bookmarks = (data.get("bookmarks", obj.__undef__), dirty)
        if obj._bookmarks[0] is not None and obj._bookmarks[0] is not obj.__undef__:
            assert isinstance(obj._bookmarks[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._bookmarks[0], type(obj._bookmarks[0])))
            common.validate_format(obj._bookmarks[0], "None", None, None)
        obj._unvirtualized = (data.get("unvirtualized", obj.__undef__), dirty)
        if obj._unvirtualized[0] is not None and obj._unvirtualized[0] is not obj.__undef__:
            assert isinstance(obj._unvirtualized[0], float), ("Expected one of ['number'], but got %s of type %s" % (obj._unvirtualized[0], type(obj._unvirtualized[0])))
            common.validate_format(obj._unvirtualized[0], "None", None, None)
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
        if "total" == "type" or (self.total is not self.__undef__ and (not (dirty and not self._total[1]))):
            dct["total"] = dictify(self.total)
        if "containers" == "type" or (self.containers is not self.__undef__ and (not (dirty and not self._containers[1]))):
            dct["containers"] = dictify(self.containers)
        if "bookmarks" == "type" or (self.bookmarks is not self.__undef__ and (not (dirty and not self._bookmarks[1]))):
            dct["bookmarks"] = dictify(self.bookmarks)
        if "unvirtualized" == "type" or (self.unvirtualized is not self.__undef__ and (not (dirty and not self._unvirtualized[1]))):
            dct["unvirtualized"] = dictify(self.unvirtualized)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._template = (self._template[0], True)
        self._total = (self._total[0], True)
        self._containers = (self._containers[0], True)
        self._bookmarks = (self._bookmarks[0], True)
        self._unvirtualized = (self._unvirtualized[0], True)

    def is_dirty(self):
        return any([self._template[1], self._total[1], self._containers[1], self._bookmarks[1], self._unvirtualized[1]])

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
        if not isinstance(other, JSTemplateUsageData):
            return False
        return super().__eq__(other) and \
               self.template == other.template and \
               self.total == other.total and \
               self.containers == other.containers and \
               self.bookmarks == other.bookmarks and \
               self.unvirtualized == other.unvirtualized

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def template(self):
        """
        The data template that this usage information is for.

        :rtype: ``str``
        """
        return self._template[0]

    @template.setter
    def template(self, value):
        self._template = (value, True)

    @property
    def total(self):
        """
        The space that will be freed up if this template (and all of its child
        data containers are deleted).

        :rtype: ``float``
        """
        return self._total[0]

    @total.setter
    def total(self, value):
        self._total = (value, True)

    @property
    def containers(self):
        """
        The amount of space consumed by data containers that were provisioned
        from this data template. This is the space that will be freed up if all
        of those data containers are deleted or purged. This assumes that the
        data containers are deleted along with underlying data sources.

        :rtype: ``float``
        """
        return self._containers[0]

    @containers.setter
    def containers(self, value):
        self._containers = (value, True)

    @property
    def bookmarks(self):
        """
        The amount of space consumed by the bookmarks on this data template.
        This is the space that will be freed up if all bookmarks on the
        template were deleted. This presumes that all of child data containers
        are purged first.

        :rtype: ``float``
        """
        return self._bookmarks[0]

    @bookmarks.setter
    def bookmarks(self, value):
        self._bookmarks = (value, True)

    @property
    def unvirtualized(self):
        """
        The amount of space that would be consumed by the data in this template
        (and child containers) without Delphix.

        :rtype: ``float``
        """
        return self._unvirtualized[0]

    @unvirtualized.setter
    def unvirtualized(self, value):
        self._unvirtualized = (value, True)

