import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db.database import Base

class LogLevel(enum.Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    level = Column(Enum(LogLevel), default=LogLevel.INFO)
    message = Column(String)