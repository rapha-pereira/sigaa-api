from datetime import datetime
from typing import List, Literal, Union

from pydantic import BaseModel, HttpUrl, ConfigDict, validator
from selectolax.lexbor import LexborHTMLParser

from app.sigaa.examples import ex_courses, ex_activities, ex_profile
from app.core.exceptions import LoginFailed

import requests


class SIGAALogin(BaseModel):
    response: requests.Response

    def parse_response(self) -> LexborHTMLParser:
        """Method to parse the response to a LexborHTMLParser object."""
        return LexborHTMLParser(self.response.text)

    @validator("response")
    def check_login(cls, response: requests.Response) -> requests.Response:
        """Validate if the login was successful."""
        if "Usuário ou senha inválidos" in response.text:
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
    email: str
    photo: HttpUrl

    model_config = ConfigDict(
        str_to_upper=True,
        str_strip_whitespace=True,
        extra="forbid",
        frozen=True,
        json_schema_extra={"example": ex_profile},
    )


class SearchQuery(BaseModel):
    option: Literal["course", "activitie", "profile", "all"] = "all"

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "success"
    data: Union[List[Course], List[Activitie], Profile, None] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=True,
    )
