#!/usr/bin/env python3
""" Module for BasicAuth that inherits from Auth
"""
from .auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    '''
    The class for handling  basic authentication
    '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        Returns the Base64 part of the Authorization header for a
        Basic Authentication
        '''
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                authorization_header[:6] != 'Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        Returns the decoded value of a
        Base64 string base64_authorization_header
        '''
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        Returns the user email and password from the Base64 decoded value
        '''
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                not (':' in decoded_base64_authorization_header)):
            return None, None
        username, password = tuple(
                                decoded_base64_authorization_header.split(':'))

        return username, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        Returns the User instance based on his email and password
        '''
        if (user_email is None or user_pwd is None or
                not isinstance(user_pwd, str) or
                not isinstance(user_email, str)):
            return None
        credential_dict = {'email': user_email}
        possible_user_instance = User.search(attributes=credential_dict)
        if possible_user_instance:
            # Hoping it returns 1 obj since email is unique else the first obj
            user_instance = possible_user_instance[0]
            if user_instance.is_valid_password(user_pwd):
                return user_instance
        return None
