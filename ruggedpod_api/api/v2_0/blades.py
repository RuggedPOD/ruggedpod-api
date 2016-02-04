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

from ruggedpod_api.common import exception
from ruggedpod_api.services import gpio
from ruggedpod_api.services.db import Database, Blade, db

from flask import request


@api.route("/blades", methods=['GET'])
def get_blades():
    session = db.session()
    with session.begin():
        blades = []
        for b in session.query(Blade):
            blades.append({
                'id': b.id,
                'name': b.name,
                'description': b.description,
                'consumption': gpio.read_power_consumption(str(b.id))
            })
        return json.dumps(blades)


@api.route("/blades/reset", methods=['PATCH'])
def reset_blades():
    gpio.set_all_blades_reset()
    return "", 204


@api.route("/blades/power", methods=['PATCH'])
def power_blades():
    if _long_action():
        gpio.set_all_blades_long_onoff()
    else:
        gpio.set_all_blades_short_onoff()
    return "", 204


@api.route("/blades/<id>", methods=['GET'])
def get_blade(id):
    session = db.session()
    with session.begin():
        blade = _get_blade(id, session)
        return json.dumps({
            'id': blade.id,
            'name': blade.name,
            'description': blade.description,
            'consumption': gpio.read_power_consumption(str(blade.id))
        })


@api.route("/blades/<id>", methods=['PUT'])
def update_blade(id):
    session = db.session()
    with session.begin():
        blade = _get_blade(id, session)

        data = json.loads(request.data)
        if 'id' in data and int(data['id']) != int(id):
            raise exception.Conflict(reason="Id mismatch")

        if 'name' in data:
            blade.name = data['name']

        if 'description' in data:
            blade.description = data['description']

    return get_blade(id)


@api.route("/blades/<id>/reset", methods=['PATCH'])
def reset_blade(id):
    _get_blade(id, db.session())
    gpio.set_blade_reset(id)
    return "", 204


@api.route("/blades/<id>/power", methods=['PATCH'])
def power_blade(id):
    _get_blade(id, db.session())
    if _long_action():
        gpio.set_blade_long_onoff(id)
    else:
        gpio.set_blade_short_onoff(id)
    return "", 204


@api.route("/blades/<id>/serial", methods=['PATCH'])
def serial_blade(id):
    _get_blade(id, db.session())
    gpio.start_blade_serial_session(id)
    return "", 204


def _get_blade(id, session):
    blade = session.query(Blade).filter(Blade.id == id).first()
    if blade is None:
        raise exception.NotFound()
    return blade


def _long_action():
    long = request.args.get('long')
    return long is not None and (long.lower() == 'true' or long == '')
