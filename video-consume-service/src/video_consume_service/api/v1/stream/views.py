from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from .core import get_video_stream

stream_router = APIRouter(prefix="/api/v1/stream", tags=["stream"])


@stream_router.get(
    "/feed",
    name="videos:feed",
    status_code=status.HTTP_200_OK,
)
async def get_stream_feed():
    return StreamingResponse(
        get_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )
