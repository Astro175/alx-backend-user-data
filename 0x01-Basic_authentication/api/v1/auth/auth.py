#!/usr/bin/env python3

"""
  Module for authentication
"""

from flask import request

class Auth():
    """
      Authentication class
    """
    
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
          Method that depends which path requires
          authentication or not
        """
        return False

    def def authorization_header(self, request=None) -> str:
        """"
           Method for authorization_header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
          Method for current_user
        """
        return None
