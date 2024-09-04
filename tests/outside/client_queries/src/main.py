import os
import sys

import pika


# Getting environment variables.
RMQ_NET_ALIAS = os.environ.get('RMQ_NET_ALIAS')
CLIENT_QUERIES_EXCHANGE = os.environ.get('CLIENT_QUERIES_EXCHANGE')
CLIENT_QUERIES_QUEUE = os.environ.get('CLIENT_QUERIES_QUEUE')
CLIENT_QUERIES_ROUTING_KEY = os.environ.get('CLIENT_QUERIES_ROUTING_KEY')
OUTPUT_CSV_PATH = os.environ.get('OUTPUT_CSV_PATH')

OUTSIDE_VOLUME_DOCKER = os.environ.get('OUTSIDE_VOLUME_DOCKER')
RELATIVE_CSV_PATH_DOCKER = os.environ.get('CSV_PATH_DOCKER')
CSV_PATH_DOCKER = f"{OUTSIDE_VOLUME_DOCKER}/{RELATIVE_CSV_PATH_DOCKER}"

# # RMQ_URL = "amqp://guest:guest@rmq:5672/"
# RMQ_URL = "127.0.0.1:5672"


def create_channel():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=RMQ_NET_ALIAS)  # accepts credentials
    )
    chan = conn.channel()
    # channel.basic_qos(10, global_qos=False)

    return conn, chan


def declare_exchange(chan):
    chan.exchange_declare(
        exchange=CLIENT_QUERIES_EXCHANGE,
        exchange_type='direct',
    )


def declare_publish_queue(chan):
    # client_queries queue.
    chan.queue_declare(
        queue=CLIENT_QUERIES_QUEUE
    )
    chan.queue_bind(
        exchange=CLIENT_QUERIES_EXCHANGE,
        queue=CLIENT_QUERIES_QUEUE,
        routing_key=CLIENT_QUERIES_ROUTING_KEY,
    )


def declare_consumer_queue(chan):
    pass


def handling(conn, chan):
    # Create body of publish message.
    body = CSV_PATH_DOCKER.encode('utf-8')

    # Publish messages to queue.
    chan.basic_publish(
        exchange=CLIENT_QUERIES_EXCHANGE,
        routing_key=CLIENT_QUERIES_ROUTING_KEY,
        body=body,
    )
    print("[x] Sent 'Hello World!'")
    print(f"OUTPUT_CSV_PATH = {OUTPUT_CSV_PATH}")
    print(f"CLIENT_QUERIES_QUEUE = {CLIENT_QUERIES_QUEUE}", file=sys.stderr)

    conn.close()


def main():
    conn, chan = create_channel()
    declare_exchange(chan)
    declare_publish_queue(chan)
    declare_consumer_queue(chan)
    handling(conn, chan)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)
        sys.exit(2)


# def main():
#     # Set the connection parameters to connect to rabbit-server1 on port 5672
#     # on the / virtual host using the username "guest" and password "guest"
#     credentials = pika.PlainCredentials('guest', 'guest')
#     parameters = pika.ConnectionParameters(
#         'rabbit-server1',
#         5672,
#         '/',
#         credentials
#         )
