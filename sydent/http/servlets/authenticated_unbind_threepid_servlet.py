# -*- coding: utf-8 -*-

# Copyright 2020 Dirk Klimpel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.web.resource import Resource

from sydent.http.servlets import get_args, jsonwrap, send_cors
from sydent.http.servlets.threepidunbindservlet import check_req_params


class AuthenticatedUnbindThreePidServlet(Resource):
    """A servlet which allows a caller to unbind any 3pid they want from an mxid

    It is assumed that authentication happens out of band
    """
    def __init__(self, sydent):
        Resource.__init__(self)
        self.sydent = sydent

    @jsonwrap
    def render_POST(self, request):
        send_cors(request)
        
        if not check_req_params(request):
            return

        try:
            self.sydent.threepidBinder.removeBinding(threepid, mxid)

            request.write(dict_to_json_bytes({}))
            request.finish()
        except Exception as ex:
            logger.exception("Exception whilst handling unbind")
            request.setResponseCode(500)
            request.write(dict_to_json_bytes({'errcode': 'M_UNKNOWN', 'error': str(ex)}))
            request.finish()

    def render_OPTIONS(self, request):
        send_cors(request)
        return b''
