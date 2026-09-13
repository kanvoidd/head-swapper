from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Head Swapper")

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent  # Указывает на корень проекта

FRONTEND_DIR = BASE_DIR / "frontend"
STORAGE_DIR = BASE_DIR / "storage"

UPLOADS_DIR = STORAGE_DIR / "uploads"
PROCESSING_DIR = STORAGE_DIR / "processing"
RESULTS_DIR = STORAGE_DIR / "results"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Static files
# --------------------------------------------------

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)

# --------------------------------------------------
# Main page
# --------------------------------------------------

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")

# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# --------------------------------------------------
# Video upload
# --------------------------------------------------

@app.post("/upload/video")
async def upload_video(file: UploadFile = File()):

    file_extension = Path(file.filename).suffix.lower()

    allowed_extensions = {
        ".mp4",
        ".mov",
        ".avi",
    }

    if file_extension not in allowed_extensions:
        return {
            "success": False,
            "error": "Upsupported video format"
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

# --------------------------------------------------
# 3D model upload
# --------------------------------------------------

@app.post("/upload/model")
async def upload_model(file: UploadFile=File()):

    file_extension = Path(file.filename).suffix.lower()

    allowed_extensions = {
        ".glb",
        ".gltf",
        ".obj",
        ".fbx"
    }

    if file_extension not in allowed_extensions:
        return {
            "success": False,
            "error": "Unsupported model extension"
        }

    file_id = str(uuid4())

    filename = f"{file_id}{file_extension}"
    destination = UPLOADS_DIR / filename

    contents = await file.read()
    destination.write_bytes(contents)

    return {
        "success": True,
        "file_id": file_id,
        "original_filename": file.filename,
        "saved_filename": filename,
    }