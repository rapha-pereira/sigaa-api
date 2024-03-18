from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sigaa_api.core.exceptions import LoginFailed
from sigaa_api.sigaa.portal import StudentPortal
from sigaa_api.sigaa.models import Course, Profile, Activity

router = APIRouter(prefix="/student")
security = HTTPBasic()


@router.get("/courses", response_model=List[Course])
async def courses(credentials: HTTPBasicCredentials = Depends(security)):
    portal = login(credentials, "courses")
    return portal.handle()


@router.get("/profiles", response_model=Profile)
async def profile(credentials: HTTPBasicCredentials = Depends(security)):
    portal = login(credentials, "profile")
    return portal.handle()


@router.get("/activities", response_model=List[Activity])
async def activities(credentials: HTTPBasicCredentials = Depends(security)):
    portal = login(credentials, "activities")
    return portal.handle()


def login(credentials: HTTPBasicCredentials, option: str) -> StudentPortal:
    portal = StudentPortal(credentials=credentials, option=option)
    portal.login()
    if not portal.sigaa_login.ok():
        exception = LoginFailed()
        raise HTTPException(status_code=exception.status_code, detail=exception.message)
    return portal
