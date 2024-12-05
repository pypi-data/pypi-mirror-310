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
Package "database.template"
"""
from delphixpy.v1_11_37 import response_validator

def create(engine, database_template=None):
    """
    Create a new DatabaseTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param database_template: Payload object.
    :type database_template: :py:class:`v1_11_37.web.vo.DatabaseTemplate`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/database/template"
    response = engine.post(url, database_template.to_dict(dirty=True) if database_template else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified DatabaseTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_37.web.objects.Databa
        seTemplate.DatabaseTemplate` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_37.web.vo.DatabaseTemplate`
    """
    url = "/resources/json/delphix/database/template/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['DatabaseTemplate'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List DatabaseTemplate objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_37.web.vo.DatabaseTemplate`
    """
    url = "/resources/json/delphix/database/template"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['DatabaseTemplate'], returns_list=True, raw_result=raw_result)

def update(engine, ref, database_template=None):
    """
    Update the specified DatabaseTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_37.web.objects.Databa
        seTemplate.DatabaseTemplate` object
    :type ref: ``str``
    :param database_template: Payload object.
    :type database_template: :py:class:`v1_11_37.web.vo.DatabaseTemplate`
    """
    url = "/resources/json/delphix/database/template/%s" % ref
    response = engine.post(url, database_template.to_dict(dirty=True) if database_template else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified DatabaseTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_37.web.objects.Databa
        seTemplate.DatabaseTemplate` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/database/template/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def config(engine):
    """
    Return a list of static template configuration information.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_37.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_37.web.vo.DatabaseTemplateConfig`
    """
    url = "/resources/json/delphix/database/template/config"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['DatabaseTemplateConfig'], returns_list=True, raw_result=raw_result)

