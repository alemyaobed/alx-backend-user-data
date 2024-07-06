#!/usr/bin/env python3
'''
User passwords should NEVER be stored in plain text in a database.

Implement a hash_password function that expects one string argument
name password and returns a salted, hashed password, which is a byte
string.

Use the bcrypt package to perform the hashing (with hashpw).
'''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' Hashing using bcrypt and returning a byte string'''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    Implement an is_valid function that expects 2 arguments and returns a
    boolean.

    Arguments:

    hashed_password: bytes type
    password: string type
    Use bcrypt to validate that the provided password matches the hashed
    password.
    '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)