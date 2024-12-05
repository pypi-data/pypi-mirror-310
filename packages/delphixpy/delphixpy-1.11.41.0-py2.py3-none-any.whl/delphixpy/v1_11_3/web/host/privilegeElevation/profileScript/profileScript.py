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
Package "host.privilegeElevation.profileScript"
"""
from delphixpy.v1_11_3 import response_validator

def create(engine, host_privilege_elevation_profile_script=None):
    """
    Create a new HostPrivilegeElevationProfileScript object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_3.delphix_engine.DelphixEngine`
    :param host_privilege_elevation_profile_script: Payload object.
    :type host_privilege_elevation_profile_script:
        :py:class:`v1_11_3.web.vo.HostPrivilegeElevationProfileScript`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/host/privilegeElevation/profileScript"
    response = engine.post(url, host_privilege_elevation_profile_script.to_dict(dirty=True) if host_privilege_elevation_profile_script else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified HostPrivilegeElevationProfileScript object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_3.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_3.web.objects.HostPri
        vilegeElevationProfileScript.HostPrivilegeElevationProfileScript`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_3.web.vo.HostPrivilegeElevationProfileScript`
    """
    url = "/resources/json/delphix/host/privilegeElevation/profileScript/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['HostPrivilegeElevationProfileScript'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List HostPrivilegeElevationProfileScript objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_3.delphix_engine.DelphixEngine`
    :rtype: ``list`` of
        :py:class:`v1_11_3.web.vo.HostPrivilegeElevationProfileScript`
    """
    url = "/resources/json/delphix/host/privilegeElevation/profileScript"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['HostPrivilegeElevationProfileScript'], returns_list=True, raw_result=raw_result)

def update(engine, ref, host_privilege_elevation_profile_script=None):
    """
    Update the specified HostPrivilegeElevationProfileScript object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_3.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_3.web.objects.HostPri
        vilegeElevationProfileScript.HostPrivilegeElevationProfileScript`
        object
    :type ref: ``str``
    :param host_privilege_elevation_profile_script: Payload object.
    :type host_privilege_elevation_profile_script:
        :py:class:`v1_11_3.web.vo.HostPrivilegeElevationProfileScript`
    """
    url = "/resources/json/delphix/host/privilegeElevation/profileScript/%s" % ref
    response = engine.post(url, host_privilege_elevation_profile_script.to_dict(dirty=True) if host_privilege_elevation_profile_script else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified HostPrivilegeElevationProfileScript object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_3.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_3.web.objects.HostPri
        vilegeElevationProfileScript.HostPrivilegeElevationProfileScript`
        object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/host/privilegeElevation/profileScript/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

