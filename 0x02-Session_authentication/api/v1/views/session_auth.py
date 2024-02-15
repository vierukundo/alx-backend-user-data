#!/usr/bin/env python3
"""A new Flask view that handles all routes
for the Session authentication."""
import os
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """handles all routes for the Session authentication"""
    email = request.form.get('email')
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    res = jsonify(user[0].to_json())
    session_name = os.getenv('SESSION_NAME')
    if session_name:
        res.set_cookie(session_name, session_id)
    return res
