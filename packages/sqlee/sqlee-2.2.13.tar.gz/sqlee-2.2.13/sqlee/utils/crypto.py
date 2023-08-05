from Crypto.Cipher import AES
import base64
import binascii
import quopri
import json

class CryptoHandler:
    def __init__(self, key=None, iv=None, crypto=True):
        self.crypto = crypto
        if not self.crypto:
            return
        if key and not iv:
            self.key = key
            self.iv = key
        elif not key and iv:
            self.key = iv
            self.iv = iv
        elif key and iv:
            self.key = iv
            self.iv = iv
        else:
            self.key = b'.\x9c\xd0\xc31\xb0\x89\xe8\xc3\xf5\xc3\x89\xfcG\x1a6'
            self.iv = self.key

    def encrypt(self, string):
        if not self.crypto:
            return string
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        return binascii.b2a_hex(cipher.encrypt(base64.b64encode(binascii.b2a_hex(quopri.encodestring(binascii.b2a_qp(string.encode())))))).decode()

    def decrypt(self, string):
        if not self.crypto:
            return string
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        return binascii.a2b_qp(quopri.decodestring(binascii.a2b_hex(base64.b64decode(cipher.decrypt(binascii.a2b_hex(string.encode())))))).decode()

    def encrypt_to_str(self, string):
        if not self.crypto:
            return string
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        return binascii.b2a_hex(cipher.encrypt(base64.b64encode(binascii.b2a_hex(quopri.encodestring(binascii.b2a_qp(string.encode())))))).decode()

    def decrypt_by_str(self, string):
        if not self.crypto:
            return string
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        return binascii.a2b_qp(quopri.decodestring(binascii.a2b_hex(base64.b64decode(cipher.decrypt(binascii.a2b_hex(string.encode())))))).decode()

if __name__ == "__main__":
    crypto = CryptoHandler()
    print(crypto.encrypt(json.dumps({"key": "data"})))