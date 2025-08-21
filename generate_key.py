import os

# Membuat kunci 32-byte untuk enkripsi AES-256
encryption_key = os.urandom(32).hex()

# Membuat kunci 32-byte untuk autentikasi HMAC
signing_key = os.urandom(32).hex()

print(f"ENCRYPTION_KEY_AES256={encryption_key}")
print(f"SIGNING_KEY_HMAC={signing_key}")