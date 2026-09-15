from fastapi import APIRouter, File, UploadFile
from app.application.services.upload_model_service import upload_model_service


router = APIRouter()

@router.post("/upload/model")
async def upload_model(file: UploadFile=File()):
    return await upload_model_service(file)