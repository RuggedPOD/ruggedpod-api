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
from ruggedpod_api.services import i2c

from flask import request


@api.route("/i2c", methods=['GET'])
def get_bus():
    return json.dumps(i2c.read_bus())


@api.route("/i2c/<id>", methods=['GET'])
def get_single_bus(id):
    return json.dumps(i2c.read_single_bus(id))


@api.route("/i2c/<id>/detect", methods=['PUT'])
def detect_bus_devices(id):
    return json.dumps(i2c.detect_bus_devices(id))


@api.route("/i2c/<id>/devices", methods=['GET'])
def get_bus_devices(id):
    return json.dumps(i2c.read_bus_devices(id))


@api.route("/i2c/<id>/devices/<address>", methods=['GET'])
def get_single_device(id, address):
    return json.dumps(i2c.read_single_device(id, address))


@api.route("/i2c/<id>/devices/<address>", methods=['DELETE'])
def delete_single_device(id, address):
    i2c.delete_single_device(id, address)
    return '', 204


@api.route("/i2c/<id>/devices/<address>", methods=['POST'])
def setup_device(id, address):
    data = utils.parse_json_body(request)
    return json.dumps(i2c.setup_device(id, address, data))
