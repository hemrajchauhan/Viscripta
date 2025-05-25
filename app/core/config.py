## app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Viscripta API"
    DESCRIPTION: str = "PDF + OCR processing API"
    VERSION: str = "0.1.0"
    # Additional config (e.g., file limits, OCR models) can go here

settings = Settings()
