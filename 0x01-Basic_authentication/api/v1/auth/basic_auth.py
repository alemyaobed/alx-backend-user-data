#!/usr/bin/env python3
""" Module for BasicAuth that inherits from Auth
"""
from .auth import Auth


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


    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        Returns the user email and password from the Base64 decoded value
        '''
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                not (':' in decoded_base64_authorization_header)):
            return None, None
        username, password = tuple(decoded_base64_authorization_header.split(':'))
        
        return username, password
