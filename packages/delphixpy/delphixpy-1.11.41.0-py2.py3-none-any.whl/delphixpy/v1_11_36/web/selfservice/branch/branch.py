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
Package "selfservice.branch"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_36 import response_validator

def create(engine, js_branch_create_parameters):
    """
    Create a new JSBranch object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param js_branch_create_parameters: Payload object.
    :type js_branch_create_parameters:
        :py:class:`v1_11_36.web.vo.JSBranchCreateParameters`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/selfservice/branch"
    response = engine.post(url, js_branch_create_parameters.to_dict(dirty=True) if js_branch_create_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified JSBranch object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_36.web.objects.JSBranch.JSBranch` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_36.web.vo.JSBranch`
    """
    url = "/resources/json/delphix/selfservice/branch/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSBranch'], returns_list=False, raw_result=raw_result)

def get_all(engine, data_layout=None):
    """
    Lists the Self-Service branches in the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param data_layout: List branches belonging to the given data layout.
    :type data_layout: ``str``
    :rtype: ``list`` of :py:class:`v1_11_36.web.vo.JSBranch`
    """
    url = "/resources/json/delphix/selfservice/branch"
    query_params = {"dataLayout": data_layout}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSBranch'], returns_list=True, raw_result=raw_result)

def update(engine, ref, js_branch=None):
    """
    Update the specified JSBranch object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_36.web.objects.JSBranch.JSBranch` object
    :type ref: ``str``
    :param js_branch: Payload object.
    :type js_branch: :py:class:`v1_11_36.web.vo.JSBranch`
    """
    url = "/resources/json/delphix/selfservice/branch/%s" % ref
    response = engine.post(url, js_branch.to_dict(dirty=True) if js_branch else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified JSBranch object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_36.web.objects.JSBranch.JSBranch` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/selfservice/branch/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def activate(engine, ref):
    """
    Makes this branch the current branch for its data layout.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_36.web.objects.JSBranch.JSBranch` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/selfservice/branch/%s/activate" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

