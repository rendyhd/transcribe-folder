from pydantic import BaseModel
from datetime import datetime
from app.models.log import LogLevel

class LogEntryBase(BaseModel):
    message: str
    level: LogLevel

class LogEntry(LogEntryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True