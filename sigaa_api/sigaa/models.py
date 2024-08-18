import requests
from datetime import datetime, date
from pydantic import BaseModel, HttpUrl, ConfigDict
from selectolax.lexbor import LexborHTMLParser
from urllib.parse import urljoin

from sigaa_api.sigaa.examples import ex_courses, ex_activities, ex_profile
from sigaa_api.core.config import (
    SIGAA_SITE_ENTRYPOINT,
    SIGAA_LOGIN_FORM_ENDPOINT,
)


class SIGAALogin(BaseModel):
    response: requests.Response

    def parse_response(self) -> LexborHTMLParser:
        """Method to parse the response to a LexborHTMLParser object."""
        return LexborHTMLParser(self.response.text)

    def ok(self) -> bool:
        """Method to check if the login was successfull.\n
        This method checks if the response URL is different from the login URL that
        was used to login.\n
        """
        login_url = urljoin(SIGAA_SITE_ENTRYPOINT, SIGAA_LOGIN_FORM_ENDPOINT)
        if self.response.url == login_url:
            return False
        return True

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=True,
    )


class Course(BaseModel):
    name: str
    location: str
    schedule: str

    model_config = ConfigDict(
        str_to_upper=True,
        str_strip_whitespace=True,
        extra="forbid",
        frozen=True,
        json_schema_extra={"example": ex_courses},
    )


class Activity(BaseModel):
    course: Course
    title: str
    delivery_date: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_to_upper=True,
        str_strip_whitespace=True,
        extra="forbid",
        frozen=True,
        json_schema_extra={"example": ex_activities},
    )


class AcademicIndexes(BaseModel):
    mc: float
    ira: float
    iech: float
    iepl: float
    iea: float
    caa: float

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=True,
    )


class Workload(BaseModel):
    mandatory: float
    optional: float
    total: float
    progress: float

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=True,
    )


class Profile(BaseModel):
    name: str
    photo: HttpUrl
    enrollment_id: int
    course_summary: str
    course_level: str
    course_status: str
    course_joined_at: date
    academic_indexes: AcademicIndexes
    workload: Workload

    model_config = ConfigDict(
        str_to_upper=True,
        str_strip_whitespace=True,
        extra="allow",
        frozen=True,
        json_schema_extra={"example": ex_profile},
    )
