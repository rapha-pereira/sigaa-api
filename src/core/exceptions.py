"""Module to represent API custom exceptions."""


class SIGAAException(Exception):
    """Base exception for the SIGAA API."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class LoginFailed(SIGAAException):
    """Exception to be raised when the login fails."""

    def __init__(self) -> None:
        super().__init__(
            "The login failed! This can be due to wrong username or password, "
            "or even a SIGAA error. Please, try again."
        )
