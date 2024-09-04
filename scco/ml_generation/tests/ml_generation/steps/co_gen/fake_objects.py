import inspect
import json

import util.app_config as app_cfg

from broker.broker import Broker
from broker.broker import Publisher
from broker.broker import Consumer

from ml_generation.steps.co_gen import CoGen

from ml_generation.ml_model import MlModel


class CoGenTestMlModel(MlModel):
    def generate(self, data):
        gen_data = {
            "main_text": "some_useful_text"
        }
        return gen_data


class CoGenTestMethod:
    delivery_tag = "delivery_tag"


class CoGenTestChannel:
    def basic_ack(self, delivery_tag):
        assert delivery_tag == CoGenTestMethod.delivery_tag


class CoGenTestBroker(Broker):
    ############################################################################
    # API

    def __init__(self, publish_out: dict) -> None:
        self._publish_out = publish_out
        self.pubs: dict[str, Publisher] = {}

    def add_publisher(self, publisher: Publisher):
        self.pubs[publisher.name] = publisher

        assert publisher.name == CoGen.pdf_generation_pub
        assert publisher.exchange == app_cfg.PDF_GENERATION_EXCHANGE
        assert publisher.queue == app_cfg.PDF_GENERATION_QUEUE
        assert publisher.routing_key == app_cfg.PDF_GENERATION_ROUTING_KEY

    def add_consumer(self, consumer: Consumer):
        assert consumer.exchange == app_cfg.CO_GEN_EXCHANGE
        assert consumer.queue == app_cfg.CO_GEN_QUEUE
        assert consumer.routing_key == app_cfg.CO_GEN_ROUTING_KEY
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
        print(f"type(recv_data) = {type(recv_data)}")
        print(f"type(self._publish_out) = {type(self._publish_out)}")
        assert recv_data["main_text"] == self._publish_out["main_text"]
        assert recv_data["message_group_id"] == self._publish_out["message_group_id"]
        # assert recv_data == self._publish_out

    def basic_publish_unknown(
            self,
            pub: Publisher,
            body: bytes
    ) -> None:
        pass

    ############################################################################
    # Internals
