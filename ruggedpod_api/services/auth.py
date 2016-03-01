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

import os
import json
import time

from Crypto import Random

from ruggedpod_api import config
from ruggedpod_api.common import exception, security
from ruggedpod_api.services import users


auth = config.get_attr('authentication')


class AuthenticationFailed(exception.RuggedpodException):
    msg_fmt = "Authentication failed"
    status_code = 401


def get_token(username, password):

    try:
        user = users.find(username=username)
    except exception.NotFound:
        raise AuthenticationFailed()

    if not security.check_password(user.password, password):
        raise AuthenticationFailed()

    create_date = int(round(time.time()))
    expire_date = create_date + auth['token_lifetime']

    data = {
        "username": username,
        "create_date": create_date,
        "expire_date": expire_date,
        "salt": os.urandom(32).encode('base_64'),
    }

    token = security.Cipher(auth['secret_key']).encrypt(json.dumps(data))

    return (token, expire_date)


def check(token):
    if token == auth['token_admin']:
        return

    identity = json.loads(security.Cipher(auth['secret_key']).decrypt(token))

    try:
        user = users.find(username=identity['username'])
    except exception.NotFound:
        raise AuthenticationFailed()

    current_date = int(round(time.time()))

    if current_date > identity['expire_date']:
        raise AuthenticationFailed()

    return user
