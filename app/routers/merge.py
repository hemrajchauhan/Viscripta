## app/routers/merge.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from app.services.pdf_service import merge_pdfs

router = APIRouter()

@router.post("/")
async def merge_endpoint(files: list[UploadFile] = File(...)):
    output = await merge_pdfs(files)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged.pdf"}
    )
