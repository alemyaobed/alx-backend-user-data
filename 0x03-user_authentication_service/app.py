#!/usr/bin/env python3
'''
The Flask App model
'''
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    ''' The home route that returns a JSON payload. '''
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


if __name__ == '__main__':
    ''' Runs if this file or script is executed directly '''
    app.run(host='0.0.0.0', port='5000')
