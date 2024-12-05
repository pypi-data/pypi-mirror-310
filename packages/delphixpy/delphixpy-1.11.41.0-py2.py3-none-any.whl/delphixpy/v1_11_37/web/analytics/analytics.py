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

"""
Package "analytics"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_37 import response_validator

def create(engine, statistic_slice=None):
    """
    Create a new StatisticSlice object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param statistic_slice: Payload object.
    :type statistic_slice: :py:class:`v1_11_37.web.vo.StatisticSlice`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/analytics"
    response = engine.post(url, statistic_slice.to_dict(dirty=True) if statistic_slice else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified StatisticSlice object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_37.web.vo.StatisticSlice`
    """
    url = "/resources/json/delphix/analytics/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StatisticSlice'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    Returns a list of statistics in the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_37.web.vo.StatisticSlice`
    """
    url = "/resources/json/delphix/analytics"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StatisticSlice'], returns_list=True, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified StatisticSlice object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/analytics/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def get_data(engine, ref, start_time=None, end_time=None, resolution=None, count=None):
    """
    Returns data for the specified time range. If no time range is specified,
    the most recent data will be returned. Time ranges are limited to 1 hour of
    1-second data, 1 day of 1-minute data, and 1 month of 1-hour data.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    :param start_time: None
    :type start_time: ``str``
    :param end_time: None
    :type end_time: ``str``
    :param resolution: The time interval each datapoint should represent,
        measured in seconds. If datapoints of the desired resolution are not
        available, datapoints of the next smallest available resolution will be
        returned. If unspecified or set to the value smaller than the smallest
        available resolution, then the lowest available resolution will be
        used.
    :type resolution: ``int``
    :param count: The number of data points to return. Mds data points will be
        combined in order to to meet this requirement. When count is specified
        at least two of the other getData parameters must be specified.
    :type count: ``int``
    :rtype: :py:class:`v1_11_37.web.vo.DatapointSet`
    """
    url = "/resources/json/delphix/analytics/%s/getData" % ref
    query_params = {"startTime": start_time, "endTime": end_time, "resolution": resolution, "count": count}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['DatapointSet'], returns_list=False, raw_result=raw_result)

def remember_range(engine, ref, time_range_parameters):
    """
    Prevents data from being deleted automatically.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    :param time_range_parameters: Payload object.
    :type time_range_parameters:
        :py:class:`v1_11_37.web.vo.TimeRangeParameters`
    """
    url = "/resources/json/delphix/analytics/%s/rememberRange" % ref
    response = engine.post(url, time_range_parameters.to_dict(dirty=True) if time_range_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def stop_remembering_range(engine, ref, time_range_parameters):
    """
    Allows saved data to be deleted automatically if it is getting old.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    :param time_range_parameters: Payload object.
    :type time_range_parameters:
        :py:class:`v1_11_37.web.vo.TimeRangeParameters`
    """
    url = "/resources/json/delphix/analytics/%s/stopRememberingRange" % ref
    response = engine.post(url, time_range_parameters.to_dict(dirty=True) if time_range_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def pause(engine, ref):
    """
    Pauses the collection of data for this slice.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/analytics/%s/pause" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def resume(engine, ref):
    """
    Resumes the collection of data for this slice.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_37.web.objects.StatisticSlice.StatisticSlice
        ` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/analytics/%s/resume" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

