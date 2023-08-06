import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):

    def __init__(self, key=None, hash_key=None, iv=None):
        if hash_key:
            self.key = hash_key
        else:
            self.key = hashlib.sha256(key.encode()).digest()
        if not iv:
            iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        self.iv = iv

    def encrypt_part(self, raw):
        return self.cipher.encrypt(raw)

    def decrypt_part(self, enc):
        return self.cipher.decrypt(enc)

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded = pad(raw, 16)
        return base64.b64encode(self.iv + cipher.encrypt(padded))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:]), 16)

    @staticmethod
    def pad2(s):
        if len(s) % 16 != 0:
            length = 16 - (len(s) % 16)
            s += bytes([length]) * length
        return s

    @staticmethod
    def pad(s):
        return pad(s, 16)

    @staticmethod
    def unpad(s):
        return unpad(s, 16)
