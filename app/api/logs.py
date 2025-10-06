from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.log import LogEntry
from app.schemas.log import LogEntry as LogEntrySchema

router = APIRouter()

@router.get("/logs/", response_model=List[LogEntrySchema])
def list_logs(db: Session = Depends(get_db)):
    return db.query(LogEntry).order_by(LogEntry.timestamp.desc()).all()