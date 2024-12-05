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
Package "domain"
"""
from delphixpy.v1_11_28 import response_validator

def get(engine):
    """
    Retrieve the specified Domain object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_28.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_28.web.vo.Domain`
    """
    url = "/resources/json/delphix/domain"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Domain'], returns_list=False, raw_result=raw_result)

def initialize_system(engine, system_initialization_parameters):
    """
    Initialize storage, core domain objects and node type.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_28.delphix_engine.DelphixEngine`
    :param system_initialization_parameters: Payload object.
    :type system_initialization_parameters:
        :py:class:`v1_11_28.web.vo.SystemInitializationParameters`
    """
    url = "/resources/json/delphix/domain/initializeSystem"
    response = engine.post(url, system_initialization_parameters.to_dict(dirty=True) if system_initialization_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def lock(engine):
    """
    Protects all sources in the engine from deletion and other data-losing
    actions. Cannot be undone.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_28.delphix_engine.DelphixEngine`
    """
    url = "/resources/json/delphix/domain/lock"
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

