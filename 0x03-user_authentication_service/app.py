#!/usr/bin/env python3
'''
The Flask App model
'''
from flask import Flask, jsonify, request
from auth import Auth

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


if __name__ == '__main__':
    ''' Runs if this file or script is executed directly '''
    app.run(host='0.0.0.0', port='5000')
