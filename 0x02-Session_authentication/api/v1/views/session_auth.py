#!/usr/bin/env python3
"""
  Module that for routes for session_auth
"""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """
      Methods for session_auth
    """
    password = request.form.get('password')
    email = request.form.get('email')

    if email == '' or email is None:
        return jsonify({"error": "email missing"}), 400
    if password is '' or password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users or users is []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            data = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            data.set_cookie(session_name, session_id)
            return data
        return jsonify({"error": "wrong password"})
