import inspect
import json

from util.app_errors import dict_get_or_panic
from util.app_errors import runtime_error_wrapper

from util.reply import Reply
from util.reply import add_reply_ctx

from broker.broker import Broker
from broker.broker import Consumer

import util.app_config as app_cfg

################################################################################

# Callbacks

# data_preproc
from service.request_cb.data_preproc.filter_new_queries import FilterNewQueries
from service.request_cb.data_preproc.get_customers_lists import (
    GetCustomersLists,
)
from service.request_cb.data_preproc.insert_new_queries_csv import (
    InsertNewQueriesCsv,
)
from service.request_cb.data_preproc.insert_preprocessed_queries import (
    InsertPreprocessedQueries,
)

# ml_co_gen
from service.request_cb.ml_co_gen.get_info_for_co_generation import (
    GetInfoForCoGeneration,
)

# pdf_co_gen
from service.request_cb.pdf_co_gen.insert_offers import InsertOffers

# customer_creator
from service.request_cb.customer_creator.insert_customer import InsertCustomer

# manual
from service.request_cb.manual.map_offers_to_messages import MapOffersToMessages

################################################################################


class Dispatcher:
    def __init__(self, broker: Broker):
        self.broker = broker

        # Publishers.
        # ...

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.DB_FUNCTIONAL_SERVICE_EXCHANGE,
                queue=app_cfg.DB_FUNCTIONAL_SERVICE_QUEUE,
                routing_key=app_cfg.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
                callback=self.callback,
            )
        )

        self.callback_map = {
            # data_preproc
            "filter_new_queries": FilterNewQueries(),
            "insert_new_queries_csv": InsertNewQueriesCsv(),
            "get_customers_lists": GetCustomersLists(),
            "insert_preprocessed_queries": InsertPreprocessedQueries(),

            # ml_co_gen
            "get_info_for_co_generation": GetInfoForCoGeneration(),

            # pdf_co_gen
            "insert_offers": InsertOffers(),

            # customer_creator
            "insert_customer": InsertCustomer(),

            # manual
            "map_offers_to_messages": MapOffersToMessages(),
        }

    def callback(self, ch, method, props, body):
        print("Dispatcher callback started")

        # Get data from body.
        body = body.decode("utf-8")
        print_request_body(body)
        srv_req_data = json.loads(body)

        self.dispatch_function(srv_req_data)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def dispatch_function(self, srv_req_data):
        print("dispatch_function")
        req_data, reply, request_name = extract_basic_data(srv_req_data)

        if request_name not in self.callback_map:
            print("Dispatcher callback finished")
            raise RuntimeError(f"Unknown request_name: '{request_name}'")

        cb = self.callback_map.get(request_name)
        answer = cb.make_call(req_data, srv_req_data)

        if reply.is_required() and answer is None:
            handle_reply_not_generated(request_name, req_data, srv_req_data)

        if reply.is_required():
            publish_answer(answer, srv_req_data, reply, self.broker)
        else:
            print("Publish is not required, skipping")

################################################################################

# Helpers


def extract_basic_data(srv_req_data):
    req_data = dict_get_or_panic(srv_req_data, "request_data")
    reply = Reply(srv_req_data)
    query_name = dict_get_or_panic(srv_req_data, "request_name")
    return req_data, reply, query_name


def publish_answer(
        answer,
        srv_req_data,
        reply: Reply,
        broker: Broker,
) -> None:
    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2, ensure_ascii=False)
    print(f"Answer:\n{answer}")

    print("sending reply")
    broker.basic_publish_unknown(
        reply.get_publisher(),
        answer.encode("utf-8"),
    )


def handle_reply_not_generated(
        request_name: str,
        req_data,
        srv_req_data,
) -> None:
    description = inspect.cleandoc(
        f"""
        Request data contains 'reply' section but no data was generated
        request_name: '{request_name}'
        """
    )
    runtime_error_wrapper(description, req_data, srv_req_data)


def print_request_body(body) -> None:
    print(
        f"""
body of request:
-----------
{body}
----------"""
    )
