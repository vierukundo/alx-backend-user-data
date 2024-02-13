#!/usr/bin/env python3
"""Basic Auth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Auth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        :param authorization_header: The Authorization header string.
        :return: The Base64 part of the Authorization header,
        or None if invalid.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        # Check if the header starts with 'Basic ' (with a space at the end)
        if not authorization_header.startswith('Basic '):
            return None

        # Extract the Base64 part after 'Basic '
        base64_part = authorization_header.split(' ')[1]

        return base64_part
