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
Package "service.smtp"
"""
from delphixpy.v1_11_30 import response_validator

def get(engine):
    """
    Retrieve the specified SMTPConfig object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_30.web.vo.SMTPConfig`
    """
    url = "/resources/json/delphix/service/smtp"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SMTPConfig'], returns_list=False, raw_result=raw_result)

def set(engine, smtp_config=None):
    """
    Update the specified SMTPConfig object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :param smtp_config: Payload object.
    :type smtp_config: :py:class:`v1_11_30.web.vo.SMTPConfig`
    """
    url = "/resources/json/delphix/service/smtp"
    response = engine.post(url, smtp_config.to_dict(dirty=True) if smtp_config else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def validate(engine, validate_smtp_parameters):
    """
    Validate SMTP configuration without committing changes by sending a test
    email.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_30.delphix_engine.DelphixEngine`
    :param validate_smtp_parameters: Payload object.
    :type validate_smtp_parameters:
        :py:class:`v1_11_30.web.vo.ValidateSMTPParameters`
    """
    url = "/resources/json/delphix/service/smtp/validate"
    response = engine.post(url, validate_smtp_parameters.to_dict(dirty=True) if validate_smtp_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

