## app/routers/extract_table.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.ocr_service import extract_table

router = APIRouter()

@router.post("/")
async def table_endpoint(file: UploadFile = File(...)):
    result = await extract_table(file)
    return JSONResponse(content=result)
