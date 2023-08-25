from datetime import datetime

from models.logs import Log
from repositories.logs_repo import LogRepository

from sqlalchemy import select, func, and_


class LogService:

    def __init__(self, log_repo: LogRepository):
        self.repo = log_repo

    async def get_all_logs(
            self,
            start_date: datetime | None = None,
            end_date: datetime | None = None,
            content: str | None = None,
    ):
        query = (
            select(Log)
        )
        filters = []

        if start_date and end_date:
            filters.append(Log.timestamp.between(start_date, end_date))

        if content:
            filters.append(func.lower(Log.content).ilike(f"%{content.lower()}%"))

        if filters:
            query = query.where(and_(*filters))

        logs = await self.repo.get_all(query)

        return logs

    async def get_log_by_id(
            self,
            log_id: int,
    ):
        query = select(Log).where(Log.id == log_id)

        log = await self.repo.get_one_obj(query)

        return log
