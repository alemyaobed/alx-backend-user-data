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
        ''' Returns False for now '''
        return False

    def authorization_header(self, request=None) -> str:
        ''' Returns None for now '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Returns None for now '''
        return None
