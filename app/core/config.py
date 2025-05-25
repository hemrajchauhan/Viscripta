## app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Viscripta API"
    DESCRIPTION: str = "PDF + OCR processing API"
    VERSION: str = "0.1.0"

settings = Settings()
