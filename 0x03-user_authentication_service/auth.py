#!/usr/bin/env python3

"""Module that hashes a password with bcrypt"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Should take mandatory email and password string
        arguments and return a User object."""

        try:
            old_user = self._db.find_user_by(email=email)

        except NoResultFound:
            hashed_pw = _hash_password(password)
            user = self._db.add_user(email, hashed_pw)
        else:
            raise ValueError("User {} already exists".format(email))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Takes an email and password and checks them"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        bytes_pw = password.encode('utf-8')
        result = bcrypt.checkpw(bytes_pw, user.hashed_password)
        return result

    def create_session(self, email: str):
        """Checks email and generates a session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        id = _generate_uuid()
        user.session_id = id
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """If the session ID is None or no user is found,
        return None. Otherwise return the corresponding user"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """The method updates the corresponding user's
        session ID to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email. If the user does not
        exist, raise a ValueError exception. If it exists, generate a UUID
        and update the user's reset_token database field. Return the token."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user.reset_token = str(uuid4())
        return user.reset_token


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and
    returns bytes, he returned bytes is a salted hash of the
    input password, hashed with bcrypt.hashpw"""
    byte_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(byte_pw, salt)

    return encrypted_password


def _generate_uuid() -> str:
    """The function should return a string representation
    of a new UUID. """
    id = str(uuid4())
    return id
