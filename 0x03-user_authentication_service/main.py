#!/usr/bin/env python3
"""
Main file
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    ''' Testing the registering of user endpoint'''
    url = 'http://localhost:5000/users'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    response_email = response.json().get('email')
    response_message = response.json().get('message')
    assert response_email == email
    assert response_message == "user created"
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    ''' Testing the endpoint for logging in with wrong password '''
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    assert response.status_code == 401
    assert response.cookies.get('session_id') is None


def log_in(email: str, password: str) -> str:
    ''' Testing endpoint for logging in with the right credentials '''
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    response_email = response.json().get('email')
    response_message = response.json().get('message')
    assert response.status_code == 200
    assert response_email == email
    assert response_message == "logged in"
    assert response.cookies.get('session_id') is not None
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    '''
    Testing the endpoint for getting the profile of a user with no session id
    to indicate alread logged in
    '''
    url = 'http://localhost:5000/profile'
    response = requests.get(url=url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    '''
    Testing the endpoint for getting the profile of a user with the session id
    '''
    url = 'http://localhost:5000/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url=url, cookies=cookies)
    response_email = response.json().get('email')
    assert response.status_code == 200
    assert response_email is not None


def log_out(session_id: str) -> None:
    '''Testing the endpoint for logging out with the session id '''
    url = 'http://localhost:5000/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url=url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    ''' Testing the endpoint for password resets '''
    url = 'http://localhost:5000/reset_password'
    data = {'email': email}
    response = requests.post(url=url, data=data)
    response_email = response.json().get('email')
    response_token = response.json().get('reset_token')
    assert response_email == email
    assert response_token is not None
    assert response.status_code == 200
    return response_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    ''' Testing the endpoint for updating password with a reset token'''
    url = 'http://localhost:5000/reset_password'
    data = {
                'email': email,
                'reset_token': reset_token,
                'new_password': new_password
    }
    response = requests.put(url=url, data=data)
    response_email = response.json().get('email')
    response_message = response.json().get('message')
    assert response.status_code == 200
    assert response_email == email
    assert response_message == "Password updated"


if __name__ == "__main__":
    ''' Contents below to be executed if file is run and not imported '''
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
