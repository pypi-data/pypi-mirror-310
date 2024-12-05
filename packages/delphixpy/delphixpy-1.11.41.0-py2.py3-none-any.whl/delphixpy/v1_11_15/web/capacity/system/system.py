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
Package "capacity.system"
"""
from delphixpy.v1_11_15 import response_validator

def get(engine):
    """
    Retrieve the specified CurrentSystemCapacityData object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_15.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_15.web.vo.CurrentSystemCapacityData`
    """
    url = "/resources/json/delphix/capacity/system"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['CurrentSystemCapacityData'], returns_list=False, raw_result=raw_result)

