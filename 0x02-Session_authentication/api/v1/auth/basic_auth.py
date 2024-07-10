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
        And modified to accept passwords with : in them
        '''
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                not (':' in decoded_base64_authorization_header)):
            return None, None
        # Assuming the email doesn't contain :, meaning the first of the split
        # with : which is at index 0 will be the email. Now combining the email
        # with the : and removing it will be left with the portion representing
        # the password
        # eg: 'email@e.com:pass:word:134' using split will give
        # ['email@e.com', 'pass', 'word', '134'] with index 0 being the email
        # so removing the characters of the email with the first : leaves us
        # with the password
        # email = (decoded_base64_authorization_header.split(':'))[0]
        # remove_email = email + ':'
        # password = decoded_base64_authorization_header.replace(
        #                                                     remove_email, '')

        # A better way: Split on the first occurrence of ':'
        email, password = decoded_base64_authorization_header.split(':', 1)

        return email, password

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

        # In case there is no user instance, there would be a key error using
        # the search method, therefor using try/except
        try:
            possible_user_instance = User.search(attributes=credential_dict)
        except KeyError:
            return None
        if possible_user_instance:
            # Hoping it returns 1 obj since email is unique else the first obj
            user_instance = possible_user_instance[0]
            if user_instance.is_valid_password(user_pwd):
                return user_instance
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Overloads Auth and retrieves the User instance for a request
        '''
        authorization_header = self.authorization_header(request=request)
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header=authorization_header)
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_authorization_header=base64_authorization_header)
        extracted_user_credentials = self.extract_user_credentials(
            decoded_base64_authorization_header=decoded_base64_auth_header)
        email, password = extracted_user_credentials
        current_user_instance = self.user_object_from_credentials(
            user_email=email, user_pwd=password)
        return current_user_instance
