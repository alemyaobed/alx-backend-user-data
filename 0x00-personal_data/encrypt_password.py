#!/usr/bin/env python3
'''
User passwords should NEVER be stored in plain text in a database.

Implement a hash_password function that expects one string argument
name password and returns a salted, hashed password, which is a byte
string.

Use the bcrypt package to perform the hashing (with hashpw).
'''
from bcrypt import hashpw, gensalt


def hash_password(password: str) -> bytes:
    ''' Hashing using bcrypt and returning a byte string'''
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed
