from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class MonitoredFolder(Base):
    __tablename__ = "monitored_folders"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)
    monitoring_enabled = Column(Boolean, default=True)