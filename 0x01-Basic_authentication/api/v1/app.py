#!/usr/bin/env python3
"""
    The Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth_type = getenv('AUTH_TYPE', 'auth')
auth = None
if auth_type == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request() -> str:
    """
        Before request huandler
    """
    if auth is None:
        return

    allowed_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if auth.require_auth(request.path, allowed_paths):
        auth_header = auth.authorization_header(request)
        user = auth.current_user(request)
        if auth_header is None:
            abort(401)
        if user is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """
        Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
        Handles Unauthorized error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
        Handles Forbidden error
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
