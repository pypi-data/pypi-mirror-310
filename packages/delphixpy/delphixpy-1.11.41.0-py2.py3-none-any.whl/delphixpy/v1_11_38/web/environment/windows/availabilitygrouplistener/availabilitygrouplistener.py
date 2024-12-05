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
Package "environment.windows.availabilitygrouplistener"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_38 import response_validator

def get_all(engine, availabilitygroup=None):
    """
    Returns a list of listeners filtered by SQL Server Availability Group.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_38.delphix_engine.DelphixEngine`
    :param availabilitygroup: A reference to the SQL Server Availability Group
        this listener belongs to.
    :type availabilitygroup: ``str``
    :rtype: ``list`` of
        :py:class:`v1_11_38.web.vo.MSSqlAvailabilityGroupListener`
    """
    url = "/resources/json/delphix/environment/windows/availabilitygrouplistener"
    query_params = {"availabilitygroup": availabilitygroup}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['MSSqlAvailabilityGroupListener'], returns_list=True, raw_result=raw_result)

