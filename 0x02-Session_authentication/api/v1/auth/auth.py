#!/usr/bin/env python3
""" Module for Auth
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    '''
    The class for handling authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Determines if a given path requires authentication '''
        if path and excluded_paths:

            # Normalize the path to ensure it ends with a slash
            if not path.endswith('/'):
                path += '/'

            if path in excluded_paths:
                return False

            for excluded_path in excluded_paths:
                # Normalize excluded_path to ensure it ends with a slash
                # if not excluded_path.endswith('/'):
                #     excluded_path += '/'

                # Check for exact match or pattern match
                if excluded_path.endswith('*'):
                    if path.startswith(excluded_path[:-1]):
                        return False
                elif path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
        Extracts the Authorization header from the Flask request object.
        '''
        if request and request.headers.get('Authorization'):
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Returns None for now '''
        return None

    def session_cookie(self, request=None):
        ''' Returns a cookie value from a request '''
        if request:
            cookie_name = getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
        return None
