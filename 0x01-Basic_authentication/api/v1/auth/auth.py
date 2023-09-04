#!/usr/bin/env python3

"""
  Module for authentication
"""
from typing import List, TypeVar

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
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        len_path = len(path)

        if path[len_path - 1] == '/':
            slashed_path = path
        else:
            slashed_path = path + '/'

        if slashed_path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """"
           Method for authorization_header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
          Method for current_user
        """
        return None
