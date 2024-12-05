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
Package "transformation"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_5 import response_validator

def get(engine, ref):
    """
    Retrieve the specified Transformation object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_5.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_5.web.objects.Transformation.Transformation`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_5.web.vo.Transformation`
    """
    url = "/resources/json/delphix/transformation/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Transformation'], returns_list=False, raw_result=raw_result)

def get_all(engine, container=None, parent_container=None):
    """
    Returns a list of all transformations on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_5.delphix_engine.DelphixEngine`
    :param container: Return the transformation responsible for the given
        container reference.
    :type container: ``str``
    :param parent_container: List the transformations that have been created
        against the provided container.
    :type parent_container: ``str``
    :rtype: ``list`` of :py:class:`v1_11_5.web.vo.Transformation`
    """
    url = "/resources/json/delphix/transformation"
    query_params = {"container": container, "parentContainer": parent_container}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Transformation'], returns_list=True, raw_result=raw_result)

def update(engine, ref, transformation=None):
    """
    Update the specified Transformation object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_5.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_5.web.objects.Transformation.Transformation`
        object
    :type ref: ``str``
    :param transformation: Payload object.
    :type transformation: :py:class:`v1_11_5.web.vo.Transformation`
    """
    url = "/resources/json/delphix/transformation/%s" % ref
    response = engine.post(url, transformation.to_dict(dirty=True) if transformation else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def apply(engine, ref, timeflow_point_parameters):
    """
    Apply a transformation.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_5.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_5.web.objects.Transformation.Transformation`
        object
    :type ref: ``str``
    :param timeflow_point_parameters: Payload object.
    :type timeflow_point_parameters:
        :py:class:`v1_11_5.web.vo.TimeflowPointParameters`
    """
    url = "/resources/json/delphix/transformation/%s/apply" % ref
    response = engine.post(url, timeflow_point_parameters.to_dict(dirty=True) if timeflow_point_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

