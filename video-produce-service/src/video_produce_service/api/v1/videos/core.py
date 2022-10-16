from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

import cv2
from fastapi import File
from loguru import logger

from ....external.kafka.kafka import KafkaClient
from ....settings import settings
from .models import VideoMeta


def _save_upload_file_tmp(upload_file: File, ext: str = "jpg") -> tuple[Path, str]:
    filename = f"{uuid4()}.{ext}"
    suffix = Path(filename).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload_file)
        tmp_path = Path(tmp.name)
    return tmp_path, filename


def upload_video_kafka(file: File, kafka_client: KafkaClient):
    path, filename = _save_upload_file_tmp(file)
    video = cv2.VideoCapture(str(path))
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video_meta = VideoMeta(
        name=filename,
        frames=str(frames),
        fps=str(fps),
    )

    logger.info(f"Start publishing video {video_meta.name}")

    frame_no = 1
    while video.isOpened():
        success, frame = video.read()

        if not success:
            logger.error(f"Bad read {video_meta.name}")
            break
        if frame_no % 1 == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            kafka_client.producer.produce(
                topic=settings.kafka_video_topic,
                value=buffer.tobytes(),
                timestamp=frame_no,
                headers=video_meta.dict(),
            )
            kafka_client.producer.poll(0)
        frame_no += 1
    video.release()
    logger.info(f"End publishing video {video_meta.name}")
    return video_meta
