from kafka import KafkaProducer


class KafkaClient:
    producer: KafkaProducer | None


kafka_client = KafkaClient()


def get_client() -> KafkaClient:
    return kafka_client
