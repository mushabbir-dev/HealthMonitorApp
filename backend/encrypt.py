from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# 16-byte key (AES-128), should be kept secret
SECRET_KEY = b'ThisIsA16ByteKey'

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + chr(pad_len) * pad_len

def unpad(data):
    pad_len = ord(data[-1])
    return data[:-pad_len]

def encrypt_data(plain_text):
    plain_text = pad(plain_text)
    iv = get_random_bytes(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(plain_text.encode('utf-8'))
    return base64.b64encode(iv + encrypted).decode('utf-8')

def decrypt_data(enc_text):
    enc = base64.b64decode(enc_text)
    iv = enc[:16]
    encrypted = enc[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted).decode('utf-8')
    return unpad(decrypted)
