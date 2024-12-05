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
Package "capacity.system.historical"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_23 import response_validator

def get_all(engine, start_date=None, end_date=None, resolution=None):
    """
    Lists historical system capacity data.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_23.delphix_engine.DelphixEngine`
    :param start_date: Earliest date for which to list data.
    :type start_date: ``str``
    :param end_date: Latest date for which to list data.
    :type end_date: ``str``
    :param resolution: The time range each datapoint should represent, measured
        in seconds.
    :type resolution: ``int``
    :rtype: ``list`` of
        :py:class:`v1_11_23.web.vo.HistoricalSystemCapacityData`
    """
    url = "/resources/json/delphix/capacity/system/historical"
    query_params = {"startDate": start_date, "endDate": end_date, "resolution": resolution}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['HistoricalSystemCapacityData'], returns_list=True, raw_result=raw_result)

