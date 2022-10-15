from kafka import KafkaConsumer


class KafkaClient:
    consumer: KafkaConsumer | None


kafka_client = KafkaClient()


def get_client() -> KafkaClient:
    return kafka_client
