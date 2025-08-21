import os
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

load_dotenv()

ENCRYPTION_KEY = bytes.fromhex(os.getenv("ENCRYPTION_KEY_AES256"))
SIGNING_KEY = bytes.fromhex(os.getenv("SIGNING_KEY_HMAC"))

if len(ENCRYPTION_KEY) != 32:
    raise ValueError("ENCRYPTION_KEY_AES256 harus 32 byte (64 karakter hex)")
if len(SIGNING_KEY) != 32:
    raise ValueError("SIGNING_KEY_HMAC harus 32 byte (64 karakter hex)")

IV_SIZE = 16
BLOCK_SIZE_BITS = 128


class EncryptionServiceAES256:
    @staticmethod
    def encrypt(plaintext):

        if not plaintext:
            return ''

        # untuk memastikan ukuran blok sesuai standar 128 bit standar pkcs7
        padder = padding.PKCS7(BLOCK_SIZE_BITS).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        # iv untuk pembeda di setiap enkripsinya dan melakukan enkripsi
        iv = os.urandom(IV_SIZE)
        cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # menambahkan signiture
        signature = hmac.new(SIGNING_KEY, iv + ciphertext, hashlib.sha256).digest()

        encrypted_bytes = iv + signature + ciphertext

        return base64.b64encode(encrypted_bytes).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_payload_str):
        if not encrypted_payload_str:
            return ''

        encrypted_payload = base64.b64decode(encrypted_payload_str)

        iv = encrypted_payload[:IV_SIZE]
        signature = encrypted_payload[IV_SIZE: IV_SIZE + 32]
        ciphertext = encrypted_payload[IV_SIZE + 32:]

        # validasi signiture
        expected_signature = hmac.new(SIGNING_KEY, iv + ciphertext, hashlib.sha256).digest()

        # untuk mencegah timing attacks -> serangan dari pencocokan data
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError("Tanda tangan tidak valid. Data mungkin telah diubah.")

        # dekripsi
        cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # menghapus padding
        unpadder = padding.PKCS7(BLOCK_SIZE_BITS).unpadder()
        plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext_bytes.decode('utf-8')
