#!/usr/bin/env python3

"""
  Module that instantiates an AUth
  class Model
"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
      BasicAuth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
           Method that checks the header and
           extract_base64_authorization_header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[0:6] != "Basic ":
            return None
        if len(authorization_header) < 6:
            return None
        value = authorization_header[6:]
        return value

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
          Method that converts base64 header to a normal
          string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_str = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        decoded_utf = decoded_str.decode('utf-8')
        return decoded_utf

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
          Method that retrieves the user's email and password
          from the decoded string, works only if ':' is included
        """

        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_cred = decoded_base64_authorization_header.split(":")
        email = user_cred[0]
        password = user_cred[1]
        return email, password
