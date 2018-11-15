# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64

def encrypt_password(password):
    PADDING = '\0'
    pad_it = lambda s: s+(16 - len(s)%16)*PADDING
    key = '1234567812345678'
    iv = '1234567812345678'
    source = password
    generator = AES.new(key, AES.MODE_CBC, iv)
    crypt = generator.encrypt(pad_it(source))
    cryptedStr = base64.b64encode(crypt)
    return cryptedStr