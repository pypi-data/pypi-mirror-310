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
Package "replication.serializationpoint"
"""
from delphixpy.v1_11_8 import response_validator

def get(engine, ref):
    """
    Retrieve the specified SerializationPoint object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_8.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_8.web.objects.Seriali
        zationPoint.SerializationPoint` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_8.web.vo.SerializationPoint`
    """
    url = "/resources/json/delphix/replication/serializationpoint/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SerializationPoint'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List SerializationPoint objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_8.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_8.web.vo.SerializationPoint`
    """
    url = "/resources/json/delphix/replication/serializationpoint"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SerializationPoint'], returns_list=True, raw_result=raw_result)

