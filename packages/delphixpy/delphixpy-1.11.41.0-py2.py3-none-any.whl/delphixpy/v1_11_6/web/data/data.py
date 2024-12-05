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
Package "data"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_6 import response_validator

def download(engine, token=None):
    """
    Download the resource.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_6.delphix_engine.DelphixEngine`
    :param token: A token that uniquely identifies a resource stored on the
        Delphix Engine.
    :type token: ``str``
    """
    url = "/resources/json/delphix/data/download"
    query_params = {"token": token}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def download_output_stream(engine, token=None):
    """
    Download the output stream resource.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_6.delphix_engine.DelphixEngine`
    :param token: A token that uniquely identifies a resource stored on the
        Delphix Engine.
    :type token: ``str``
    """
    url = "/resources/json/delphix/data/downloadOutputStream"
    query_params = {"token": token}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

