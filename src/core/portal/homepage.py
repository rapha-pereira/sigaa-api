"""Module to represent the SIGAA portal core."""

from src.core.login.portal_login import PortalLogin
from src.core.login.login_model import LoginModel
from src.core.portal.classes import Classes


class StudentPortal:
    """
    A class that represents the SIGAA main page.
    https://sig.ifsc.edu.br/sigaa/portais/discente/
    """

    def __init__(self, username: str = "", password: str = "") -> None:
        self.parser = self._login(username, password).parse_response()

    def _login(self, username: str = "", password: str = "") -> LoginModel:
        """Method to login into the SIGAA portal."""
        return PortalLogin(username=username, password=password).login()

    def get_classes_portal(self) -> Classes:
        """Returns an instance of the Classes class."""
        return Classes(parser=self.parser)
