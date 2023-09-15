#!/usr/bin/env python3
"""Basiv flask app"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

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
        payload = {"email": user.email, "message": "user created"}
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
    payload = {"email": email, "message": "logged in".format(email)}
    response = jsonify(payload)
    response.set_cookie('session_id', id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Find the user with the requested session ID. If the user
    exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status."""

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
