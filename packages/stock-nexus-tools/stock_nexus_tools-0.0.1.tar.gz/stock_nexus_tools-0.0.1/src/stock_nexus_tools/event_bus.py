from typing import Any
import pika
import json
from pika.adapters.blocking_connection import BlockingChannel


class EventBus:
    def __init__(self, uri: str) -> None:
        parameters = pika.URLParameters(uri)
        self.connection = pika.BlockingConnection(parameters)
        self.channel: BlockingChannel = self.connection.channel()

    def publish(self, queue_name: str, event: dict[str, Any]) -> None:
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(event)
        )

    def consume(self, queue_name: str, callback) -> None:
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

    def start_consuming(self) -> None:
        self.channel.start_consuming()
