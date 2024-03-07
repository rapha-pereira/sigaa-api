from datetime import datetime, date
from typing import List, Literal, Union

from pydantic import BaseModel, HttpUrl, ConfigDict, validator
from selectolax.lexbor import LexborHTMLParser

from app.sigaa.examples import ex_courses, ex_activities, ex_profile
from app.core.exceptions import LoginFailed

import requests


class LoginModel(BaseModel):
    response: requests.Response

    def parse_response(self) -> LexborHTMLParser:
        """Method to parse the response to a LexborHTMLParser object."""
        return LexborHTMLParser(self.response.text)

    @validator("response")
    def check_login(cls, response: requests.Response) -> requests.Response:
        """Validate if the login was successful."""
        if not response.ok:
            raise LoginFailed()
        return response

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


class Activitie(BaseModel):
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


class Profile(BaseModel):
    name: str
    photo: HttpUrl
    student_id: int
    degree_description: str
    degree_type: str
    degree_status: str
    degree_started_at: date

    @validator("degree_started_at", pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            if value.endswith("1"):
                return date(year=value[0:4], month=1, day=1)
            if value.endswith("2"):
                return date(year=value[0:4], month=7, day=1)

    model_config = ConfigDict(
        str_to_upper=True,
        str_strip_whitespace=True,
        extra="forbid",
        frozen=True,
        json_schema_extra={"example": ex_profile},
    )


class SearchQuery(BaseModel):
    option: Literal["course", "profile_basic", "profile_additional", "all"] = "all"

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "success"
    data: Union[List[Course], List[Activitie], Profile, List, None]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=True,
    )
