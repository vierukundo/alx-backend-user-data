#!/usr/bin/env python3
"""Module to manage the API authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Add a trailing slash to the path for slash tolerance
        path_with_slash = path + '/' if not path.endswith('/') else path

        # Check if the path (with trailing slash) is in excluded_paths
        return path_with_slash not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Returns None for now, implementation will be added later.
        """
        if request is None:
            return None
        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return None
        else:
            return authorization_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None for now, implementation will be added later.
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        session_name = os.getenv('SESSION_NAME')
        if request is None or session_name is None:
            return None
        cookie_value = request.cookies.get(session_name)
        return cookie_value
