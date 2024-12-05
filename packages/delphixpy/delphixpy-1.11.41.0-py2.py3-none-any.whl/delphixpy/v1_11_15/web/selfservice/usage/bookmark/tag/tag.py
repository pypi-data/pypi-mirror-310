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
Package "selfservice.usage.bookmark.tag"
"""
from urllib.parse import urlencode
from delphixpy.v1_11_15 import response_validator

def list_bookmark_tag_usage_data(engine, bookmark_tag=None):
    """
    Lists the usage breakdown for Self-Service bookmark tags.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_15.delphix_engine.DelphixEngine`
    :param bookmark_tag: If passed in, this query parameter restricts the API
        to only return the usage information for the given bookmark tag. By
        default, the usage information for all bookmarks tags is returned.
    :type bookmark_tag: ``str``
    :rtype: ``list`` of :py:class:`v1_11_15.web.vo.JSBookmarkTagUsageData`
    """
    url = "/resources/json/delphix/selfservice/usage/bookmark/tag/listBookmarkTagUsageData"
    query_params = {"bookmarkTag": bookmark_tag}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['JSBookmarkTagUsageData'], returns_list=True, raw_result=raw_result)

