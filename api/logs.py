from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi import UploadFile, File
from starlette import status

from api.users import fastapi_users
from models import User
from serializers.logs import LogList
from services.logs_upload_and_search_service import LogService
from utils.dependencies.services import get_logs_service

router = APIRouter()


@router.get("", response_model=list[LogList])
async def get_logs(
    content: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    user: User = Depends(fastapi_users.current_user(optional=False)),
    service: LogService = Depends(get_logs_service)
):
    result = await service.get_all_logs(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        content=content,
    )

    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no logs with such details"
        )

    return result


@router.get("/{log_id}", response_model=LogList)
async def get_logs_by_id(
        log_id: int,
        user: User = Depends(fastapi_users.current_user(optional=False)),
        service: LogService = Depends(get_logs_service)
):
    log = await service.get_log_by_id(log_id)

    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The log has been not found"
        )

    return log


@router.post("/upload")
async def upload_log(
    file: UploadFile = File(...),
    user: User = Depends(fastapi_users.current_user(optional=False)),
    service: LogService = Depends(get_logs_service)
):
    logs = await service.process_uploaded_log(file)
    if logs:
        return {"status": "success", "message": "Logs processed successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to process the logs.")
