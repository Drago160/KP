import sys
import inspect

import crud.dbapi as dbapi
from crud.models import Base

from broker.host_broker import HostBroker
from service.dispatcher import Dispatcher

from testing.init_db import dummy_init_db

################################################################################

# Requests.

# data_preprocessing
from service.data.data_preproc.filter_new_queries import (
    request_simple as fnq_request,
    request_custom_datetime as fnq_datetime_request,
    request_cast_type as fnq_cast_request,
)
from service.data.data_preproc.insert_new_queries_csv import (
    request_simple as inq_csv_request,
)
from service.data.data_preproc.get_customers_lists import (
    request_simple as gcl_request,
)
from service.data.data_preproc.insert_preprocessed_queries import (
    request_simple as ipq_request,
)

# ml_co_gen
from service.data.ml_co_gen.get_info_for_co_generation import (
    request_simple as gifcg_request,
)

# pdf_co_gen
from service.data.pdf_co_gen.insert_offers import (
    request_simple as io_request
)

# customer_creator
from service.data.customer_creator.insert_customer import (
    request_simple as ic_request
)

# manual
from service.data.manual.map_offers_to_messages import (
    request_simple as motom_request
)


################################################################################

def init_database():
    print("Creating db engine", flush=True)
    engine = dbapi.DbEngine.get_engine()

    print("Removing old tables", flush=True)
    Base.metadata.drop_all(engine)

    print("Creating tables", flush=True)
    Base.metadata.create_all(engine)

    print("Inserting dummy values", flush=True)
    dummy_init_db()


def main():
    init_database()

    broker = HostBroker()
    dispatcher = Dispatcher(broker)

    disp_requests = {
        # data_preproc
        "filter_new_queries": [
            # fnq_request,
            # fnq_datetime_request,
            fnq_cast_request,
        ],
        "insert_new_queries_csv": [inq_csv_request],
        "get_customers_lists": [gcl_request],
        "insert_preprocessed_queries": [ipq_request],

        # ml_co_gen
        "get_info_for_co_generation": [gifcg_request],

        # pdf_co_gen
        "insert_offers": [io_request],

        # customer_creator
        "insert_customer": [ic_request],

        # manual
        "map_offers_to_messages": [motom_request],
    }

    name = "filter_new_queries"  # CHANGE ME

    for i, req in enumerate(disp_requests[name]):
        print(
            inspect.cleandoc(
                f"""
                *****************
                Request {i}
                *****************
                """
            )
        )
        dispatcher.dispatch_function(req)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        raise e
        # sys.exit(2)


################################################################################


# def text_query():
#     textual_sql = text(
#         "SELECT id, name, fullname FROM user_account ORDER BY id"
#         )
#     textual_sql = textual_sql.columns(User.id, User.name, User.fullname)
#     orm_sql = select(User).from_statement(textual_sql)
#     for user_obj in session.execute(orm_sql).scalars():
#         print(user_obj)
