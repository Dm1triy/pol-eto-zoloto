import json
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

import cv2
from fastapi import UploadFile
from loguru import logger

from ....external.kafka.kafka import KafkaClient
from ....settings import settings
from .models import VideoMeta


def _save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def upload_video_kafka(file: UploadFile, kafka_client: KafkaClient):
    path = _save_upload_file_tmp(file)
    video = cv2.VideoCapture(str(path))
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video_meta = VideoMeta(
        name=file.filename,
        content_type=file.content_type,
        frames=frames,
        fps=fps,
    )

    kafka_client.producer.send(
        settings.kafka_video_topic, json.dumps(video_meta.dict()).encode("utf-8")
    )

    logger.info(f"Start publishing video {video_meta.name}")

    while video.isOpened():
        success, frame = video.read()

        if not success:
            logger.error(f"Bad read {video_meta.name}")
            break

        _, buffer = cv2.imencode(".jpg", frame)

        kafka_client.producer.send(settings.kafka_video_topic, buffer.tobytes())

    video.release()
    logger.info(f"End publishing video {video_meta.name}")
    return video_meta
