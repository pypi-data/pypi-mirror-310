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
Package "selfservice.usage.container"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_41 import response_validator

def list_container_usage_data(engine, data_container=None, template=None, user=None):
    """
    Lists the usage breakdown for data containers.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_41.delphix_engine.DelphixEngine`
    :param data_container: If passed in, this query parameter restricts the API
        to only return the usage information for the given data container. This
        parameter is mutually exclusive with the "template" and "user"
        parameters.
    :type data_container: ``str``
    :param template: If passed in, this query parameter restricts the API to
        only return the usage information for all of the data containers from
        the given data template. This parameter is mutually exclusive with the
        "dataContainer" and "user" parameters.
    :type template: ``str``
    :param user: If passed in, this query parameter restricts the API to only
        return the usage information for all of the data containers owned by
        the given user. This parameter is mutually exclusive with the
        "dataContainer" and "template" parameters.
    :type user: ``str``
    :rtype: ``list`` of :py:class:`v1_11_41.web.vo.JSContainerUsageData`
    """
    url = "/resources/json/delphix/selfservice/usage/container/listContainerUsageData"
    query_params = {"dataContainer": data_container, "template": template, "user": user}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSContainerUsageData'], returns_list=True, raw_result=raw_result)

