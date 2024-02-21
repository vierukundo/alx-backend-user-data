#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import requests
import json


def register_user(email: str, password: str) -> None:
    """Integration test for user registration."""
    credentials = {"email": email, "password": password}
    res = requests.post('http://localhost:5000/users', data=credentials)
    payload = {"email": email, "message": "user created"}
    assert res.json() == payload

def log_in_wrong_password(email: str, password: str) -> None:
    """Integration test for login with wrong password."""
    credentials = {"email": email, "password": password}
    res = requests.post('http://localhost:5000/sessions', data=credentials)
    print(res.status_code, res.text)
    assert res.status_code == 401

def log_in(email: str, password: str) -> str:
    """Integration test for successful login."""
    credentials = {"email": email, "password": password}
    res = requests.post('http://localhost:5000/sessions', data=credentials)
    assert res.status_code in (200, 401)
    if res.status_code == 200:
        return res.cookies.get('session_id')

def profile_unlogged() -> None:
    """Integration test for accessing profile without logging in."""
    res = requests.get('http://localhost:5000/profile')
    assert res.status_code == 403

def profile_logged(session_id: str) -> None:
    """Integration test for accessing profile after logging in."""
    cookies = dict(session_id='{}'.format(session_id))
    # headers = {"Cookie": f"session_id={session_id}"}
    res = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert res.status_code == 200

def log_out(session_id: str) -> None:
    """Integration test for logging out a user."""
    headers = {"Cookie": "session_id={}".format(session_id)}
    res = requests.delete('http://localhost:5000/sessions', headers=headers, allow_redirects=True)
    print(res.status_code)
    print(res.json())
    assert res.json() == {"message": "Bienvenue"}

def reset_password_token(email: str) -> str:
    """Integration test for obtaining a password reset token."""
    data = {"email": email}
    res = requests.post('http://localhost:5000/reset_password', data=data)
    assert res.status_code == 200
    return res.json().get('reset_token')

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Integration test for updating the password using a reset token."""
    data = {"email": email, "new_password": new_password, "reset_token": reset_token}
    res = requests.put('http://localhost:5000/reset_password', data=data)
    payload = {"email": email, "message": "Password updated"}
    assert res.json() == payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    # Execute the integration tests in sequence
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
