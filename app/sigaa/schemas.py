from datetime import datetime
from typing import List, Literal, Union
from pydantic import BaseModel, HttpUrl, ConfigDict
from app.sigaa.examples import ex_courses, ex_activities, ex_profile


class Courses(BaseModel):
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


class Activities(BaseModel):
    course: Courses
    title: str
    delivery_date: datetime

    model_config = ConfigDict(
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
    option: Literal["courses", "activities", "profile", "all"] = "all"


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "success"
    data: Union[List[Courses], List[Activities], Profile, None] = None
