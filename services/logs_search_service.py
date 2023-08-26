from datetime import datetime
from models.logs import Log
from repositories.logs_repo import LogRepository

from fastapi import UploadFile, File
from sqlalchemy import select, func, and_

from utils.dependencies.services import extract_zip


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

    async def process_uploaded_log(self, file: UploadFile = File(...)):
        if file.filename.endswith(".zip"):
            # Can be extended to handle other archive types like '.tar.gz', etc.
            logs = await self._handle_zip(file)
        elif file.filename.endswith(".txt"):
            logs = await self._handle_txt(file)
        else:
            return None

        # Store logs (This is an example; you'd likely want to parse and structure the logs better)
        for log_content in logs:
            log = Log(content=log_content)
            # Store the log in the database
        return logs

    async def _handle_zip(self, file: UploadFile = File(...)):
        return await extract_zip(file)

    async def _handle_txt(self, file: UploadFile = File(...)):
        content = await file.read()
        logs = content.decode().splitlines()
        return logs
