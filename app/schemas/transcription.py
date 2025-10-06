from pydantic import BaseModel
from datetime import datetime
from app.models.transcription import TranscriptionStatus

class TranscriptionJobBase(BaseModel):
    file_name: str
    file_path: str
    status: TranscriptionStatus

class TranscriptionJob(TranscriptionJobBase):
    id: int
    date_added: datetime
    date_completed: datetime | None = None
    error_message: str | None = None

    class Config:
        from_attributes = True