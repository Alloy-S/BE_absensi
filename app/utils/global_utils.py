import random
import string

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def generate_username(length=8):
    chars = string.digits
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def format_string(string, params):
    return string.format(**params)