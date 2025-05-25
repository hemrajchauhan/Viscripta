## app/services/pdf_service.py

import io
from pypdf import PdfReader, PdfWriter
from fastapi import UploadFile

async def merge_pdfs(files: list[UploadFile]) -> io.BytesIO:
    writer = PdfWriter()
    for file in files:
        reader = PdfReader(file.file)
        for page in reader.pages:
            writer.add_page(page)
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output
