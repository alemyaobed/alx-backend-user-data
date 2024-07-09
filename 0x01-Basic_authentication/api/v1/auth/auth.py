#!/usr/bin/env python3
""" Module for Auth
"""
from flask import request
from typing import List, TypeVar


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
        return True

    def authorization_header(self, request=None) -> str:
        ''' Returns None for now '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Returns None for now '''
        return None
