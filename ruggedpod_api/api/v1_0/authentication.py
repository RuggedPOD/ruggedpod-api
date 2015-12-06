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

from .blueprint import api

from ruggedpod_api import config
from ruggedpod_api.common import exception
from ruggedpod_api.services import auth

from flask import request, make_response

auth_enabled = config.get_attr('authentication')['enabled']


@api.before_request
def check_authentication():
    if not auth_enabled:
        return
    if request.path.endswith('/token') and request.method == 'POST':
        return
    token_key = 'X-Auth-Token'
    if token_key in request.cookies:
        token = request.cookies[token_key]
    else:
        if token_key in request.headers:
            token = request.headers[token_key]
        else:
            raise auth.AuthenticationFailed()
    auth.check(token)


@api.route("/token", methods=['POST'])
def authenticate():
    if 'username' not in request.args:
        raise exception.ParameterMissing(name="username")
    if 'password' not in request.args:
        raise exception.ParameterMissing(name="password")

    token, expires = auth.get_token(request.args['username'],
                                    request.args['password'])
    response = make_response('', 201)
    response.set_cookie('X-Auth-Username', request.args['username'], expires=expires)
    response.set_cookie('X-Auth-Token', token, expires=expires)
    return response
