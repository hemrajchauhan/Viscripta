## app/utils/image_utils.py

import tempfile
from fastapi import UploadFile


def save_upload_to_temp(file: UploadFile) -> str:
    suffix = ".jpg" if file.filename.lower().endswith(('.jpg','.jpeg')) else ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = file.file.read()
        tmp.write(contents)
        return tmp.name