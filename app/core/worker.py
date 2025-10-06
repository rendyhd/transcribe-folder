import time
import threading
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.database import SessionLocal
from app.models.transcription import TranscriptionJob, TranscriptionStatus
from app.core.transcriber import transcribe_audio
from app.core.logger import log_message, LogLevel

def process_transcription_queue():
    while True:
        db: Session = SessionLocal()
        job_processed = False
        try:
            job = db.query(TranscriptionJob).filter(TranscriptionJob.status == TranscriptionStatus.QUEUED).first()
            if job:
                job_processed = True
                log_message(db, f"Starting transcription for job {job.id}: {job.file_path}")
                job.status = TranscriptionStatus.TRANSCRIBING
                db.commit()

                try:
                    transcribe_audio(job)
                    job.status = TranscriptionStatus.COMPLETE
                    job.date_completed = func.now()
                    log_message(db, f"Transcription completed for job {job.id}")
                except Exception as e:
                    if job.retry_count < 3:
                        job.retry_count += 1
                        job.status = TranscriptionStatus.QUEUED
                        log_message(db, f"Job {job.id} failed. Retrying ({job.retry_count}/3)...", LogLevel.WARNING)
                        time.sleep(5)  # Wait 5 seconds before retrying
                    else:
                        job.status = TranscriptionStatus.ERROR
                        job.error_message = str(e)
                        job.date_completed = func.now()
                        log_message(db, f"Job {job.id} failed after 3 retries: {e}", LogLevel.ERROR)

                db.commit()
        finally:
            db.close()

        # Sleep only if no job was found to avoid unnecessary delay
        if not job_processed:
            time.sleep(5)

def start_worker():
    worker_thread = threading.Thread(target=process_transcription_queue, daemon=True)
    worker_thread.start()