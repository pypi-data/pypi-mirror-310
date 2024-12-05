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
Package "service.ldap.server"
"""
from delphixpy.v1_11_19 import response_validator

def create(engine, ldap_server=None):
    """
    Create a new LdapServer object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_19.delphix_engine.DelphixEngine`
    :param ldap_server: Payload object.
    :type ldap_server: :py:class:`v1_11_19.web.vo.LdapServer`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/service/ldap/server"
    response = engine.post(url, ldap_server.to_dict(dirty=True) if ldap_server else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified LdapServer object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_19.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_19.web.objects.LdapServer.LdapServer` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_19.web.vo.LdapServer`
    """
    url = "/resources/json/delphix/service/ldap/server/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['LdapServer'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List LdapServer objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_19.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_19.web.vo.LdapServer`
    """
    url = "/resources/json/delphix/service/ldap/server"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['LdapServer'], returns_list=True, raw_result=raw_result)

def update(engine, ref, ldap_server=None):
    """
    Update the specified LdapServer object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_19.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_19.web.objects.LdapServer.LdapServer` object
    :type ref: ``str``
    :param ldap_server: Payload object.
    :type ldap_server: :py:class:`v1_11_19.web.vo.LdapServer`
    """
    url = "/resources/json/delphix/service/ldap/server/%s" % ref
    response = engine.post(url, ldap_server.to_dict(dirty=True) if ldap_server else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified LdapServer object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_19.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_19.web.objects.LdapServer.LdapServer` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/service/ldap/server/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def test(engine, ldap_server=None):
    """
    Test the LDAP server by anonymous login.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_19.delphix_engine.DelphixEngine`
    :param ldap_server: Payload object.
    :type ldap_server: :py:class:`v1_11_19.web.vo.LdapServer`
    """
    url = "/resources/json/delphix/service/ldap/server/test"
    response = engine.post(url, ldap_server.to_dict(dirty=True) if ldap_server else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

