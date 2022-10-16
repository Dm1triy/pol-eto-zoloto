from pydantic import BaseModel


class VideoMeta(BaseModel):
    name: str
    content_type: str
