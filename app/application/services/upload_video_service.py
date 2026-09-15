from fastapi import UploadFile

from uuid import uuid4
from config import *

async def upload_video_service(file: UploadFile):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_VIDEO_EXTENSIONS:
        return {
            "success": False,
            "error": "Upsupported video format"
        }

    filesize_mb = file.size / BYTES_IN_MB

    if filesize_mb > MAX_VIDEO_SIZE_MB:
        return {
            "success": False,
            "error": "File size is too big"
        }

    file_id = str(uuid4())

    filename = f"{file_id}{file_extension}"
    destination = UPLOADS_DIR / filename

    contents = await file.read() # временное решение чтоб не усложнять код
    destination.write_bytes(contents)

    return {
        "success": True,
        "file_id": file_id,
        "original_filename": file.filename,
        "saved_filename": filename,
    }