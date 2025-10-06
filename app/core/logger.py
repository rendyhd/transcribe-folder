from sqlalchemy.orm import Session
from app.models.log import LogEntry, LogLevel

def log_message(db: Session, message: str, level: LogLevel = LogLevel.INFO):
    """
    Logs a message to the database.
    """
    log_entry = LogEntry(message=message, level=level)
    db.add(log_entry)
    db.commit()