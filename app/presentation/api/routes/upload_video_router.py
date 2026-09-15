from fastapi import APIRouter, File, UploadFile
from app.application.services.upload_video_service import upload_video_service

router = APIRouter()

@router.post("/upload/video")
async def upload_video(file: UploadFile=File()):
    return await upload_video_service(file)