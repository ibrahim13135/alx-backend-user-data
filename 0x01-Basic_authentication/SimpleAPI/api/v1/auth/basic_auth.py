from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """
        Returns Authorization header-the Base64 part of the:
        Args:
            the Base64 part of the  authorization header:

        Returns:
            encoded values - A string of Base64
        """
        # Return None if authorization_header is None
        # Return None if authorization_header is not a string
        # Return None if authorization_header doesn’t start by Basic (with a space at the end)
        # Otherwise, return the value after Basic (after the space)
        # You can assume authorization_header contains only one Basic
        # to allow password with :
        if authorization_header is None:
            return None

        if type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a Base64 string."""
        # Return None if base64_authorization_header is None
        # Return None if base64_authorization_header is not a string
        # Return None if base64_authorization_header is not a valid Base64 - you can use try/except
        # Otherwise, return the decoded value as UTF8 string - you can use
        # decode('utf-8')
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (TypeError, base64.binascii.Error):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extracts user credentials (email and password) from the decoded Base64 string."""
        # This method must return 2 values
        # Return None, None if decoded_base64_authorization_header is None
        # Return None, None if decoded_base64_authorization_header is not a string
        # Return None, None if decoded_base64_authorization_header doesn’t contain :
        # Otherwise, return the user email and the user password - these 2 values must be separated by a :
        # You can assume decoded_base64_authorization_header will contain only
        # one :
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on email and password."""
        # Return None if user_email is None or not a string
        # Return None if user_pwd is None or not a string
        # Return None if your database (file) doesn’t contain any User instance with email equal to user_email - you should use the class method search of the User to lookup the list of users based on their email. Don’t forget to test all cases: “what if there is no user in DB?”, etc.
        # Return None if user_pwd is not the password of the User instance found - you must use the method is_valid_password of User
        # Otherwise, return the User instance
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request using Basic Auth."""
        # You must use authorization_header
        # You must use extract_base64_authorization_header
        # You must use decode_base64_authorization_header
        # You must use extract_user_credentials
        # You must use user_object_from_credentials
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
