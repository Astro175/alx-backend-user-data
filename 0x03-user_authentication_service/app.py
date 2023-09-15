#!/usr/bin/env python3
"""Basiv flask app"""

from auth import Auth
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route('/users', methods=['POST'])
def users():
    """Post user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        payload = {"email": "{}", "message": "user created".format(email)}
        return jsonify(payload)
    except ValueError:
        payload = {"message": "email already registered"}
        return jsonify(payload), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Checks for credentials and logs in user"""
    email = request.form.get('email')
    password = request.form.get('password')

    status = AUTH.valid_login(email, password)

    if not status:
        abort(401)
    id = AUTH.create_session(email)
    payload = {"email": "<user email>", "message": "logged in"}
    response = jsonify(payload)
    response.set_cookie('session_id', id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
