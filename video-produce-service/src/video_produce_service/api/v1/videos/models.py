from uuid import UUID, uuid4

from pydantic import BaseModel


class VideoMeta(BaseModel):
    id: str = str(uuid4())
    name: str
    content_type: str
    frames: int
    fps: int
