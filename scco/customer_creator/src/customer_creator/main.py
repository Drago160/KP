import sys
import logging

from broker_for_creator.Broker import Broker
from broker_for_creator.RmqBroker import RmqBroker

from steps.insertToDb import InsertToDb

def main():
    logging.info("Customer creator:Creating RmqBroker...")
    broker: Broker = RmqBroker()
    logging.info("RmqBroker created")

    logging.info("Creating insertToDb...")
    insertToDb = InsertToDb(broker)
    logging.info("InsertToDb created")

    logging.info("Start consuming...")
    broker.start_consuming()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.error('Interrupted', file=sys.stderr)
    except Exception as e:
        logging.error(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)

