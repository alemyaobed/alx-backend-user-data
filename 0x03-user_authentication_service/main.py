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
    assert response_email == email, \
        f"Expected email {email} but got {response_email}"
    assert response_message == "user created", \
        f"Expected 'user created' but got {response_message}"
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"


def log_in_wrong_password(email: str, password: str) -> None:
    ''' Testing the endpoint for logging in with wrong password '''
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    assert response.status_code == 401, \
        f"Expected 401 but got {response.status_code}"
    assert response.cookies.get('session_id') is None, \
        "Expected no session_id cookie"


def log_in(email: str, password: str) -> str:
    ''' Testing endpoint for logging in with the right credentials '''
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    response_email = response.json().get('email')
    response_message = response.json().get('message')
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert response_email == email, \
        f"Expected email {email} but got {response_email}"
    assert response_message == "logged in", \
        f"Expected 'logged in' but got {response_message}"
    assert response.cookies.get('session_id') is not None, \
        "Expected session_id cookie"
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    '''
    Testing the endpoint for getting the profile of a user with no session id
    to indicate alread logged in
    '''
    url = 'http://localhost:5000/profile'
    response = requests.get(url=url)
    assert response.status_code == 403, \
        f"Expected 403 but got {response.status_code}"


def profile_logged(session_id: str) -> None:
    '''
    Testing the endpoint for getting the profile of a user with the session id
    '''
    url = 'http://localhost:5000/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url=url, cookies=cookies)
    response_email = response.json().get('email')
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert response_email is not None, \
        "Expected an email in the response"


def log_out(session_id: str) -> None:
    '''Testing the endpoint for logging out with the session id '''
    url = 'http://localhost:5000/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url=url, cookies=cookies)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"


def reset_password_token(email: str) -> str:
    ''' Testing the endpoint for password resets '''
    url = 'http://localhost:5000/reset_password'
    data = {'email': email}
    response = requests.post(url=url, data=data)
    response_email = response.json().get('email')
    response_token = response.json().get('reset_token')
    assert response_email == email, \
        f"Expected email {email} but got {response_email}"
    assert response_token is not None, \
        "Expected a reset_token in the response"
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
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
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert response_email == email, \
        f"Expected email {email} but got {response_email}"
    assert response_message == "Password updated", \
        f"Expected 'Password updated' but got {response_message}"


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
