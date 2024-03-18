"""Module to represent the SIGAA portal core."""

from fastapi.security import HTTPBasicCredentials
from fastapi.exceptions import HTTPException
from fastapi import status

from typing import List, Union

from sigaa_api.sigaa.models import Course, Profile
from sigaa_api.sigaa.login.portal_login import PortalLogin
from sigaa_api.sigaa.course.portal_courses import PortalCourses
from sigaa_api.sigaa.profile.portal_profile import PortalProfile


class StudentPortal:
    """
    A class that represents the SIGAA main page.
    https://sig.ifsc.edu.br/sigaa/portais/discente/
    """

    def __init__(self, credentials: HTTPBasicCredentials, option: str) -> None:
        self._credentials = credentials
        self.option = option
        self.parser = None

    def _get_courses(self) -> Union[List[Course], None]:
        """Returns a list of courses the student is enrolled in."""
        return PortalCourses(parser=self.parser).get_courses()

    def _get_activities(self) -> None:
        """Returns a list of activities the student is enrolled in."""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet."
        )

    def _get_profile_additional(self) -> Union[Profile, None]:
        """Returns the student profile with additional info."""
        return PortalProfile(parser=self.parser).get_profile()

    def login(self) -> None:
        """Login to the SIGAA portal."""
        self.sigaa_login = PortalLogin(credentials=self._credentials).login()

    def handle(self) -> Union[List[Course], Profile, None]:
        """Handle the request based on the option."""
        self.parser = self.sigaa_login.parse_response()
        options = {
            "courses": self._get_courses,
            "activities": self._get_activities,
            "profile": self._get_profile_additional,
        }
        option_class = options.get(self.option)
        return option_class() if option_class else None
