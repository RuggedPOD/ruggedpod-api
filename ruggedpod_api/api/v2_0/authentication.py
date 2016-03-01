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
import datetime

from .blueprint import api

from ruggedpod_api import config
from ruggedpod_api.common import exception
from ruggedpod_api.services import auth

from flask import request, make_response
from flask import g as request_context

auth_enabled = config.get_attr('authentication')['enabled']


@api.before_request
def check_authentication():
    if not auth_enabled:
        return
    if request.path.endswith('/tokens') and request.method == 'POST':
        return
    token_key = 'X-Auth-Token'
    if token_key in request.cookies:
        token = request.cookies[token_key]
    else:
        if token_key in request.headers:
            token = request.headers[token_key]
        else:
            raise auth.AuthenticationFailed()
    user = auth.check(token)
    request_context.user = user


@api.route("/tokens", methods=['POST'])
def authenticate():
    try:
        data = json.loads(request.data)
    except ValueError:
        raise exception.BodySyntaxError()

    if 'username' not in data:
        raise exception.ParameterMissing(name="username")
    if 'password' not in data:
        raise exception.ParameterMissing(name="password")

    token, expires = auth.get_token(data['username'], data['password'])

    date = datetime.datetime.fromtimestamp(expires).strftime('%Y-%m-%dT%H:%M:%SZ')

    resp_data = {
        'token': token,
        'expires': date
    }
    response = make_response(json.dumps(resp_data), 201)
    response.set_cookie('X-Auth-Username', data['username'], expires=expires)
    response.set_cookie('X-Auth-Token', token, expires=expires)
    return response
