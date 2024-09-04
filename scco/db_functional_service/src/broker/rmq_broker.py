import inspect

import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from broker.broker import Broker
from broker.broker import Publisher
from broker.broker import Consumer

import util.app_config as app_cfg


class RmqBroker(Broker):
    ############################################################################
    # API

    def __init__(self) -> None:
        self.chan = self.__class__._create_channel()
        self.pubs: dict[str, Publisher] = {}

    def add_publisher(self, publisher: Publisher):
        self.pubs[publisher.name] = publisher
        self.chan.exchange_declare(
            exchange=publisher.exchange,
            exchange_type='topic',
            durable=True,
        )
        self.chan.queue_declare(
            queue=publisher.queue,
            durable=True,
        )
        self.chan.queue_bind(
            exchange=publisher.exchange,
            queue=publisher.queue,
            routing_key=publisher.routing_key,
        )

    def add_consumer(self, consumer: Consumer):
        self.chan.exchange_declare(
            exchange=consumer.exchange,
            exchange_type='topic',
            durable=True,
        )
        q = self.chan.queue_declare(
            queue=consumer.queue,
            durable=True,
        )
        q_name = q.method.queue  # if consumer.queue == "" - auto generate queue
        consumer.queue = q_name
        self.chan.queue_bind(
            exchange=consumer.exchange,
            queue=consumer.queue,
            routing_key=consumer.routing_key,
        )
        self.chan.basic_consume(
            queue=consumer.queue,
            on_message_callback=consumer.callback,
        )

    def start_consuming(self):
        self.chan.start_consuming()  # Infinite loop.

    def basic_publish(self, publisher_name: str, body: bytes):
        if publisher_name not in self.pubs:
            RuntimeError(
                inspect.cleandoc(
                    f"""invalid publisher name
                    provided name: {publisher_name}
                    accessible names: {self.pubs.keys()}"""
                )
            )

        pub = self.pubs[publisher_name]
        self.chan.basic_publish(
            exchange=pub.exchange,
            routing_key=pub.routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

    def basic_publish_unknown(
            self,
            pub: Publisher,
            body: bytes
    ) -> None:
        self.chan.basic_publish(
            exchange=pub.exchange,
            routing_key=pub.routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

    ############################################################################
    # Internals

    @classmethod
    def _create_channel(cls) -> BlockingChannel:
        chan = cls._conn.channel()
        return chan

    # Class fields (Lazy initialization on host)
    _conn: BlockingConnection = pika.BlockingConnection(
        pika.ConnectionParameters(host=app_cfg.RMQ_NET_ALIAS)
    )
