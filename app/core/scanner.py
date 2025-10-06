import os
from sqlalchemy.orm import Session
from app.models.folder import MonitoredFolder
from app.models.transcription import TranscriptionJob
from app.core.logger import log_message

SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac"}

def scan_folders(db: Session):
    log_message(db, "Starting folder scan...")
    monitored_folders = db.query(MonitoredFolder).filter(MonitoredFolder.monitoring_enabled == True).all()
    new_files_found = 0
    for folder in monitored_folders:
        for root, _, files in os.walk(folder.path):
            for file in files:
                if any(file.endswith(ext) for ext in SUPPORTED_FORMATS):
                    file_path = os.path.join(root, file)
                    existing_job = db.query(TranscriptionJob).filter(TranscriptionJob.file_path == file_path).first()
                    if not existing_job:
                        new_job = TranscriptionJob(
                            file_name=os.path.basename(file_path),
                            file_path=file_path,
                        )
                        db.add(new_job)
                        new_files_found += 1
    if new_files_found > 0:
        log_message(db, f"Found {new_files_found} new audio files.")
    else:
        log_message(db, "No new audio files found.")
    db.commit()
    log_message(db, "Folder scan complete.")