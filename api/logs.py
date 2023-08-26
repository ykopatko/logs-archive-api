from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from api.users import fastapi_users
from models import User
from serializers.logs import LogList, LogBase
from services.logs_search_service import LogService
from utils.dependencies.services import get_logs_service

router = APIRouter()


@router.get("", response_model=list[LogList])
async def get_logs(
    content: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    user: User = Depends(fastapi_users.current_user(optional=False)),
    service: LogService = Depends(get_logs_service)
):
    result = await service.get_all_logs(
        start_date=start_date,
        end_date=end_date,
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
