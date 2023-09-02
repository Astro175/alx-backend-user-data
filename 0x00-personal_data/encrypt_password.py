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

    hash = bcrypt.hashpw(pw_bytes, salt)

    return hash
