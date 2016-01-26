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
from .db import Database, Blade, db

from ruggedpod_api.common import exception
from ruggedpod_api.services import gpio

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
                'description': b.description
            })
        return json.dumps(blades)


@api.route("/blades/<id>", methods=['GET'])
def get_blade(id):
    session = db.session()
    with session.begin():
        blade = session.query(Blade).filter(Blade.id==id).first()
        if blade == None:
            return "", 404
        return json.dumps({
            'id': blade.id,
            'name': blade.name,
            'description': blade.description
        })
