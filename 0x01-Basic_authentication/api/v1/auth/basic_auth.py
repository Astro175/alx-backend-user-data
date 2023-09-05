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
