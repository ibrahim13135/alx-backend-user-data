from typing import List, TypeVar
from flask import request
import fnmatch


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        based on the path and excluded paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths
            that do not require authentication.

        Returns:
            bool: True if authentication is required,
            False otherwise.
        """
        # returns True if the path is not in the list of strings
        # excluded_paths:

        # Returns True if path is None
        # Returns True if excluded_paths is None or empty
        # Returns False if path is in excluded_paths
        # You can assume excluded_paths contains string path always ending by a /
        # This method must be slash tolerant: path=/api/v1/status
        # and path=/api/v1/status/ must be returned False if excluded_paths
        # contains /api/v1/status/
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        l_path = len(path)
        if l_path == 0:
            return True

        slash_path = True if path[l_path - 1] == '/' else False

        tmp_path = path
        if not slash_path:
            tmp_path += '/'

        for excluded_path in excluded_paths:
            l_excluded_path = len(excluded_path)
            if l_excluded_path == 0:
                continue

            if excluded_path[l_excluded_path - 1] != '*':
                if tmp_path == excluded_path:
                    return False
            else:
                if excluded_path[:-1] == path[:l_excluded_path - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header from the request """
        # If request is None, returns None
        # If request doesn’t contain the header key Authorization, returns None
        # Otherwise, return the value of the header request Authorization
        if request is None:
            return None
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user """
        return None
