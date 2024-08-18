"""Module to represent API custom exceptions."""

from fastapi import status


class SIGAAException:
    """Base exception for the SIGAA API."""

    def __init__(self, message: str, status_code) -> None:
        self.message = message
        self.status_code = status_code


class LoginFailed(SIGAAException):
    """Exception to be raised when the login fails."""

    def __init__(self) -> None:
        super().__init__(
            message="The login failed! This can be due to wrong username or password, "
            "or even a SIGAA error. Please, try again.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
