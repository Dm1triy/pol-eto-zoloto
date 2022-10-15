import json
from datetime import datetime

from loguru import logger

from ....external.kafka.kafka import kafka_client


def get_video_stream():
    for msg in kafka_client.consumer:
        try:
            data = json.loads(msg.value)
            logger.info(data)
        except UnicodeDecodeError:
            yield (b"--frame\r\n" b"Content-Type: image/jpg\r\n\r\n" + msg.value + b"\r\n\r\n")
