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
Package "fault.effect"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_9 import response_validator

def get(engine, ref):
    """
    Retrieve the specified FaultEffect object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_9.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_9.web.objects.FaultEffect.FaultEffect`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_9.web.vo.FaultEffect`
    """
    url = "/resources/json/delphix/fault/effect/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['FaultEffect'], returns_list=False, raw_result=raw_result)

def get_all(engine, severity=None, target=None, targets=None, root_cause=None, bundle_id=None):
    """
    Returns the list of all the fault effects that match the given criteria.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_9.delphix_engine.DelphixEngine`
    :param severity: The impact of the fault effect on the system: CRITICAL or
        WARNING. *(permitted values: CRITICAL, WARNING)*
    :type severity: ``str``
    :param target: The reference to the Delphix user-visible object associated
        with the fault effect.
    :type target: ``str``
    :param targets: The references to the Delphix user-visible objects
        associated with the fault effects.
    :type targets: ``list`` of ``str``
    :param root_cause: The reference to the fault which is the root cause of
        the fault effect.
    :type root_cause: ``str``
    :param bundle_id: A unique dot delimited identifier associated with the
        fault effect.
    :type bundle_id: ``str``
    :rtype: ``list`` of :py:class:`v1_11_9.web.vo.FaultEffect`
    """
    url = "/resources/json/delphix/fault/effect"
    query_params = {"severity": severity, "target": target, "targets": targets, "rootCause": root_cause, "bundleID": bundle_id}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['FaultEffect'], returns_list=True, raw_result=raw_result)

