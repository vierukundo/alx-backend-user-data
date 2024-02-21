#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, request, jsonify, make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """GET route to return a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Endpoint to register a user."""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Endpoint to handle user login."""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response_data = {"email": email, "message": "logged in"}
        response = make_response(jsonify(response_data), 200)
        response.set_cookie("session_id", session_id)

        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Handle a DELETE request to log out a user."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Look out the user in database and return 200 code if ok"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route(
        "/reset_password",
        methods=["GET"], strict_slashes=False)
def get_reset_password_token():
    """Extract email from form data"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    response = {"email": email, "reset_token": reset_token}
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
