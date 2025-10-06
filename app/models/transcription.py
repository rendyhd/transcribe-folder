import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db.database import Base

class TranscriptionStatus(enum.Enum):
    QUEUED = "Queued"
    TRANSCRIBING = "Transcribing"
    COMPLETE = "Complete"
    ERROR = "Error"

class TranscriptionJob(Base):
    __tablename__ = "transcription_jobs"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    file_path = Column(String, unique=True, index=True)
    status = Column(Enum(TranscriptionStatus), default=TranscriptionStatus.QUEUED)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_completed = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)