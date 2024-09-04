import inspect
import json

import util.app_config as app_cfg

from broker.broker import Broker
from broker.broker import Publisher
from broker.broker import Consumer

from ml_generation.steps.preproc import Preproc


class PreprocTestMethod:
    delivery_tag = "delivery_tag"


class PreprocTestChannel:
    def basic_ack(self, delivery_tag):
        assert delivery_tag == PreprocTestMethod.delivery_tag


class PreprocTestBroker(Broker):
    ############################################################################
    # API

    def __init__(self, publish_out: dict) -> None:
        self._publish_out = publish_out
        self.pubs: dict[str, Publisher] = {}

    def add_publisher(self, publisher: Publisher):
        self.pubs[publisher.name] = publisher

        assert publisher.name == Preproc.db_functional_service_pub
        assert publisher.exchange == app_cfg.DB_FUNCTIONAL_SERVICE_EXCHANGE
        assert publisher.queue == app_cfg.DB_FUNCTIONAL_SERVICE_QUEUE
        assert publisher.routing_key == \
               app_cfg.DB_FUNCTIONAL_SERVICE_ROUTING_KEY

    def add_consumer(self, consumer: Consumer):
        assert consumer.exchange == app_cfg.ML_GENERATION_EXCHANGE
        assert consumer.queue == app_cfg.ML_GENERATION_QUEUE
        assert consumer.routing_key == app_cfg.ML_GENERATION_ROUTING_KEY
        # assert consumer.callback == Preproc.callback

    def start_consuming(self):
        raise NotImplemented()

    def basic_publish(self, publisher_name: str, body: bytes):
        assert publisher_name in self.pubs, inspect.cleandoc(
            f"""invalid publisher name
            provided name: {publisher_name}
            accessible names: {self.pubs.keys()}"""
        )

        recv_data = json.loads(body.decode("utf-8"))
        assert type(recv_data) is dict
        assert recv_data == self._publish_out

    def basic_publish_unknown(
            self,
            pub: Publisher,
            body: bytes
    ) -> None:
        pass

    ############################################################################
    # Internals
