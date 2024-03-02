"""Module to represent the SIGAA portal core."""

from fastapi.security import HTTPBasicCredentials

from typing import List, Union

from app.sigaa.schemas import Course, Profile
from app.sigaa.login.portal_login import PortalLogin
from app.sigaa.course.portal_courses import PortalCourses
from app.sigaa.profile.portal_profile import PortalProfile


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

    def _get_profile_basic(self) -> Union[Profile, None]:
        """Returns the student profile."""
        return PortalProfile(parser=self.parser).get_profile_with_basic_info()

    def _get_profile_additional(self) -> Union[Profile, None]:
        """Returns the student profile with additional info."""
        return PortalProfile(parser=self.parser).get_profile_with_additional_info()

    def handle(self) -> Union[List[Course], Profile, List, None]:
        """Handle the request based on the option."""
        match self.option:
            case "course":
                return self._get_courses()
            case "profile_basic":
                return self._get_profile_basic()
            case "profile_additional":
                return self._get_profile_additional()
            case "all":
                return [self._get_courses(), self._get_profile_additional()]
            case _:
                return None
