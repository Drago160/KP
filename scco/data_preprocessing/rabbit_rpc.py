import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
import json
import uuid
import config


def declare_rabbit_db_service(ch):
    ch.exchange_declare(exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE, exchange_type='topic', durable=True)
    ch.queue_declare(queue=config.DB_FUNCTIONAL_SERVICE_QUEUE, durable=True)
    ch.queue_bind(
        exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE,
        queue=config.DB_FUNCTIONAL_SERVICE_QUEUE,
        routing_key=config.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
    )


class FilterRpcClient:
    def __init__(self, connection: BlockingConnection, channel: BlockingChannel):
        if config.DEBUG_ISOLATED:
            return

        self.connection = connection
        self.channel = channel
        declare_rabbit_db_service(self.channel)

        self.channel.exchange_declare(exchange=config.CONTAINS_REQUEST_EXCHANGE, exchange_type='topic', durable=True)
        self.channel.queue_declare(queue=config.CONTAINS_REQUEST_QUEUE, durable=True)
        self.channel.queue_bind(
            exchange=config.CONTAINS_REQUEST_EXCHANGE,
            queue=config.CONTAINS_REQUEST_QUEUE,
            routing_key=config.CONTAINS_REQUEST_ROUTING_KEY,
        )

        self.channel.basic_consume(
            queue=config.CONTAINS_REQUEST_QUEUE, on_message_callback=self.on_response, auto_ack=False
        )

        self.reply_ctx = None
        self.response = None

    def on_response(self, ch, method, props, body):
        print('Debug: Filter on response', flush=True)
        json_body = json.loads(body.decode())
        if self.reply_ctx == json_body['reply_ctx']:
            self.response = json_body['not_exist']
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, request_data):
        self.response = None
        self.reply_ctx = uuid.uuid4().hex
        request = json.dumps(
            {
                "request_name": "filter_new_queries",
                "reply": {
                    "exchange": config.CONTAINS_REQUEST_EXCHANGE,
                    "routing_key": config.CONTAINS_REQUEST_ROUTING_KEY,
                },
                "reply_ctx": self.reply_ctx,
                "request_data": request_data,
            },
            ensure_ascii=False,
        )
        print(" [X] Sending request", request, flush=True)

        if config.DEBUG_ISOLATED:
            return request_data  # as if all messages were new

        self.channel.basic_publish(
            exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE,
            routing_key=config.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
            body=request,
        )

        while self.response is None:
            print('Debug: Filter loop', flush=True)
            self.connection.process_data_events(time_limit=1)
        return self.response


class SaveCsvRpcClient:
    def __init__(self, connection: BlockingConnection, channel: BlockingChannel, new_queries_csv_info: dict):
        self.new_queries_csv_info = new_queries_csv_info

        if config.DEBUG_ISOLATED:
            return

        self.connection = connection
        self.channel = channel
        declare_rabbit_db_service(self.channel)

        self.channel.exchange_declare(
            exchange=config.INSERT_NEW_QUERIES_REQUEST_EXCHANGE, exchange_type='topic', durable=True
        )
        self.channel.queue_declare(queue=config.INSERT_NEW_QUERIES_REQUEST_QUEUE, durable=True)
        self.channel.queue_bind(
            exchange=config.INSERT_NEW_QUERIES_REQUEST_EXCHANGE,
            queue=config.INSERT_NEW_QUERIES_REQUEST_QUEUE,
            routing_key=config.INSERT_NEW_QUERIES_REQUEST_ROUTING_KEY,
        )

        self.channel.basic_consume(
            queue=config.INSERT_NEW_QUERIES_REQUEST_QUEUE, on_message_callback=self.on_response, auto_ack=False
        )

        self.new_queries_csv_info = new_queries_csv_info
        self.response = None

    def on_response(self, ch, method, props, body):
        json_body = json.loads(body.decode())
        if self.new_queries_csv_info['path'] == json_body['csv_path']:  # TODO is it ok?
            self.response = json_body['csv_path']
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self):
        self.response = None
        request = json.dumps(
            {
                "request_name": "insert_new_queries_csv",
                "reply": {
                    "exchange": config.INSERT_NEW_QUERIES_REQUEST_EXCHANGE,
                    "routing_key": config.INSERT_NEW_QUERIES_REQUEST_ROUTING_KEY,
                },
                "request_data": {
                    "csv_path": self.new_queries_csv_info['path'],
                },
            },
            ensure_ascii=False,
        )
        print(" [X] Sending request", request, flush=True)

        if config.DEBUG_ISOLATED:
            return self.new_queries_csv_info['path']

        self.channel.basic_publish(
            exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE,
            routing_key=config.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
            body=request,
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=1)
        return self.response


class MatchingListsRpcClient:
    def __init__(self, connection: BlockingConnection, channel: BlockingChannel, new_queries_csv_info: dict):
        self.saved = dict()

        if config.DEBUG_ISOLATED:
            return

        self.connection = connection
        self.channel = channel
        declare_rabbit_db_service(self.channel)

        self.channel.exchange_declare(
            exchange=config.CUSTOMER_LISTS_REQUEST_EXCHANGE, exchange_type='topic', durable=True
        )
        self.channel.queue_declare(queue=config.CUSTOMER_LISTS_REQUEST_QUEUE, durable=True)
        self.channel.queue_bind(
            exchange=config.CUSTOMER_LISTS_REQUEST_EXCHANGE,
            queue=config.CUSTOMER_LISTS_REQUEST_QUEUE,
            routing_key=config.CUSTOMER_LISTS_REQUEST_ROUTING_KEY,
        )

        self.channel.basic_consume(
            queue=config.CUSTOMER_LISTS_REQUEST_QUEUE, on_message_callback=self.on_response, auto_ack=False
        )

        self.reply_ctx = None
        self.response = None

    def load_default_lists(self):
        with open('resources/sample_data/user_blacklist') as f:
            black_list = [s.strip() for s in f.readlines()]
        if '' in black_list:
            black_list.remove('')
        with open('resources/sample_data/user_whitelist') as f:
            white_list = [s.strip() for s in f.readlines()]
        if '' in white_list:
            white_list.remove('')
        return {'black_list': black_list, 'white_list': white_list}

    def on_response(self, ch, method, props, body):
        json_body = json.loads(body.decode())
        if self.reply_ctx == json_body['reply_ctx']:
            if len(json_body['array_data']) > 0:
                self.response = json_body['array_data'][0]
            else:
                print('Warning: black or white list for client not found. Loading default lists')
                self.response = self.load_default_lists()
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, customer_id):
        self.response = None
        self.reply_ctx = uuid.uuid4().hex
        request = json.dumps(
            {
                "request_name": "get_customers_lists",
                "reply": {
                    "exchange": config.CUSTOMER_LISTS_REQUEST_EXCHANGE,
                    "routing_key": config.CUSTOMER_LISTS_REQUEST_ROUTING_KEY,
                },
                "reply_ctx": self.reply_ctx,
                "request_data": [
                    {
                        "customer_id": customer_id,
                    }
                ],
            },
            ensure_ascii=False,
        )
        print(" [X] Sending request", request, flush=True)

        if config.DEBUG_ISOLATED:
            return self.load_default_lists()

        self.channel.basic_publish(
            exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE,
            routing_key=config.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
            body=request,
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=1)
        return self.response

    def get_black_list(self, customer_id):
        response = self.call(customer_id)
        self.saved[customer_id] = response['white_list']
        return response['black_list']

    def get_white_list(self, customer_id):
        if customer_id in self.saved:
            return self.saved[customer_id]
        else:
            return self.call(customer_id)['white_list']


class InsertToDbRpcClient:
    def __init__(self, connection: BlockingConnection, channel: BlockingChannel, new_queries_csv_info: dict):
        self.new_queries_csv_info = new_queries_csv_info

        if config.DEBUG_ISOLATED:
            return

        self.connection = connection
        self.channel = channel
        declare_rabbit_db_service(self.channel)

        self.channel.exchange_declare(
            exchange=config.INSERT_RESULT_REQUEST_EXCHANGE, exchange_type='topic', durable=True
        )
        self.channel.queue_declare(queue=config.INSERT_RESULT_REQUEST_QUEUE, durable=True)
        self.channel.queue_bind(
            exchange=config.INSERT_RESULT_REQUEST_EXCHANGE,
            queue=config.INSERT_RESULT_REQUEST_QUEUE,
            routing_key=config.INSERT_RESULT_REQUEST_ROUTING_KEY,
        )

        self.channel.basic_consume(
            queue=config.INSERT_RESULT_REQUEST_QUEUE, on_message_callback=self.on_response, auto_ack=False
        )

        self.response = None

    def on_response(self, ch, method, props, body):
        json_body = json.loads(body.decode())
        if self.new_queries_csv_info['path'] == json_body['reply_ctx']:  # TODO is it ok?
            self.response = json_body['array_data']
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, items):
        self.response = None
        request = json.dumps(
            {
                "request_name": "insert_preprocessed_queries",
                "reply_ctx": self.new_queries_csv_info['path'],
                "reply": {
                    "exchange": config.INSERT_RESULT_REQUEST_EXCHANGE,
                    "routing_key": config.INSERT_RESULT_REQUEST_ROUTING_KEY,
                },
                "request_data": {"csv_path": self.new_queries_csv_info['path'], "array_data": items},
            },
            ensure_ascii=False,
        )
        print(" [X] Sending request", request, flush=True)

        if config.DEBUG_ISOLATED:
            return [3, 4, 5]

        self.channel.basic_publish(
            exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE,
            routing_key=config.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
            body=request,
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=1)
        return self.response
