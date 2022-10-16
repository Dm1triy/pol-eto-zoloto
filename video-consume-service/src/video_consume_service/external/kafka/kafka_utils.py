from loguru import logger

from kafka import KafkaConsumer

from ...settings import settings
from .kafka import kafka_client


def init_kafka_connection():
    logger.info("Start kafka connection")
    try:
        kafka_client.consumer = KafkaConsumer(
            *[settings.kafka_video_topic], bootstrap_servers=settings.kafka_bootstrap_servers
        )
    except Exception as exc:
        logger.error(exc)
        logger.warning("Fatal error was occured while kafka was starting")
        raise Exception


def close_kafka_connection():
    logger.info("Close kafka connection")
    if kafka_client.consumer:
        kafka_client.consumer.close()
