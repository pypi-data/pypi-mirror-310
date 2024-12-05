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
Package "selfservice.usagedata.operationduration"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_29 import response_validator

def get(engine, ref):
    """
    Retrieve the specified JSDailyOperationDuration object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_29.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_29.web.objects.JSDail
        yOperationDuration.JSDailyOperationDuration` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_29.web.vo.JSDailyOperationDuration`
    """
    url = "/resources/json/delphix/selfservice/usagedata/operationduration/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSDailyOperationDuration'], returns_list=False, raw_result=raw_result)

def get_all(engine, usage_object=None):
    """
    List the operation durations in the system, optionally restricted to those
    operations related to a single object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_29.delphix_engine.DelphixEngine`
    :param usage_object: Restrict usage data to that related to a specific
        object.
    :type usage_object: ``str``
    :rtype: ``list`` of :py:class:`v1_11_29.web.vo.JSDailyOperationDuration`
    """
    url = "/resources/json/delphix/selfservice/usagedata/operationduration"
    query_params = {"usageObject": usage_object}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSDailyOperationDuration'], returns_list=True, raw_result=raw_result)

