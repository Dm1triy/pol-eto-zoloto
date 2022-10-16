from confluent_kafka import Producer


class KafkaClient:
    producer: Producer | None


kafka_client = KafkaClient()


def get_client() -> KafkaClient:
    return kafka_client
