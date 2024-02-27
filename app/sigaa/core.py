"""Module to represent the SIGAA portal core."""

from fastapi.security import HTTPBasicCredentials

from typing import List, Union

from app.sigaa.schemas import Course
from app.sigaa.login.portal_login import PortalLogin
from app.sigaa.course.portal_courses import PortalCourses


class StudentPortal:
    """
    A class that represents the SIGAA main page.
    https://sig.ifsc.edu.br/sigaa/portais/discente/
    """

    def __init__(self, credentials: HTTPBasicCredentials, option: str) -> None:
        _sigaa_login = PortalLogin(credentials=credentials).login()
        self.parser = _sigaa_login.parse_response()
        self.option = option

    def _get_courses(self) -> Union[List[Course], None]:
        """Returns a list of courses the student is enrolled in."""
        return PortalCourses(parser=self.parser).get_courses()

    def handle(self) -> Union[List[Course], None]:
        """Handle the request based on the option."""
        if self.option == "course":
            return self._get_courses()
        return None
