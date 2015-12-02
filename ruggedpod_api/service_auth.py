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
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

from ruggedpod_api import config
from ruggedpod_api.common import exception


auth = config.get_attr('authentication')
users = auth['users']


class AuthenticationFailed(exception.RuggedpodException):
    msg_fmt = "Authentication failed"
    status_code = 401


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class Cypher(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.key = hashlib.sha256(auth['secret_key'].encode()).digest()

    def encrypt(self, raw):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(self._pad(raw)))

    def decrypt(self, enc):
        try:
            dec = base64.b64decode(enc)
            iv = dec[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(dec[AES.block_size:])).decode('utf-8')
        except:
            raise AuthenticationFailed()

    @staticmethod
    def _pad(s):
        length = 16 - len(s) % 16
        return s + length * chr(length)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def get_token(username, password):
    if username not in users:
        raise AuthenticationFailed()

    if password != users[username]:
        raise AuthenticationFailed()

    create_date = int(round(time.time()))
    expire_date = create_date + auth['token_lifetime']

    data = {
        "username": username,
        "create_date": create_date,
        "expire_date": expire_date,
        "salt": os.urandom(32).encode('base_64'),
    }

    token = Cypher().encrypt(json.dumps(data))

    return (token, expire_date)


def check(token):
    identity = json.loads(Cypher().decrypt(token))

    if identity['username'] not in users:
        raise AuthenticationFailed()

    current_date = int(round(time.time()))

    if current_date > identity['expire_date']:
        raise AuthenticationFailed()
