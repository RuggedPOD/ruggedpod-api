import base64
import hashlib
import uuid

from Crypto.Cipher import AES
from Crypto import Random

from . import singleton, exception


def generate_uuid():
    return uuid.uuid4().hex


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


class DecryptFailed(exception.RuggedpodException):
    msg_fmt = "Cypher cannot be decrypted"
    status_code = 500


class Cipher(object):
    __metaclass__ = singleton.Singleton

    def __init__(self, secret_key):
        self.key = hashlib.sha256(secret_key.encode()).digest()

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
            raise DecryptFailed()

    @staticmethod
    def _pad(s):
        length = 16 - len(s) % 16
        return s + length * chr(length)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
