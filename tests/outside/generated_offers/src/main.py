import pika
import os
import sys


# Getting environment variables.
RMQ_NET_ALIAS = os.environ.get('RMQ_NET_ALIAS')
GENERATED_OFFERS_EXCHANGE = os.environ.get('GENERATED_OFFERS_EXCHANGE')
GENERATED_OFFERS_QUEUE = os.environ.get('GENERATED_OFFERS_QUEUE')
GENERATED_OFFERS_ROUTING_KEY = os.environ.get('GENERATED_OFFERS_ROUTING_KEY')


def create_channel():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=RMQ_NET_ALIAS)  # accepts credentials
    )
    chan = conn.channel()
    # channel.basic_qos(10, global_qos=False)

    return conn, chan


def declare_exchange(chan):
    chan.exchange_declare(
        exchange=GENERATED_OFFERS_EXCHANGE,
        exchange_type='direct',
    )


def declare_publish_queue(chan):
    pass


def declare_consumer_queue(chan):
    # generated_offers queue.
    chan.queue_declare(
        queue=GENERATED_OFFERS_QUEUE
    )
    chan.queue_bind(
        exchange=GENERATED_OFFERS_EXCHANGE,
        queue=GENERATED_OFFERS_QUEUE,
        routing_key=GENERATED_OFFERS_ROUTING_KEY,
    )


def handling(conn, chan):
    chan.basic_consume(
        queue=GENERATED_OFFERS_QUEUE,
        on_message_callback=callback,
    )

    print('[*] Waiting for messages. To exit press CTRL+C', file=sys.stderr)
    print(f'CLIENT_QUERIES_QUEUE = {GENERATED_OFFERS_QUEUE}', file=sys.stderr)
    chan.start_consuming()  # Infinite loop.


def callback(ch, method, properties, body):
    print(f"[x] Received {body}", file=sys.stderr)


def main():
    conn, chan = create_channel()
    declare_exchange(chan)
    declare_publish_queue(chan)
    declare_consumer_queue(chan)
    handling(conn, chan)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)
        sys.exit(2)
