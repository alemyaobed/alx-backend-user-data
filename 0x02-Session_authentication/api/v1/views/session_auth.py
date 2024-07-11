#!/usr/bin/env python3
""" Module of Session authentication.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - logging a user in, creating a session for the user and returning a
        session cookie
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    credential_dict = {'email': email}

    # In case there is no user instance, there would be a key error using
    # the search method, therefor using try/except
    try:
        possible_user_instance = User.search(attributes=credential_dict)
    except KeyError:
        return jsonify({"error": "no user found for this email"}), 404

    if possible_user_instance:
        # Hoping it returns 1 obj since email is unique else the first obj
        user_instance = possible_user_instance[0]
        if not user_instance.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth

            session_id = auth.create_session(user_instance.id)
            response = jsonify(user_instance.to_json())
            cookie_name = getenv('SESSION_NAME')
            response.set_cookie(cookie_name, session_id)
            return response
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - logging out a user by deleting a session based on the session cookie
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
