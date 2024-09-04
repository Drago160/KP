import util.app_config as app_cfg

from ml_generation.dispatcher import get_callback_data
from ml_generation.dispatcher import publish_answer

from broker.broker import Broker
from broker.broker import Publisher
from broker.broker import Consumer


class Preproc:
    # Publishers.
    db_functional_service_pub = "db_service_pub"

    def __init__(self, broker: Broker):
        self.broker = broker

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.ML_GENERATION_EXCHANGE,
                queue=app_cfg.ML_GENERATION_QUEUE,
                routing_key=app_cfg.ML_GENERATION_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=self.db_functional_service_pub,
                exchange=app_cfg.DB_FUNCTIONAL_SERVICE_EXCHANGE,
                queue=app_cfg.DB_FUNCTIONAL_SERVICE_QUEUE,
                routing_key=app_cfg.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            )
        )

    def callback(self, ch, method, props, body):
        print("Preproc callback started")
        passed_data = get_callback_data(body)

        answer = self.callback_handle(passed_data)

        publish_answer(answer, self.db_functional_service_pub, self.broker)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Preproc callback finished")

    def callback_handle(self, passed_data) -> dict:
        message_group_id = passed_data["message_group_id"]

        answer = {
            "request_name": "get_info_for_co_generation",
            "reply": {
                "exchange": app_cfg.CO_GEN_EXCHANGE,
                "routing_key": app_cfg.CO_GEN_ROUTING_KEY,
            },
            "reply_ctx": message_group_id,  # not required
            "request_data": {
                "message_group_id": message_group_id,
            }
        }

        return answer
