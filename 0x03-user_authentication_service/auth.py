#!/usr/bin/env python3

"""Module that hashes a password with bcrypt"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and
    returns bytes, he returned bytes is a salted hash of the
    input password, hashed with bcrypt.hashpw"""
    byte_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(byte_pw, salt)

    return encrypted_password
