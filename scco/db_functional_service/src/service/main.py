import sys

import crud.dbapi as dbapi
from crud.models import Base

from broker.rmq_broker import RmqBroker
from service.dispatcher import Dispatcher
from db_insert_on_first_startup import check_first_startup
from db_insert_on_first_startup import db_insert_on_first_startup


def init_database():
    print("Creating db engine", flush=True)
    engine = dbapi.DbEngine.get_engine()

    # print("Removing old tables", flush=True)
    # Base.metadata.drop_all(engine)

    print("Creating tables", flush=True)
    Base.metadata.create_all(engine)

    if check_first_startup():
        print("Inserting customers on first startup", flush=True)
        db_insert_on_first_startup()
    else:
        print("Skip inserting customers on first startup"
              "(must be already inserted)", flush=True)


def main():
    init_database()

    print("Creating broker", flush=True)
    broker = RmqBroker()

    print("Creating dispatcher", flush=True)
    dispatcher = Dispatcher(broker)

    print("Start consuming", flush=True)
    broker.start_consuming()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)
