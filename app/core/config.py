import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    local_whisper_server_ip: str = "127.0.0.1"
    local_whisper_server_port: int = 9000
    whisper_model: str = "base"

    class Config:
        env_file = ".env"

settings = Settings()