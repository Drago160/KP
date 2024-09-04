from typing import Callable

from abc import ABC
from abc import abstractmethod


# TODO: add on_reply
class Publisher:
    def __init__(
            self,
            name: str,
            exchange: str,
            queue: str,
            routing_key: str,
    ):
        self.name = name
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key


class Consumer:
    def __init__(
            self,
            exchange: str,
            queue: str,
            routing_key: str,
            callback: Callable,
    ):
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.callback = callback


class Broker(ABC):
    @abstractmethod
    def add_publisher(self, publisher: Publisher):
        raise NotImplementedError("Pure virtual method")

    @abstractmethod
    def add_consumer(self, consumer: Consumer):
        raise NotImplementedError("Pure virtual method")

    @abstractmethod
    def start_consuming(self):
        raise NotImplementedError("Pure virtual method")

    @abstractmethod
    def basic_publish(self, publisher_name: str, body: bytes):
        raise NotImplementedError("Pure virtual method")

    @abstractmethod
    def basic_publish_unknown(
            self,
            pub: Publisher,
            body: bytes
    ) -> None:
        raise NotImplementedError("Pure virtual method")

