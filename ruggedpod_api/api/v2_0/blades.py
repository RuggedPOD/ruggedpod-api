# RuggedPOD management API
#
# Copyright (C) 2015 Maxime Terras <maxime.terras@numergy.com>
# Copyright (C) 2015 Guillaume Giamarchi <guillaume.giamarchi@gmail.com>
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
from ruggedpod_api.services import blades

from flask import request


@api.route("/blades", methods=['GET'])
def get_blades():
    return json.dumps(blades.get_blades())


@api.route("/blades/reset", methods=['PATCH'])
def reset_blades():
    blades.reset_blades()
    return "", 204


@api.route("/blades/power", methods=['PATCH'])
def power_blades():
    blades.power_blades(_long_action())
    return "", 204


@api.route("/blades/<id>", methods=['GET'])
def get_blade(id):
    return json.dumps(blades.get_blade(id))


@api.route("/blades/<id>", methods=['PUT'])
def update_blade(id):
    data = utils.parse_json_body(request)
    return json.dumps(blades.update_blade(id, data))


@api.route("/blades/<id>/reset", methods=['PATCH'])
def reset_blade(id):
    blades.reset_blade(id)
    return "", 204


@api.route("/blades/<id>/power", methods=['PATCH'])
def power_blade(id):
    blades.power_blade(id, _long_action())
    return "", 204


@api.route("/blades/<id>/serial", methods=['PATCH'])
def serial_blade(id):
    blades.serial_blade(id)
    return "", 204


@api.route("/commands", methods=['GET'])
def get_all_commands():
    return json.dumps(blades.get_all_commands())


@api.route("/commands/<id>", methods=['GET'])
def get_command(id):
    return json.dumps(blades.get_command(id))


@api.route("/blades/<blade_id>/commands/<id>", methods=['GET'])
def get_blade_command(blade_id, id):
    return json.dumps(blades.get_blade_command(blade_id, id))


@api.route("/blades/<id>/commands", methods=['GET'])
def get_blade_commands(id):
    return json.dumps(blades.get_blade_commands(id))


@api.route("/blades/<id>/commands", methods=['POST'])
def exec_command(id):
    data = utils.parse_json_body(request)
    return json.dumps(blades.exec_command(id)), 202


@api.route("/blades/<id>/build", methods=['POST'])
def build_blade(id):
    data = utils.parse_json_body(request)
    blades.build_blade(id, data)
    return "", 204


@api.route("/blades/<id>/build", methods=['DELETE'])
def cancel_build_blade(id):
    blades.cancel_build_blade(id)
    return "", 204


def _long_action():
    long = request.args.get('long')
    return long is not None and (long.lower() == 'true' or long == '')
