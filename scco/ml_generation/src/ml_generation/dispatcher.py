import inspect
import json

from broker.broker import Broker

from util.reply import Reply

################################################################################

# Helpers


def get_callback_data(body: bytes):
    body = body.decode("utf-8")
    print_request_body(body)
    res = json.loads(body)
    return res


def publish_answer(
        answer,
        publisher_name: str,
        broker: Broker,
) -> None:
    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2, ensure_ascii=False)
    print(f"Answer:\n{answer}")

    print("sending answer")
    broker.basic_publish(
        publisher_name,
        answer.encode("utf-8"),
    )


def print_request_body(body) -> None:
    print(
        f"""
body of request:
-----------
{body}
----------"""
    )
