from fastapi import APIRouter, Depends, UploadFile, status

from ....external.kafka.kafka import get_client
from .core import upload_video_kafka
from .models import VideoMeta

videos_router = APIRouter(prefix="/api/v1/videos", tags=["videos"])


@videos_router.post(
    "/upload",
    name="videos:upload",
    status_code=status.HTTP_200_OK,
    response_model=VideoMeta,
)
async def upload_video(file: UploadFile, producer=Depends(get_client)):
    meta = upload_video_kafka(file, producer)

    return meta
