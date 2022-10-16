from confluent_kafka import Producer
from loguru import logger

from ...settings import settings
from .kafka import kafka_client


def init_kafka_connection():
    logger.info("Start kafka connection")
    try:
        kafka_client.producer = Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})
    except Exception as exc:
        logger.error(exc)
        logger.warning("Fatal error was occured while kafka was starting")
        raise Exception


def close_kafka_connection():
    logger.info("Close kafka connection")
    if kafka_client.producer:
        kafka_client.producer.flush()
