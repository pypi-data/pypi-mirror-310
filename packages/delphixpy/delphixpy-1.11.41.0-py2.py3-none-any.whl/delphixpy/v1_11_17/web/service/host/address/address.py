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
Package "service.host.address"
"""
from delphixpy.v1_11_17 import response_validator

def create(engine, static_host_address=None):
    """
    Create a new StaticHostAddress object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_17.delphix_engine.DelphixEngine`
    :param static_host_address: Payload object.
    :type static_host_address: :py:class:`v1_11_17.web.vo.StaticHostAddress`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/service/host/address"
    response = engine.post(url, static_host_address.to_dict(dirty=True) if static_host_address else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified StaticHostAddress object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_17.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_17.web.objects.Static
        HostAddress.StaticHostAddress` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_17.web.vo.StaticHostAddress`
    """
    url = "/resources/json/delphix/service/host/address/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StaticHostAddress'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List StaticHostAddress objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_17.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_17.web.vo.StaticHostAddress`
    """
    url = "/resources/json/delphix/service/host/address"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StaticHostAddress'], returns_list=True, raw_result=raw_result)

def update(engine, ref, static_host_address=None):
    """
    Update the specified StaticHostAddress object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_17.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_17.web.objects.Static
        HostAddress.StaticHostAddress` object
    :type ref: ``str``
    :param static_host_address: Payload object.
    :type static_host_address: :py:class:`v1_11_17.web.vo.StaticHostAddress`
    """
    url = "/resources/json/delphix/service/host/address/%s" % ref
    response = engine.post(url, static_host_address.to_dict(dirty=True) if static_host_address else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified StaticHostAddress object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_17.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_17.web.objects.Static
        HostAddress.StaticHostAddress` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/service/host/address/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

