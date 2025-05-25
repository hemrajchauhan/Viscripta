## app/routers/merge.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
from app.services.pdf_service import merge_pdfs

router = APIRouter()

@router.post("/", summary="Merge PDFs")
async def merge_endpoint(
    files: List[UploadFile] = File(
        ..., 
        description="Select one or more PDF files", 
        media_type="application/pdf"
    )
):
    output = await merge_pdfs(files)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged.pdf"}
    )
