from fastapi import APIRouter
from app.core.config import settings
from app.schemas.settings import Settings, SettingsUpdate

router = APIRouter()

@router.get("/settings/", response_model=Settings)
def get_settings():
    return settings

@router.put("/settings/", response_model=Settings)
def update_settings(settings_update: SettingsUpdate):
    settings.whisper_model = settings_update.whisper_model
    return settings