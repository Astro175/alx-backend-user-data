#!/usr/bin/env python3

"""Module that hashes a password with bcrypt"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound


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


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and
    returns bytes, he returned bytes is a salted hash of the
    input password, hashed with bcrypt.hashpw"""
    byte_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(byte_pw, salt)

    return encrypted_password
