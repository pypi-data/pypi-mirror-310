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
Package "host"
"""
from delphixpy.v1_11_30.web.host import privilegeElevation
from urllib.parse import urlencode
from delphixpy.v1_11_30 import response_validator

def get(engine, ref):
    """
    Retrieve the specified Host object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_30.web.objects.Host.Host` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_30.web.vo.Host`
    """
    url = "/resources/json/delphix/host/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Host'], returns_list=False, raw_result=raw_result)

def get_all(engine, environment=None):
    """
    Returns the list of all hosts in the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :param environment: Include only hosts belonging to the given environment.
    :type environment: ``str``
    :rtype: ``list`` of :py:class:`v1_11_30.web.vo.Host`
    """
    url = "/resources/json/delphix/host"
    query_params = {"environment": environment}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Host'], returns_list=True, raw_result=raw_result)

def update(engine, ref, host=None):
    """
    Update the specified Host object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_30.web.objects.Host.Host` object
    :type ref: ``str``
    :param host: Payload object.
    :type host: :py:class:`v1_11_30.web.vo.Host`
    """
    url = "/resources/json/delphix/host/%s" % ref
    response = engine.post(url, host.to_dict(dirty=True) if host else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def validate_java(engine, validate_java_parameters=None):
    """
    Tests that the user-provided version of Java on a remote host works and
    meets our requirements.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :param validate_java_parameters: Payload object.
    :type validate_java_parameters:
        :py:class:`v1_11_30.web.vo.ValidateJavaParameters`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/host/validateJava"
    response = engine.post(url, validate_java_parameters.to_dict(dirty=True) if validate_java_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

