from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.folder import MonitoredFolder
from app.schemas.folder import Folder, FolderCreate, FolderUpdate
from app.core.scanner import scan_folders
from app.core.logger import log_message

router = APIRouter()

@router.post("/folders/", response_model=Folder)
def add_monitored_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    db_folder = db.query(MonitoredFolder).filter(MonitoredFolder.path == folder.path).first()
    if db_folder:
        raise HTTPException(status_code=400, detail="Folder already monitored")
    new_folder = MonitoredFolder(path=folder.path)
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    log_message(db, f"Added new monitored folder: {folder.path}")
    return new_folder

@router.get("/folders/", response_model=List[Folder])
def list_monitored_folders(db: Session = Depends(get_db)):
    return db.query(MonitoredFolder).all()

@router.put("/folders/{folder_id}", response_model=Folder)
def update_monitored_folder(folder_id: int, folder_update: FolderUpdate, db: Session = Depends(get_db)):
    db_folder = db.query(MonitoredFolder).filter(MonitoredFolder.id == folder_id).first()
    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    db_folder.monitoring_enabled = folder_update.monitoring_enabled
    db.commit()
    db.refresh(db_folder)
    log_message(db, f"Updated monitoring status for folder {db_folder.path} to {db_folder.monitoring_enabled}")
    return db_folder

@router.post("/scan/")
def trigger_scan(db: Session = Depends(get_db)):
    log_message(db, "Manual scan triggered by user.")
    scan_folders(db)
    return {"message": "Scan completed"}