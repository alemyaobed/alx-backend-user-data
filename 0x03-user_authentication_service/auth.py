#!/usr/bin/env python3
'''
Authentication module
'''
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    ''' Takes in a password string arguments and hashes returns bytes.'''
    encoded_pwd = password.encode('utf-8')
    return hashpw(encoded_pwd, gensalt())
