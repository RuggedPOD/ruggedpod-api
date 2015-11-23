
import os
import json
import time

from common import exception
from common.conf import YmlConf
from cryptography.fernet import Fernet


auth = YmlConf("conf.yaml").get_attr('authentication')
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
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, text):
        return self.cipher_suite.encrypt(b"%s" % text)

    def decrypt(self, cipher):
        try:
            return self.cipher_suite.decrypt(cipher.encode("ascii"))
        except:
            raise AuthenticationFailed()


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
