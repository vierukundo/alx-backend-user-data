#!/usr/bin/env python3
"""Basic Auth module"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the Base64
        decoded authorization header.
        :return: A tuple containing user email and password,
        or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        # Check if decoded_base64_authorization_header contains ':'
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string into email and password using ':'
        user_credentials = decoded_base64_authorization_header.split(':')

        return tuple(user_credentials)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Look up the list of users based on their credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            credentials = {'email': user_email}
            users = User.search(credentials)
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            # Return None if no valid user is found
            return None
        except (KeyError, TypeError):
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        auth = self.authorization_header(request)
        extracted = self.extract_base64_authorization_header(auth)
        decoded = self.decode_base64_authorization_header(extracted)
        email, password = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, password)
