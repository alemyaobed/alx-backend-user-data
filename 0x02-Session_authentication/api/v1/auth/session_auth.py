#!/usr/bin/env python3
""" Module for SessionAuth that inherits from Auth
"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    '''
    The class for handling  session authentication
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' Creates a Session ID for a user_id '''
        if user_id and isinstance(user_id, str):
            session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id
        return None
