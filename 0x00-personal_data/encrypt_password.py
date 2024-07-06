#!/usr/bin/env python3
'''
Hashing passwords
'''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' Hashing using bcrypt and returning a byte string'''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' Checks if a hashed password is valid'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
