#!/usr/bin/env python3
""" Module for SessionDBAuth that inherits from SessionExpAuth
"""
from .session_exp_auth import SessionExpAuth
from os import getenv
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''
    The class for handling DB session authentication expiration
    '''
    def __init__(self):
        ''' Overload '''
        super().__init__()

    def create_session(self, user_id=None):
        '''
        Overloads method in parent class and creates and stores new instance
        of UserSession and returns the Session ID
        '''
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession()
            user_session.user_id = user_id
            user_session.session_id = session_id
            user_session.created_at
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        '''
        Overloads method in parent class and returns the User ID by requesting
        UserSession in the database based on session_id
        '''
        if session_id:
            search_dict = {'session_id': session_id}

            try:
                possible_session_obj = UserSession.search(
                                            attributes=search_dict)
            except KeyError:
                return None
            if possible_session_obj:
                session_obj = possible_session_obj[0]
                if self.session_duration <= 0:
                    return session_obj.user_id
                if (session_obj.created_at + timedelta(
                        seconds=self.session_duration) < datetime.now()):
                    return None
                return session_obj.user_id
        return None

    def destroy_session(self, request=None):
        '''
        Overloads method in parent class and destroys the UserSession based on
        the Session ID from the request cookie
        '''
        if request and self.session_cookie(request):
            session_id = self.session_cookie(request)
            search_dict = {'session_id': session_id}

            try:
                possible_session_obj = UserSession.search(
                                                attributes=search_dict)
            except KeyError:
                return False
            if possible_session_obj:
                session_obj = possible_session_obj[0]
                session_obj.remove()
                return True
        return False
