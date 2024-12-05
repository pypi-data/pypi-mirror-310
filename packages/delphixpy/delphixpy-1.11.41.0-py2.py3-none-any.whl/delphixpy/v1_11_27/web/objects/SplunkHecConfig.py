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
#     /delphix-splunk-hec-config.json
#
# Do not edit this file manually!
#

from delphixpy.v1_11_27.web.objects.UserObject import UserObject
from delphixpy.v1_11_27 import common

class __Undef:
    def __repr__(self):
        return "undef"

    def __setattr__(self, name, value):
        raise Exception('Cannot modify attributes of __Undef.')

_UNDEFINED = __Undef()

class SplunkHecConfig(UserObject):
    """
    *(extends* :py:class:`v1_11_27.web.vo.UserObject` *)* Splunk HTTP Event
    Collector specific configuration information.
    """
    def __init__(self, undef_enabled=True):
        super().__init__()
        self._type = ("SplunkHecConfig", True)
        self._enabled = (self.__undef__, True)
        self._host = (self.__undef__, True)
        self._hec_port = (self.__undef__, True)
        self._hec_token = (self.__undef__, True)
        self._main_index = (self.__undef__, True)
        self._enable_ssl = (self.__undef__, True)
        self._enable_metrics = (self.__undef__, True)
        self._metrics_index = (self.__undef__, True)
        self._performance_metrics_resolution = (self.__undef__, True)
        self._events_push_frequency = (self.__undef__, True)
        self._metrics_push_frequency = (self.__undef__, True)


    @classmethod
    def from_dict(cls, data, dirty=False, undef_enabled=True):
        obj = super().from_dict(data, dirty, undef_enabled)
        obj._enabled = (data.get("enabled", obj.__undef__), dirty)
        if obj._enabled[0] is not None and obj._enabled[0] is not obj.__undef__:
            assert isinstance(obj._enabled[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enabled[0], type(obj._enabled[0])))
            common.validate_format(obj._enabled[0], "None", None, None)
        obj._host = (data.get("host", obj.__undef__), dirty)
        if obj._host[0] is not None and obj._host[0] is not obj.__undef__:
            assert isinstance(obj._host[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._host[0], type(obj._host[0])))
            common.validate_format(obj._host[0], "None", None, None)
        obj._hec_port = (data.get("hecPort", obj.__undef__), dirty)
        if obj._hec_port[0] is not None and obj._hec_port[0] is not obj.__undef__:
            assert isinstance(obj._hec_port[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._hec_port[0], type(obj._hec_port[0])))
            common.validate_format(obj._hec_port[0], "None", None, None)
        obj._hec_token = (data.get("hecToken", obj.__undef__), dirty)
        if obj._hec_token[0] is not None and obj._hec_token[0] is not obj.__undef__:
            assert isinstance(obj._hec_token[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._hec_token[0], type(obj._hec_token[0])))
            common.validate_format(obj._hec_token[0], "None", None, None)
        obj._main_index = (data.get("mainIndex", obj.__undef__), dirty)
        if obj._main_index[0] is not None and obj._main_index[0] is not obj.__undef__:
            assert isinstance(obj._main_index[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._main_index[0], type(obj._main_index[0])))
            common.validate_format(obj._main_index[0], "None", None, None)
        obj._enable_ssl = (data.get("enableSSL", obj.__undef__), dirty)
        if obj._enable_ssl[0] is not None and obj._enable_ssl[0] is not obj.__undef__:
            assert isinstance(obj._enable_ssl[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enable_ssl[0], type(obj._enable_ssl[0])))
            common.validate_format(obj._enable_ssl[0], "None", None, None)
        obj._enable_metrics = (data.get("enableMetrics", obj.__undef__), dirty)
        if obj._enable_metrics[0] is not None and obj._enable_metrics[0] is not obj.__undef__:
            assert isinstance(obj._enable_metrics[0], bool), ("Expected one of ['boolean'], but got %s of type %s" % (obj._enable_metrics[0], type(obj._enable_metrics[0])))
            common.validate_format(obj._enable_metrics[0], "None", None, None)
        obj._metrics_index = (data.get("metricsIndex", obj.__undef__), dirty)
        if obj._metrics_index[0] is not None and obj._metrics_index[0] is not obj.__undef__:
            assert isinstance(obj._metrics_index[0], str), ("Expected one of ['string', 'null'], but got %s of type %s" % (obj._metrics_index[0], type(obj._metrics_index[0])))
            common.validate_format(obj._metrics_index[0], "None", None, None)
        obj._performance_metrics_resolution = (data.get("performanceMetricsResolution", obj.__undef__), dirty)
        if obj._performance_metrics_resolution[0] is not None and obj._performance_metrics_resolution[0] is not obj.__undef__:
            assert isinstance(obj._performance_metrics_resolution[0], str), ("Expected one of ['string'], but got %s of type %s" % (obj._performance_metrics_resolution[0], type(obj._performance_metrics_resolution[0])))
            assert obj._performance_metrics_resolution[0] in ['SECOND', 'MINUTE'], "Expected enum ['SECOND', 'MINUTE'] but got %s" % obj._performance_metrics_resolution[0]
            common.validate_format(obj._performance_metrics_resolution[0], "None", None, None)
        obj._events_push_frequency = (data.get("eventsPushFrequency", obj.__undef__), dirty)
        if obj._events_push_frequency[0] is not None and obj._events_push_frequency[0] is not obj.__undef__:
            assert isinstance(obj._events_push_frequency[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._events_push_frequency[0], type(obj._events_push_frequency[0])))
            common.validate_format(obj._events_push_frequency[0], "None", None, None)
        obj._metrics_push_frequency = (data.get("metricsPushFrequency", obj.__undef__), dirty)
        if obj._metrics_push_frequency[0] is not None and obj._metrics_push_frequency[0] is not obj.__undef__:
            assert isinstance(obj._metrics_push_frequency[0], int), ("Expected one of ['integer'], but got %s of type %s" % (obj._metrics_push_frequency[0], type(obj._metrics_push_frequency[0])))
            common.validate_format(obj._metrics_push_frequency[0], "None", None, None)
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
        if "enabled" == "type" or (self.enabled is not self.__undef__ and (not (dirty and not self._enabled[1]) or self.is_dirty_list(self.enabled, self._enabled) or belongs_to_parent)):
            dct["enabled"] = dictify(self.enabled)
        elif belongs_to_parent and self.enabled is self.__undef__:
            dct["enabled"] = False
        if "host" == "type" or (self.host is not self.__undef__ and (not (dirty and not self._host[1]) or self.is_dirty_list(self.host, self._host) or belongs_to_parent)):
            dct["host"] = dictify(self.host)
        if "hec_port" == "type" or (self.hec_port is not self.__undef__ and (not (dirty and not self._hec_port[1]) or self.is_dirty_list(self.hec_port, self._hec_port) or belongs_to_parent)):
            dct["hecPort"] = dictify(self.hec_port)
        if "hec_token" == "type" or (self.hec_token is not self.__undef__ and (not (dirty and not self._hec_token[1]) or self.is_dirty_list(self.hec_token, self._hec_token) or belongs_to_parent)):
            dct["hecToken"] = dictify(self.hec_token)
        if "main_index" == "type" or (self.main_index is not self.__undef__ and (not (dirty and not self._main_index[1]) or self.is_dirty_list(self.main_index, self._main_index) or belongs_to_parent)):
            dct["mainIndex"] = dictify(self.main_index)
        if "enable_ssl" == "type" or (self.enable_ssl is not self.__undef__ and (not (dirty and not self._enable_ssl[1]) or self.is_dirty_list(self.enable_ssl, self._enable_ssl) or belongs_to_parent)):
            dct["enableSSL"] = dictify(self.enable_ssl)
        if "enable_metrics" == "type" or (self.enable_metrics is not self.__undef__ and (not (dirty and not self._enable_metrics[1]) or self.is_dirty_list(self.enable_metrics, self._enable_metrics) or belongs_to_parent)):
            dct["enableMetrics"] = dictify(self.enable_metrics)
        elif belongs_to_parent and self.enable_metrics is self.__undef__:
            dct["enableMetrics"] = True
        if "metrics_index" == "type" or (self.metrics_index is not self.__undef__ and (not (dirty and not self._metrics_index[1]) or self.is_dirty_list(self.metrics_index, self._metrics_index) or belongs_to_parent)):
            dct["metricsIndex"] = dictify(self.metrics_index)
        if "performance_metrics_resolution" == "type" or (self.performance_metrics_resolution is not self.__undef__ and (not (dirty and not self._performance_metrics_resolution[1]) or self.is_dirty_list(self.performance_metrics_resolution, self._performance_metrics_resolution) or belongs_to_parent)):
            dct["performanceMetricsResolution"] = dictify(self.performance_metrics_resolution)
        elif belongs_to_parent and self.performance_metrics_resolution is self.__undef__:
            dct["performanceMetricsResolution"] = "MINUTE"
        if "events_push_frequency" == "type" or (self.events_push_frequency is not self.__undef__ and (not (dirty and not self._events_push_frequency[1]) or self.is_dirty_list(self.events_push_frequency, self._events_push_frequency) or belongs_to_parent)):
            dct["eventsPushFrequency"] = dictify(self.events_push_frequency)
        elif belongs_to_parent and self.events_push_frequency is self.__undef__:
            dct["eventsPushFrequency"] = 60
        if "metrics_push_frequency" == "type" or (self.metrics_push_frequency is not self.__undef__ and (not (dirty and not self._metrics_push_frequency[1]) or self.is_dirty_list(self.metrics_push_frequency, self._metrics_push_frequency) or belongs_to_parent)):
            dct["metricsPushFrequency"] = dictify(self.metrics_push_frequency)
        elif belongs_to_parent and self.metrics_push_frequency is self.__undef__:
            dct["metricsPushFrequency"] = 60
        return dct

    def dirty(self):
        return self.from_dict(self.to_dict(dirty=False), dirty=True)

    def force_dirty(self):
        self._enabled = (self._enabled[0], True)
        self._host = (self._host[0], True)
        self._hec_port = (self._hec_port[0], True)
        self._hec_token = (self._hec_token[0], True)
        self._main_index = (self._main_index[0], True)
        self._enable_ssl = (self._enable_ssl[0], True)
        self._enable_metrics = (self._enable_metrics[0], True)
        self._metrics_index = (self._metrics_index[0], True)
        self._performance_metrics_resolution = (self._performance_metrics_resolution[0], True)
        self._events_push_frequency = (self._events_push_frequency[0], True)
        self._metrics_push_frequency = (self._metrics_push_frequency[0], True)

    def is_dirty(self):
        return any([self._enabled[1], self._host[1], self._hec_port[1], self._hec_token[1], self._main_index[1], self._enable_ssl[1], self._enable_metrics[1], self._metrics_index[1], self._performance_metrics_resolution[1], self._events_push_frequency[1], self._metrics_push_frequency[1]])

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
        if not isinstance(other, SplunkHecConfig):
            return False
        return super().__eq__(other) and \
               self.enabled == other.enabled and \
               self.host == other.host and \
               self.hec_port == other.hec_port and \
               self.hec_token == other.hec_token and \
               self.main_index == other.main_index and \
               self.enable_ssl == other.enable_ssl and \
               self.enable_metrics == other.enable_metrics and \
               self.metrics_index == other.metrics_index and \
               self.performance_metrics_resolution == other.performance_metrics_resolution and \
               self.events_push_frequency == other.events_push_frequency and \
               self.metrics_push_frequency == other.metrics_push_frequency

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return common.generate_repr_string(self)

    @property
    def enabled(self):
        """
        Whether we should send Delphix Insight data to Splunk using this
        configuration.

        :rtype: ``bool``
        """
        return self._enabled[0]

    @enabled.setter
    def enabled(self, value):
        self._enabled = (value, True)

    @property
    def host(self):
        """
        Splunk host name or IP address.

        :rtype: ``str``
        """
        return self._host[0]

    @host.setter
    def host(self, value):
        self._host = (value, True)

    @property
    def hec_port(self):
        """
        The TCP port number for the Splunk HTTP Event Collector (HEC).

        :rtype: ``int``
        """
        return self._hec_port[0]

    @hec_port.setter
    def hec_port(self, value):
        self._hec_port = (value, True)

    @property
    def hec_token(self):
        """
        The token for the Splunk HTTP Event Collector (HEC).

        :rtype: ``str``
        """
        return self._hec_token[0]

    @hec_token.setter
    def hec_token(self, value):
        self._hec_token = (value, True)

    @property
    def main_index(self):
        """
        The Splunk Index events will be sent to. Must be set as an allowed
        index for the HEC token.

        :rtype: ``str``
        """
        return self._main_index[0]

    @main_index.setter
    def main_index(self, value):
        self._main_index = (value, True)

    @property
    def enable_ssl(self):
        """
        Whether to use HTTPS to connect to Splunk. This should correspond to
        your HTTP Event Collector settings in Splunk.

        :rtype: ``bool``
        """
        return self._enable_ssl[0]

    @enable_ssl.setter
    def enable_ssl(self, value):
        self._enable_ssl = (value, True)

    @property
    def enable_metrics(self):
        """
        *(default value: True)* Whether we should send metrics data to Splunk.

        :rtype: ``bool``
        """
        return self._enable_metrics[0]

    @enable_metrics.setter
    def enable_metrics(self, value):
        self._enable_metrics = (value, True)

    @property
    def metrics_index(self):
        """
        The Splunk Index metrics will be sent to. Must be set as an allowed
        index for the HEC token. If none is specified the mainIndex will be
        used for metrics as well.

        :rtype: ``str`` *or* ``null``
        """
        return self._metrics_index[0]

    @metrics_index.setter
    def metrics_index(self, value):
        self._metrics_index = (value, True)

    @property
    def performance_metrics_resolution(self):
        """
        *(default value: MINUTE)* The resolution of performance metrics data
        sent to Splunk. The options are SECOND for 1-second resolution, or
        MINUTE for 1-minute resolution. *(permitted values: SECOND, MINUTE)*

        :rtype: ``str``
        """
        return self._performance_metrics_resolution[0]

    @performance_metrics_resolution.setter
    def performance_metrics_resolution(self, value):
        self._performance_metrics_resolution = (value, True)

    @property
    def events_push_frequency(self):
        """
        *(default value: 60)* The frequency in number of seconds at which the
        Events will be pushed to Splunk. Defaults to 60 seconds.

        :rtype: ``int``
        """
        return self._events_push_frequency[0]

    @events_push_frequency.setter
    def events_push_frequency(self, value):
        self._events_push_frequency = (value, True)

    @property
    def metrics_push_frequency(self):
        """
        *(default value: 60)* The frequency in number of seconds at which the
        Performance Metrics will be pushed to Splunk. Defaults to 60 seconds.

        :rtype: ``int``
        """
        return self._metrics_push_frequency[0]

    @metrics_push_frequency.setter
    def metrics_push_frequency(self, value):
        self._metrics_push_frequency = (value, True)

