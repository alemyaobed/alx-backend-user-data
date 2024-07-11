#!/usr/bin/env python3
""" Module for SessionExpAuth that inherits from SessionAuth
"""
from .session_auth import SessionAuth
from uuid import uuid4
from models.user import User
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''
    The class for handling  session authentication expiration
    '''
    def __init__(self):
        ''' Overload '''
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        ''' Overloads the SessionAuth.create_session method '''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        ''' Overloads the SessionAuth.user_id_for_session_id method'''
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        created_at = session_dict.get('created_at')
        if (created_at + timedelta(seconds=self.session_duration) <
                datetime.now()):
            return None

        return session_dict.get('user_id')
