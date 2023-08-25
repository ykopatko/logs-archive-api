from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.logs_repo import LogRepository
from services.logs_search_service import LogService
from utils.dependencies.get_session import get_session


def get_logs_service(
        session: AsyncSession = Depends(get_session)
) -> LogService:
    repo = LogRepository(session)
    service = LogService(log_repo=repo)

    return service
