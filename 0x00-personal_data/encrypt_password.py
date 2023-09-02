#!/usr/bin/env python3

"""
  Function that uses bcrypt to encrypt
  a password into a hash
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
      Takes a string argument password and returns
      a byte hashed password
    """

    pw_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(pw_bytes, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
      Checks if a hashed password was created from the string
      password, if true, it authenticates the user
    """

    pw_bytes = password.encode("utf-8")

    check = bcrypt.checkpw(pw_bytes, hashed_password)

    return check
