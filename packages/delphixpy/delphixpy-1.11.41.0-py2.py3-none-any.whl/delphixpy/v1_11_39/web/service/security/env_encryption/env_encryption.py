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
Package "service.security.env_encryption"
"""
from delphixpy.v1_11_39 import response_validator

def get(engine):
    """
    Retrieve the specified EnvEncryptionConfig object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_39.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_39.web.vo.EnvEncryptionConfig`
    """
    url = "/resources/json/delphix/service/security/env_encryption"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['EnvEncryptionConfig'], returns_list=False, raw_result=raw_result)

def set(engine, env_encryption_config=None):
    """
    Update the specified EnvEncryptionConfig object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_39.delphix_engine.DelphixEngine`
    :param env_encryption_config: Payload object.
    :type env_encryption_config:
        :py:class:`v1_11_39.web.vo.EnvEncryptionConfig`
    """
    url = "/resources/json/delphix/service/security/env_encryption"
    response = engine.post(url, env_encryption_config.to_dict(dirty=True) if env_encryption_config else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

