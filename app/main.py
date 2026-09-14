from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.presentation.api.routes.upload_video import router as upload_video_router
from app.presentation.api.routes.upload_model import router as upload_model_router

from config import *


app = FastAPI(title="Head Swapper")

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

app.include_router(upload_video_router)
app.include_router(upload_model_router)