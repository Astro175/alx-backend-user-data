#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
key = getenv("AUTH_TYPE")

auth = key

if auth == 'auth':
    auth = Auth()
elif auth == 'basic_auth':
    auth = BasicAuth()
elif auth == 'session_auth':
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def un_authorized(error) -> str:
    """
      Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
      Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def check_auth() -> str:
    """
       Checks the path for authentication
       before_request
    """
    get_header = auth.authorization_header(request)
    get_user = auth.current_user(request)
    request.current_user = auth.current_user(request)

    if auth is None:
        pass
    no_auth_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                    '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    check = auth.require_auth(request.path, no_auth_list)

    if not check:
        pass
    else:
        if not get_header:
            abort(401)
        if not get_user:
            abort(403)
    if auth.authorization_header(request) and \
            auth.session_cookie(request):
        abort(401)
        return None


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
