from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.sigaa.core import StudentPortal
from app.sigaa.schemas import SearchQuery, SearchResponse

router = APIRouter()
security = HTTPBasic()


@router.post(path="/student/", response_model=SearchResponse)
def student(data: SearchQuery, credentials: HTTPBasicCredentials = Depends(security)):
    try:
        portal_data = StudentPortal(
            credentials=credentials, option=data.option
        ).handle()
    except Exception as e:
        raise e
    status, message = (
        (True, "success") if portal_data else (False, "failed to retrieve data")
    )

    return SearchResponse(status=status, message=message, data=portal_data)
