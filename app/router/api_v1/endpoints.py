from fastapi import APIRouter

from app.sigaa import api as sigaa_api

api_router = APIRouter()

api_router.include_router(sigaa_api.router, prefix="/sigaa", tags=["SIGAA"])