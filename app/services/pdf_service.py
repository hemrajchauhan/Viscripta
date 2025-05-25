## app/services/pdf_service.py

import io
from pypdf import PdfMerger
from fastapi import UploadFile

async def merge_pdfs(files: list[UploadFile]) -> io.BytesIO:
    merger = PdfMerger()
    for file in files:
        merger.append(file.file)
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)
    return output
