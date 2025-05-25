### app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.routers import merge, ocr, extract_table

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

app.include_router(merge.router, prefix="/merge", tags=["PDF"])
app.include_router(ocr.router, prefix="/ocr", tags=["OCR"])
app.include_router(extract_table.router, prefix="/extract-table", tags=["Tables"])
