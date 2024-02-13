#!/usr/bin/env python3
"""Basic Auth module"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 Authorization header and returns
        the decoded value as a UTF-8 string.

        :param base64_authorization_header: The Base64
        Authorization header string.
        :return: The decoded value as a UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            # Decode Base64
            decoded_value = base64.b64decode(base64_authorization_header)
            # Convert to UTF-8 string
            utf8_string = decoded_value.decode('utf-8')
            return utf8_string
        except base64.binascii.Error:
            # Handle invalid Base64
            return None
