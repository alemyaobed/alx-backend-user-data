#!/usr/bin/env python3
'''
User passwords should NEVER be stored in plain text in a database.

Implement a hash_password function that expects one string argument
name password and returns a salted, hashed password, which is a byte
string.

Use the bcrypt package to perform the hashing (with hashpw).
'''
from bcrypt import hashpw, checkpw, gensalt


def hash_password(password: str) -> bytes:
    ''''''
    hashed = hashpw(password.encode(), gensalt())
    return hashed
