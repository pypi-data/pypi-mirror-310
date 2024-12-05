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
#     /delphix-repave-prepare-parameters.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_26.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_26 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class RepavePrepareParameters(TypedObject):
    """
    *(extends* :py:class:`v1_11_26.web.vo.TypedObject` *)* The parameters to
    use as input to repave prepare.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("RepavePrepareParameters", True)
        self._ignore_disable_sources_failures = (self.__undef__, True)
        self._enable_sources_on_failure = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._ignore_disable_sources_failures = (data.get("ignoreDisableSourcesFailures", obj.__undef__), dirty)
        if obj._ignore_disable_sources_failures[0] is not None and obj._ignore_disable_sources_failures[0] is not obj.__undef__:
            assert isinstance(obj._ignore_disable_sources_failures[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._ignore_disable_sources_failures[0], type(obj._ignore_disable_sources_failures[0])))
            common.validate_format(obj._ignore_disable_sources_failures[0], "None", None, None)
        obj._enable_sources_on_failure = (data.get("enableSourcesOnFailure", obj.__undef__), dirty)
        if obj._enable_sources_on_failure[0] is not None and obj._enable_sources_on_failure[0] is not obj.__undef__:
            assert isinstance(obj._enable_sources_on_failure[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enable_sources_on_failure[0], type(obj._enable_sources_on_failure[0])))
            common.validate_format(obj._enable_sources_on_failure[0], "None", None, None)
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
        if "ignore_disable_sources_failures" == "type" or (self.ignore_disable_sources_failures is not self.__undef__ and (not (dirty and not self._ignore_disable_sources_failures[1]) or self.is_dirty_list(self.ignore_disable_sources_failures, self._ignore_disable_sources_failures) or belongs_to_parent)):
            dct["ignoreDisableSourcesFailures"] = dictify(self.ignore_disable_sources_failures)
        elif belongs_to_parent and self.ignore_disable_sources_failures is self.__undef__:
            dct["ignoreDisableSourcesFailures"] = False
        if "enable_sources_on_failure" == "type" or (self.enable_sources_on_failure is not self.__undef__ and (not (dirty and not self._enable_sources_on_failure[1]) or self.is_dirty_list(self.enable_sources_on_failure, self._enable_sources_on_failure) or belongs_to_parent)):
            dct["enableSourcesOnFailure"] = dictify(self.enable_sources_on_failure)
        elif belongs_to_parent and self.enable_sources_on_failure is self.__undef__:
            dct["enableSourcesOnFailure"] = False
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._ignore_disable_sources_failures = (self._ignore_disable_sources_failures[0], True)
        self._enable_sources_on_failure = (self._enable_sources_on_failure[0], True)

    def is_dirty(self):
        return any([self._ignore_disable_sources_failures[1], self._enable_sources_on_failure[1]])

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
        if not isinstance(other, RepavePrepareParameters):
            return False
        return super().__eq__(other) and \
               self.ignore_disable_sources_failures == other.ignore_disable_sources_failures and \
               self.enable_sources_on_failure == other.enable_sources_on_failure

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def ignore_disable_sources_failures(self):
        """
        If true, a failure to disable sources will not block the repave.

        :rtype: ``bool``
        """
        return self._ignore_disable_sources_failures[0]

    @ignore_disable_sources_failures.setter
    def ignore_disable_sources_failures(self, value):
        self._ignore_disable_sources_failures = (value, True)

    @property
    def enable_sources_on_failure(self):
        """
        If true, when repave fails at a point where the Delphix management
        stack is still running, data source disabled by repave will be enabled
        again.

        :rtype: ``bool``
        """
        return self._enable_sources_on_failure[0]

    @enable_sources_on_failure.setter
    def enable_sources_on_failure(self, value):
        self._enable_sources_on_failure = (value, True)

