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
Package "service.userInterface"
"""
from delphixpy.v1_11_22 import response_validator

def get(engine):
    """
    Retrieve the specified UserInterfaceConfig object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_22.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_22.web.vo.UserInterfaceConfig`
    """
    url = "/resources/json/delphix/service/userInterface"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['UserInterfaceConfig'], returns_list=False, raw_result=raw_result)

def set(engine, user_interface_config=None):
    """
    Update the specified UserInterfaceConfig object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_22.delphix_engine.DelphixEngine`
    :param user_interface_config: Payload object.
    :type user_interface_config:
        :py:class:`v1_11_22.web.vo.UserInterfaceConfig`
    """
    url = "/resources/json/delphix/service/userInterface"
    response = engine.post(url, user_interface_config.to_dict(dirty=True) if user_interface_config else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

