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
#     /delphix-toolkit-virtual-source.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_21.web.objects.TypedObject import TypedObject
from delphixpy.v1_11_21 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class ToolkitVirtualSource(TypedObject):
    """
    *(extends* :py:class:`v1_11_21.web.vo.TypedObject` *)* A virtual source
    definition for Lua toolkits.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("ToolkitVirtualSource", True)
        self._parameters = (self.__undef__, True)
        self._configure = (self.__undef__, True)
        self._unconfigure = (self.__undef__, True)
        self._reconfigure = (self.__undef__, True)
        self._initialize = (self.__undef__, True)
        self._start = (self.__undef__, True)
        self._stop = (self.__undef__, True)
        self._pre_snapshot = (self.__undef__, True)
        self._post_snapshot = (self.__undef__, True)
        self._mount_spec = (self.__undef__, True)
        self._ownership_spec = (self.__undef__, True)
        self._status = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        if "parameters" not in data:
            raise ValueError("Missing required property \"parameters\".")
        if "parameters" in data and data["parameters"] is not None:
            obj._parameters = (data["parameters"], dirty)
        else:
            obj._parameters = (obj.__undef__, dirty)
        if "configure" not in data:
            raise ValueError("Missing required property \"configure\".")
        obj._configure = (data.get("configure", obj.__undef__), dirty)
        if obj._configure[0] is not None and obj._configure[0] is not obj.__undef__:
            assert isinstance(obj._configure[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._configure[0], type(obj._configure[0])))
            common.validate_format(obj._configure[0], "None", None, None)
        if "unconfigure" not in data:
            raise ValueError("Missing required property \"unconfigure\".")
        obj._unconfigure = (data.get("unconfigure", obj.__undef__), dirty)
        if obj._unconfigure[0] is not None and obj._unconfigure[0] is not obj.__undef__:
            assert isinstance(obj._unconfigure[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._unconfigure[0], type(obj._unconfigure[0])))
            common.validate_format(obj._unconfigure[0], "None", None, None)
        if "reconfigure" not in data:
            raise ValueError("Missing required property \"reconfigure\".")
        obj._reconfigure = (data.get("reconfigure", obj.__undef__), dirty)
        if obj._reconfigure[0] is not None and obj._reconfigure[0] is not obj.__undef__:
            assert isinstance(obj._reconfigure[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._reconfigure[0], type(obj._reconfigure[0])))
            common.validate_format(obj._reconfigure[0], "None", None, None)
        obj._initialize = (data.get("initialize", obj.__undef__), dirty)
        if obj._initialize[0] is not None and obj._initialize[0] is not obj.__undef__:
            assert isinstance(obj._initialize[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._initialize[0], type(obj._initialize[0])))
            common.validate_format(obj._initialize[0], "None", None, None)
        if "start" not in data:
            raise ValueError("Missing required property \"start\".")
        obj._start = (data.get("start", obj.__undef__), dirty)
        if obj._start[0] is not None and obj._start[0] is not obj.__undef__:
            assert isinstance(obj._start[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._start[0], type(obj._start[0])))
            common.validate_format(obj._start[0], "None", None, None)
        if "stop" not in data:
            raise ValueError("Missing required property \"stop\".")
        obj._stop = (data.get("stop", obj.__undef__), dirty)
        if obj._stop[0] is not None and obj._stop[0] is not obj.__undef__:
            assert isinstance(obj._stop[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._stop[0], type(obj._stop[0])))
            common.validate_format(obj._stop[0], "None", None, None)
        if "preSnapshot" not in data:
            raise ValueError("Missing required property \"preSnapshot\".")
        obj._pre_snapshot = (data.get("preSnapshot", obj.__undef__), dirty)
        if obj._pre_snapshot[0] is not None and obj._pre_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._pre_snapshot[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._pre_snapshot[0], type(obj._pre_snapshot[0])))
            common.validate_format(obj._pre_snapshot[0], "None", None, None)
        if "postSnapshot" not in data:
            raise ValueError("Missing required property \"postSnapshot\".")
        obj._post_snapshot = (data.get("postSnapshot", obj.__undef__), dirty)
        if obj._post_snapshot[0] is not None and obj._post_snapshot[0] is not obj.__undef__:
            assert isinstance(obj._post_snapshot[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._post_snapshot[0], type(obj._post_snapshot[0])))
            common.validate_format(obj._post_snapshot[0], "None", None, None)
        obj._mount_spec = (data.get("mountSpec", obj.__undef__), dirty)
        if obj._mount_spec[0] is not None and obj._mount_spec[0] is not obj.__undef__:
            assert isinstance(obj._mount_spec[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._mount_spec[0], type(obj._mount_spec[0])))
            common.validate_format(obj._mount_spec[0], "None", None, None)
        obj._ownership_spec = (data.get("ownershipSpec", obj.__undef__), dirty)
        if obj._ownership_spec[0] is not None and obj._ownership_spec[0] is not obj.__undef__:
            assert isinstance(obj._ownership_spec[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._ownership_spec[0], type(obj._ownership_spec[0])))
            common.validate_format(obj._ownership_spec[0], "None", None, None)
        obj._status = (data.get("status", obj.__undef__), dirty)
        if obj._status[0] is not None and obj._status[0] is not obj.__undef__:
            assert isinstance(obj._status[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._status[0], type(obj._status[0])))
            common.validate_format(obj._status[0], "None", None, None)
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
        if "parameters" == "type" or (self.parameters is not self.__undef__ and (not (dirty and not self._parameters[1]) or self.is_dirty_list(self.parameters, self._parameters) or belongs_to_parent)):
            dct["parameters"] = dictify(self.parameters, prop_is_list_or_vo=True)
        if "configure" == "type" or (self.configure is not self.__undef__ and (not (dirty and not self._configure[1]) or self.is_dirty_list(self.configure, self._configure) or belongs_to_parent)):
            dct["configure"] = dictify(self.configure)
        if "unconfigure" == "type" or (self.unconfigure is not self.__undef__ and (not (dirty and not self._unconfigure[1]) or self.is_dirty_list(self.unconfigure, self._unconfigure) or belongs_to_parent)):
            dct["unconfigure"] = dictify(self.unconfigure)
        if "reconfigure" == "type" or (self.reconfigure is not self.__undef__ and (not (dirty and not self._reconfigure[1]) or self.is_dirty_list(self.reconfigure, self._reconfigure) or belongs_to_parent)):
            dct["reconfigure"] = dictify(self.reconfigure)
        if "initialize" == "type" or (self.initialize is not self.__undef__ and (not (dirty and not self._initialize[1]))):
            dct["initialize"] = dictify(self.initialize)
        if "start" == "type" or (self.start is not self.__undef__ and (not (dirty and not self._start[1]) or self.is_dirty_list(self.start, self._start) or belongs_to_parent)):
            dct["start"] = dictify(self.start)
        if "stop" == "type" or (self.stop is not self.__undef__ and (not (dirty and not self._stop[1]) or self.is_dirty_list(self.stop, self._stop) or belongs_to_parent)):
            dct["stop"] = dictify(self.stop)
        if "pre_snapshot" == "type" or (self.pre_snapshot is not self.__undef__ and (not (dirty and not self._pre_snapshot[1]) or self.is_dirty_list(self.pre_snapshot, self._pre_snapshot) or belongs_to_parent)):
            dct["preSnapshot"] = dictify(self.pre_snapshot)
        if "post_snapshot" == "type" or (self.post_snapshot is not self.__undef__ and (not (dirty and not self._post_snapshot[1]) or self.is_dirty_list(self.post_snapshot, self._post_snapshot) or belongs_to_parent)):
            dct["postSnapshot"] = dictify(self.post_snapshot)
        if "mount_spec" == "type" or (self.mount_spec is not self.__undef__ and (not (dirty and not self._mount_spec[1]))):
            dct["mountSpec"] = dictify(self.mount_spec)
        if "ownership_spec" == "type" or (self.ownership_spec is not self.__undef__ and (not (dirty and not self._ownership_spec[1]))):
            dct["ownershipSpec"] = dictify(self.ownership_spec)
        if "status" == "type" or (self.status is not self.__undef__ and (not (dirty and not self._status[1]))):
            dct["status"] = dictify(self.status)
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._parameters = (self._parameters[0], True)
        self._configure = (self._configure[0], True)
        self._unconfigure = (self._unconfigure[0], True)
        self._reconfigure = (self._reconfigure[0], True)
        self._initialize = (self._initialize[0], True)
        self._start = (self._start[0], True)
        self._stop = (self._stop[0], True)
        self._pre_snapshot = (self._pre_snapshot[0], True)
        self._post_snapshot = (self._post_snapshot[0], True)
        self._mount_spec = (self._mount_spec[0], True)
        self._ownership_spec = (self._ownership_spec[0], True)
        self._status = (self._status[0], True)

    def is_dirty(self):
        return any([self._parameters[1], self._configure[1], self._unconfigure[1], self._reconfigure[1], self._initialize[1], self._start[1], self._stop[1], self._pre_snapshot[1], self._post_snapshot[1], self._mount_spec[1], self._ownership_spec[1], self._status[1]])

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
        if not isinstance(other, ToolkitVirtualSource):
            return False
        return super().__eq__(other) and \
               self.parameters == other.parameters and \
               self.configure == other.configure and \
               self.unconfigure == other.unconfigure and \
               self.reconfigure == other.reconfigure and \
               self.initialize == other.initialize and \
               self.start == other.start and \
               self.stop == other.stop and \
               self.pre_snapshot == other.pre_snapshot and \
               self.post_snapshot == other.post_snapshot and \
               self.mount_spec == other.mount_spec and \
               self.ownership_spec == other.ownership_spec and \
               self.status == other.status

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def parameters(self):
        """
        A user defined schema for the provisioning parameters.

        :rtype: :py:class:`v1_11_21.web.vo.SchemaDraftV4`
        """
        return self._parameters[0]

    @parameters.setter
    def parameters(self, value):
        self._parameters = (value, True)

    @property
    def configure(self):
        """
        A workflow script run when configuring a virtual copy of the
        application in a new environment.

        :rtype: ``str``
        """
        return self._configure[0]

    @configure.setter
    def configure(self, value):
        self._configure = (value, True)

    @property
    def unconfigure(self):
        """
        A workflow script run when removing a virtual copy of the application
        from an environment (e.g. on delete, disable, or refresh).

        :rtype: ``str``
        """
        return self._unconfigure[0]

    @unconfigure.setter
    def unconfigure(self, value):
        self._unconfigure = (value, True)

    @property
    def reconfigure(self):
        """
        A workflow script run when returning a virtual copy of the appliction
        to an environment that it was previously removed from.

        :rtype: ``str``
        """
        return self._reconfigure[0]

    @reconfigure.setter
    def reconfigure(self, value):
        self._reconfigure = (value, True)

    @property
    def initialize(self):
        """
        A workflow script to run when creating an empty application.

        :rtype: ``str``
        """
        return self._initialize[0]

    @initialize.setter
    def initialize(self, value):
        self._initialize = (value, True)

    @property
    def start(self):
        """
        A workflow script to run when starting a virtual copy of the
        application.

        :rtype: ``str``
        """
        return self._start[0]

    @start.setter
    def start(self, value):
        self._start = (value, True)

    @property
    def stop(self):
        """
        A workflow script to run when stopping a virtual copy of the
        application.

        :rtype: ``str``
        """
        return self._stop[0]

    @stop.setter
    def stop(self, value):
        self._stop = (value, True)

    @property
    def pre_snapshot(self):
        """
        A workflow script to run before taking a snapshot of a virtual copy of
        the application.

        :rtype: ``str``
        """
        return self._pre_snapshot[0]

    @pre_snapshot.setter
    def pre_snapshot(self, value):
        self._pre_snapshot = (value, True)

    @property
    def post_snapshot(self):
        """
        A workflow script to run after taking a snapshot of a virtual copy of
        the application.

        :rtype: ``str``
        """
        return self._post_snapshot[0]

    @post_snapshot.setter
    def post_snapshot(self, value):
        self._post_snapshot = (value, True)

    @property
    def mount_spec(self):
        """
        A workflow script that specifies where the virtual copy of the
        application should be mounted.

        :rtype: ``str``
        """
        return self._mount_spec[0]

    @mount_spec.setter
    def mount_spec(self, value):
        self._mount_spec = (value, True)

    @property
    def ownership_spec(self):
        """
        A workflow script that specifies which user/group should own the files
        inside the virtual copy of the application.

        :rtype: ``str``
        """
        return self._ownership_spec[0]

    @ownership_spec.setter
    def ownership_spec(self, value):
        self._ownership_spec = (value, True)

    @property
    def status(self):
        """
        The workflow script to run to determine if a virtual copy of the
        application is running. The script should output 'ACTIVE' if the
        application is running, 'INACTIVE' if the application is not running,
        and 'UNKNOWN' if the script encounters an unexpected problem.

        :rtype: ``str``
        """
        return self._status[0]

    @status.setter
    def status(self, value):
        self._status = (value, True)

