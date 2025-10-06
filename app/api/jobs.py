from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transcription import TranscriptionJob
from app.schemas.transcription import TranscriptionJob as TranscriptionJobSchema

router = APIRouter()

@router.get("/jobs/", response_model=List[TranscriptionJobSchema])
def list_transcription_jobs(db: Session = Depends(get_db)):
    return db.query(TranscriptionJob).all()