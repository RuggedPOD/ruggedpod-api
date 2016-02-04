# RuggedPOD management API
#
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
from ruggedpod_api.common import exception
from ruggedpod_api.services import users
from ruggedpod_api.services.db import User

from flask import request


@api.route("/users", methods=['GET'])
def get_users():
    payload = []
    for user in users.find():
        payload.append(_userToDict(user))
    return json.dumps(payload)


@api.route("/users", methods=['POST'])
def create_user():
    data = utils.parse_json_body(request)

    if 'username' not in data:
        raise exception.ParameterMissing(name="username")

    if 'firstname' not in data:
        raise exception.ParameterMissing(name="firstname")

    if 'lastname' not in data:
        raise exception.ParameterMissing(name="lastname")

    user = User(username=data['username'], firstname=data['firstname'], lastname=data['lastname'])

    if 'password' in data:
        user.password = data['password']

    id = users.save(user)
    return get_user(id)


@api.route("/users/<id>", methods=['GET'])
def get_user(id):
    user = users.find(id=id)
    return json.dumps(_userToDict(user))


@api.route("/users/<id>", methods=['PUT'])
def update_user(id):
    data = utils.parse_json_body(request)

    if 'id' in data and int(data['id']) != int(id):
        raise exception.Conflict(reason="Id mismatch")

    if 'firstname' not in data:
        raise exception.ParameterMissing(name="firstname")

    if 'lastname' not in data:
        raise exception.ParameterMissing(name="lastname")

    user = User(firstname=data['firstname'], lastname=data['lastname'])
    user.id = id

    if 'password' in data:
        user.password = data['password']

    users.update(user)
    return get_user(id)


@api.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    users.delete(id)
    return "", 204


def _userToDict(user):
    return {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname
    }
