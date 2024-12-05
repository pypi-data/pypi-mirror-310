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
#     /delphix-mssql-staging-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.MSSqlSource import MSSqlSource
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class MSSqlStagingSource(MSSqlSource):
    """
    *(extends* :py:class:`v1_11_21.web.vo.MSSqlSource` *)* An MSSQL staging
    source used for pre-provisioning.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("MSSqlStagingSource", True)
        self._mount_base = (self.__undef__, True)
        self._pre_script = (self.__undef__, True)
        self._post_script = (self.__undef__, True)
        self._config = (self.__undef__, True)
        self._locked = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._mount_base = (data.get("mountBase", obj.__undef__), dirty)
        if obj._mount_base[0] is not None and obj._mount_base[0] is not obj.__undef__:
            assert isinstance(obj._mount_base[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_base[0], type(obj._mount_base[0])))
            common.validate_format(obj._mount_base[0], "None", None, None)
        obj._pre_script = (data.get("preScript", obj.__undef__), dirty)
        if obj._pre_script[0] is not None and obj._pre_script[0] is not obj.__undef__:
            assert isinstance(obj._pre_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pre_script[0], type(obj._pre_script[0])))
            common.validate_format(obj._pre_script[0], "None", None, 1024)
        obj._post_script = (data.get("postScript", obj.__undef__), dirty)
        if obj._post_script[0] is not None and obj._post_script[0] is not obj.__undef__:
            assert isinstance(obj._post_script[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._post_script[0], type(obj._post_script[0])))
            common.validate_format(obj._post_script[0], "None", None, 1024)
        obj._config = (data.get("config", obj.__undef__), dirty)
        if obj._config[0] is not None and obj._config[0] is not obj.__undef__:
            assert isinstance(obj._config[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._config[0], type(obj._config[0])))
            common.validate_format(obj._config[0], "objectReference", None, None)
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
        if "mount_base" == "type" or (self.mount_base is not self.__undef__ and (not (dirty and not self._mount_base[1]))):
            dct["mountBase"] = dictify(self.mount_base)
        if "pre_script" == "type" or (self.pre_script is not self.__undef__ and (not (dirty and not self._pre_script[1]) or self.is_dirty_list(self.pre_script, self._pre_script) or belongs_to_parent)):
            dct["preScript"] = dictify(self.pre_script)
        if "post_script" == "type" or (self.post_script is not self.__undef__ and (not (dirty and not self._post_script[1]) or self.is_dirty_list(self.post_script, self._post_script) or belongs_to_parent)):
            dct["postScript"] = dictify(self.post_script)
        if "config" == "type" or (self.config is not self.__undef__ and (not (dirty and not self._config[1]) or self.is_dirty_list(self.config, self._config) or belongs_to_parent)):
            dct["config"] = dictify(self.config)
        if "locked" == "type" or (self.locked is not self.__undef__ and (not (dirty and not self._locked[1]))):
            dct["locked"] = dictify(self.locked)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._mount_base = (self._mount_base[0], True)
        self._pre_script = (self._pre_script[0], True)
        self._post_script = (self._post_script[0], True)
        self._config = (self._config[0], True)
        self._locked = (self._locked[0], True)

    def is_dirty(self):
        return any([self._mount_base[1], self._pre_script[1], self._post_script[1], self._config[1], self._locked[1]])

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
        if not isinstance(other, MSSqlStagingSource):
            return False
        return super().__eq__(other) and \
               self.mount_base == other.mount_base and \
               self.pre_script == other.pre_script and \
               self.post_script == other.post_script and \
               self.config == other.config and \
               self.locked == other.locked

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def mount_base(self):
        """
        The base mount point for the iSCSI LUN mounts.

        :rtype: ``str``
        """
        return self._mount_base[0]

    @mount_base.setter
    def mount_base(self, value):
        self._mount_base = (value, True)

    @property
    def pre_script(self):
        """
        A user-provided PowerShell script or executable to run prior to
        restoring from a backup during pre-provisioning.

        :rtype: ``str``
        """
        return self._pre_script[0]

    @pre_script.setter
    def pre_script(self, value):
        self._pre_script = (value, True)

    @property
    def post_script(self):
        """
        A user-provided PowerShell script or executable to run after restoring
        from a backup during pre-provisioning.

        :rtype: ``str``
        """
        return self._post_script[0]

    @post_script.setter
    def post_script(self, value):
        self._post_script = (value, True)

    @property
    def config(self):
        """
        Reference to the configuration for the source.

        :rtype: ``str``
        """
        return self._config[0]

    @config.setter
    def config(self, value):
        self._config = (value, True)

    @property
    def locked(self):
        """
        Whether the source is protected from deletion and other data-losing
        actions.

        :rtype: ``bool``
        """
        return self._locked[0]

    @locked.setter
    def locked(self, value):
        self._locked = (value, True)

