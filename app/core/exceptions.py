"""Module to represent API custom exceptions."""

from fastapi.exceptions import HTTPException
from fastapi import status, Request, FastAPI
from fastapi.responses import JSONResponse


class SIGAAException(HTTPException):
    """Base exception for the SIGAA API."""

    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class LoginFailed(SIGAAException):
    """Exception to be raised when the login fails."""

    def __init__(self) -> None:
        super().__init__(
            "The login failed! This can be due to wrong username or password, "
            "or even a SIGAA error. Please, try again."
        )


def login_failed_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.detail}
    )

def include_app(app: FastAPI):
    app.add_exception_handler(LoginFailed, login_failed_handler)
