#!/usr/bin/env python3
"""
SessionExpAuth module
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class
    """
    def __init__(self):
        """
        Constructor method
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_id_by_session_id = self.user_id_by_session_id
        user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the User ID for a Session ID
        """
        if session_id is None:
            return None

        user_id_by_session_id = self.user_id_by_session_id

        if session_id not in user_id_by_session_id:
            return None

        session_dict = user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        if "created_at" not in session_dict:
            return None

        created_at = session_dict["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
