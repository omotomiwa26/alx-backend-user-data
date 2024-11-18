#!/usr/bin/env python3
"""
    This class manages API authentication
"""
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """
        This Returns Authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            This Checks if authentication is required for path.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
            Checks for authorization header in request
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Returns None
        """
        return None
