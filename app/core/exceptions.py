"""Module to represent API custom exceptions."""

from fastapi.exceptions import HTTPException


class SIGAAException(HTTPException):
    """Base exception for the SIGAA API."""

    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, detail=message)


class LoginFailed(SIGAAException):
    """Exception to be raised when the login fails."""

    def __init__(self) -> None:
        super().__init__(
            "The login failed! This can be due to wrong username or password, "
            "or even a SIGAA error. Please, try again."
        )
