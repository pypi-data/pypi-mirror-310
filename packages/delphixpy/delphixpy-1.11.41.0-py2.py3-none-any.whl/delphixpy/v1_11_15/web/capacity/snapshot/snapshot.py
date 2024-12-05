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
Package "capacity.snapshot"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_15 import response_validator

def get_all(engine, container=None, namespace=None, page_size=None, page_offset=None):
    """
    Lists capacity metrics for all snapshots in the system sorted by snapshot
    space usage decreasing.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_15.delphix_engine.DelphixEngine`
    :param container: The container to list snapshot data for.
    :type container: ``str``
    :param namespace: The namespace to list snapshot data for. If null, will
        limit returned snapshots to the default namespace.
    :type namespace: ``str`` *or* ``null``
    :param page_size: Limit the number of entries returned.
    :type page_size: ``int``
    :param page_offset: Offset within list, in units of pageSize chunks.
    :type page_offset: ``int``
    :rtype: ``list`` of :py:class:`v1_11_15.web.vo.SnapshotCapacityData`
    """
    url = "/resources/json/delphix/capacity/snapshot"
    query_params = {"container": container, "namespace": namespace, "pageSize": page_size, "pageOffset": page_offset}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SnapshotCapacityData'], returns_list=True, raw_result=raw_result)

