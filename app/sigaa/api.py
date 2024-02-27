from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.sigaa.core import StudentPortal
from app.sigaa.schemas import SearchQuery, SearchResponse

router = APIRouter()
security = HTTPBasic()


@router.post(path="/student/", response_model=SearchResponse)
def student(data: SearchQuery, credentials: HTTPBasicCredentials = Depends(security)):
    portal_data = StudentPortal(credentials=credentials, option='course').handle() #FIXME: data.option
    status, message = (True, "success") if data else (False, "failed to retrieve data")

    return SearchResponse(status=status, message=message, data=portal_data)
