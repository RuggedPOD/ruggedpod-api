# RuggedPOD management API
#
# Copyright (C) 2016 Guillaume Giamarchi <guillaume.giamarchi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import json

from .blueprint import api
from ruggedpod_api.api import utils
from ruggedpod_api.services import dhcp

from flask import request


@api.route("/dhcp", methods=['GET'])
def get_dhcp_config():
    return json.dumps(dhcp.read_config())


@api.route("/dhcp", methods=['PUT'])
def update_dhcp_config():
    data = utils.parse_json_body(request)
    dhcp.update_config(data)
    return get_dhcp_config()


@api.route("/dhcp/refresh", methods=['PUT'])
def refresh_dhcp_config():
    dhcp.refresh()
    return "", 204
