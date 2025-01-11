import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_images(file: UploadFile, background_task: BackgroundTasks):
    ImagesService().upload_images(file, background_task)
    return {"status": "OK"}
