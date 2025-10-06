from pydantic import BaseModel

class Settings(BaseModel):
    whisper_model: str

class SettingsUpdate(BaseModel):
    whisper_model: str