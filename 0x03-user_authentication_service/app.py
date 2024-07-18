#!/usr/bin/env python3
'''
The Flask App model
'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from user import User

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    ''' The home route that returns a JSON payload. '''
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    ''' An end-point to register a new user '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    ''' Logs a user in, creates a user session and returns it as a cookie '''
    email = request.form.get('email')
    password = request.form.get('password')
    login_valid = AUTH.valid_login(email=email, password=password)
    if login_valid:
        payload = {"email": f"{email}", "message": "logged in"}
        session_id = AUTH.create_session(email=email)
        response = jsonify(payload)
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    ''' Logs a user out and deletes the user session '''
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        if user:
            AUTH.destroy_session(user_id=user.id)
            return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    ''' Finds a user '''
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        if user:
            payload = {"email": f"{user.email}"}
            return jsonify(payload), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    ''' Generates a reset password token for a user '''
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email=email)
        payload = {"email": f"{email}", "reset_token": f"{reset_token}"}
        return jsonify(payload), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    ''' Runs if this file or script is executed directly '''
    app.run(host='0.0.0.0', port='5000')
