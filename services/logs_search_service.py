from datetime import datetime
from models.logs import Log
from repositories.logs_repo import LogRepository

from fastapi import UploadFile, File
from sqlalchemy import select, func, and_

from utils.dependencies.extract_zip import extract_zip


class LogService:

    def __init__(self, log_repo: LogRepository):
        self.repo = log_repo

    async def get_all_logs(
            self,
            start_datetime: datetime | None = None,
            end_datetime: datetime | None = None,
            content: str | None = None,
    ):
        query = (
            select(Log)
        )
        filters = []

        if start_datetime and end_datetime:
            filters.append(Log.timestamp.between(start_datetime, end_datetime))

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

        for log_content in logs:
            log = Log(content=log_content)

            self.repo.session.add(log)

        await self.repo.session.commit()

        return logs

    @staticmethod
    async def _handle_zip(file: UploadFile = File(...)):
        return await extract_zip(file)

    @staticmethod
    async def _handle_txt(file: UploadFile = File(...)):
        content = await file.read()
        logs = content.decode().splitlines()
        return logs
