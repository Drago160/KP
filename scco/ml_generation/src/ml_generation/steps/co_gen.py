import util.app_config as app_cfg

from ml_generation.dispatcher import get_callback_data
from ml_generation.dispatcher import publish_answer

from broker.broker import Broker
from broker.broker import Publisher
from broker.broker import Consumer

from ml_generation.ml_model import MlModel


class CoGen:
    # Publishers
    pdf_generation_pub = "pdf_gen_pub"

    def __init__(self, broker: Broker, ml_model: MlModel):
        self.broker = broker
        self.ml_model = ml_model

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.CO_GEN_EXCHANGE,
                queue=app_cfg.CO_GEN_QUEUE,
                routing_key=app_cfg.CO_GEN_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=CoGen.pdf_generation_pub,
                exchange=app_cfg.PDF_GENERATION_EXCHANGE,
                queue=app_cfg.PDF_GENERATION_QUEUE,
                routing_key=app_cfg.PDF_GENERATION_ROUTING_KEY,
            )
        )

    def callback(self, ch, method, props, body):
        print("CoGen callback started")
        passed_data = get_callback_data(body)

        answer = self.callback_handle(passed_data)

        publish_answer(answer, self.pdf_generation_pub, self.broker)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("CoGen callback finished")

    def callback_handle(self, passed_data) -> dict:
        message_group_id = passed_data["reply_ctx"]

        # Run model.
        print("Running ml_model.generate()...")
        gen_data = self.ml_model.generate(passed_data)
        print(f"ml_model.generate() finished, gen_data:\n{gen_data}")

        answer = {
            "message_group_id": message_group_id,
            "main_text": gen_data["main_text"],
            "contact_info": passed_data["contact_info"],
        }

        return answer
