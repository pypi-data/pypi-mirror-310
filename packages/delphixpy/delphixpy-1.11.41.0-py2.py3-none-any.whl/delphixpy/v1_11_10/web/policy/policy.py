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
Package "policy"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_10 import response_validator

def create(engine, policy=None):
    """
    Create a new Policy object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param policy: Payload object.
    :type policy: :py:class:`v1_11_10.web.vo.Policy`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/policy"
    response = engine.post(url, policy.to_dict(dirty=True) if policy else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified Policy object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.Policy.Policy` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_10.web.vo.Policy`
    """
    url = "/resources/json/delphix/policy/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Policy'], returns_list=False, raw_result=raw_result)

def get_all(engine, type=None, target=None, effective=None):
    """
    Returns a list of policies in the domain.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param type: Limit policies to those of the given type.
    :type type: ``str``
    :param target: Limit policies to those affecting a particular object on the
        system.
    :type target: ``str``
    :param effective: Whether to include effective policies for the target.
    :type effective: ``str``
    :rtype: ``list`` of :py:class:`v1_11_10.web.vo.Policy`
    """
    url = "/resources/json/delphix/policy"
    query_params = {"type": type, "target": target, "effective": effective}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Policy'], returns_list=True, raw_result=raw_result)

def update(engine, ref, policy=None):
    """
    Update the specified Policy object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.Policy.Policy` object
    :type ref: ``str``
    :param policy: Payload object.
    :type policy: :py:class:`v1_11_10.web.vo.Policy`
    """
    url = "/resources/json/delphix/policy/%s" % ref
    response = engine.post(url, policy.to_dict(dirty=True) if policy else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified Policy object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.Policy.Policy` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/policy/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def apply(engine, ref, policy_apply_target_parameters):
    """
    Apply the policy to the specified target.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.Policy.Policy` object
    :type ref: ``str``
    :param policy_apply_target_parameters: Payload object.
    :type policy_apply_target_parameters:
        :py:class:`v1_11_10.web.vo.PolicyApplyTargetParameters`
    """
    url = "/resources/json/delphix/policy/%s/apply" % ref
    response = engine.post(url, policy_apply_target_parameters.to_dict(dirty=True) if policy_apply_target_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def unapply(engine, ref, policy_apply_target_parameters):
    """
    Unapply the policy on the specified target.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.Policy.Policy` object
    :type ref: ``str``
    :param policy_apply_target_parameters: Payload object.
    :type policy_apply_target_parameters:
        :py:class:`v1_11_10.web.vo.PolicyApplyTargetParameters`
    """
    url = "/resources/json/delphix/policy/%s/unapply" % ref
    response = engine.post(url, policy_apply_target_parameters.to_dict(dirty=True) if policy_apply_target_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def create_and_apply(engine, policy_create_and_apply_parameters):
    """
    Create and apply a new policy.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param policy_create_and_apply_parameters: Payload object.
    :type policy_create_and_apply_parameters:
        :py:class:`v1_11_10.web.vo.PolicyCreateAndApplyParameters`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/policy/createAndApply"
    response = engine.post(url, policy_create_and_apply_parameters.to_dict(dirty=True) if policy_create_and_apply_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

