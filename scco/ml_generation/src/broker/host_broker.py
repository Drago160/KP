from broker.broker import Broker
from broker.broker import Publisher
from broker.broker import Consumer


class HostBroker(Broker):
    ############################################################################
    # API

    def __init__(self) -> None:
        pass

    def add_publisher(self, publisher: Publisher):
        pass

    def add_consumer(self, consumer: Consumer):
        pass

    def start_consuming(self):
        pass

    def basic_publish(self, publisher_name: str, body: bytes):
        pass

    def basic_publish_unknown(
            self,
            pub: Publisher,
            body: bytes
    ) -> None:
        pass

    ############################################################################
    # Internals
