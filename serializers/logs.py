from datetime import datetime

from pydantic import BaseModel


class LogBase(BaseModel):
    content: str
    timestamp: datetime


class LogCreate(LogBase):
    pass


class LogList(LogBase):
    id: int

    class Config:
        from_attributes = True
