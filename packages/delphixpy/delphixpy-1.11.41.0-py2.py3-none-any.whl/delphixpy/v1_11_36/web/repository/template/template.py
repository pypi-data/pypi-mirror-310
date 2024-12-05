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
Package "repository.template"
"""
from delphixpy.v1_11_36 import response_validator

def create(engine, source_repository_template=None):
    """
    Create a new SourceRepositoryTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param source_repository_template: Payload object.
    :type source_repository_template:
        :py:class:`v1_11_36.web.vo.SourceRepositoryTemplate`
    :rtype: ``str``
    """
    url = "/resources/json/delphix/repository/template"
    response = engine.post(url, source_repository_template.to_dict(dirty=True) if source_repository_template else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['str'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified SourceRepositoryTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_36.web.objects.Source
        RepositoryTemplate.SourceRepositoryTemplate` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_36.web.vo.SourceRepositoryTemplate`
    """
    url = "/resources/json/delphix/repository/template/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SourceRepositoryTemplate'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    Returns the list of repository templates.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_36.web.vo.SourceRepositoryTemplate`
    """
    url = "/resources/json/delphix/repository/template"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SourceRepositoryTemplate'], returns_list=True, raw_result=raw_result)

def update(engine, ref, source_repository_template=None):
    """
    Update the specified SourceRepositoryTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_36.web.objects.Source
        RepositoryTemplate.SourceRepositoryTemplate` object
    :type ref: ``str``
    :param source_repository_template: Payload object.
    :type source_repository_template:
        :py:class:`v1_11_36.web.vo.SourceRepositoryTemplate`
    """
    url = "/resources/json/delphix/repository/template/%s" % ref
    response = engine.post(url, source_repository_template.to_dict(dirty=True) if source_repository_template else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified SourceRepositoryTemplate object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_36.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_36.web.objects.Source
        RepositoryTemplate.SourceRepositoryTemplate` object
    :type ref: ``str``
    """
    url = "/resources/json/delphix/repository/template/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

