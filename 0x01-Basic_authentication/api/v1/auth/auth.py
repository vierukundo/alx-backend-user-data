#!/usr/bin/env python3
"""Module to manage the API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.
        Returns False for now, implementation will be added later.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None for now, implementation will be added later.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None for now, implementation will be added later.
        """
        return None
