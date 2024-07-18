#!/usr/bin/env python3
'''
Authentication module
'''
from db import DB, User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    ''' Takes in a password string arguments and hashes returns bytes.'''
    encoded_pwd = password.encode('utf-8')
    return hashpw(encoded_pwd, gensalt())


def _generate_uuid() -> str:
    ''' Generates a new UUID and returns it as a string.'''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        ''' Constructor for the class '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' Registers a new user '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password=password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_pwd)
            return new_user
        except Exception as e:
            raise ValueError(f"Error occurred: {e}")

    def valid_login(self, email: str, password: str) -> bool:
        ''' Returns True if email and password are validated, else False '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        '''
        Creates a new session for a user identified by email and returns the
        session id as a string
        '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user.session_id = _generate_uuid()
                self._db.update_user(
                    user_id=user.id, session_id=user.session_id)
                return user.session_id
        except NoResultFound:
            pass
