import inspect
import datetime
import json
import os

import crud.message_group_id_generator as mgig

from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD
from crud.objects.client import ClientCRUD
from crud.objects.new_queries_csv import NewQueriesCsvCRUD
from crud.objects.query import QueryCRUD
from crud.objects.offer import OfferCRUD

import util.app_config as app_cfg

TESTING_PKG_DIR = os.path.dirname(__file__)


def parse_customer(json_path: str) -> (dict, list[dict]):
    with open(json_path, "r") as f:
        customer_json = json.load(f)

    # Customer
    customer = dict(customer_json)
    del customer["services"]

    # Customer services
    customer_services = customer_json["services"]
    for service in customer_services:
        service.update({"customer_id": customer["customer_id"]})

    return customer, customer_services


def dummy_init_db() -> None:
    print("start dummy_init_db")

    ############################################################################
    # Customer.
    customer_1, customer_1_services = parse_customer(
        f"{TESTING_PKG_DIR}/data/customer_1.json"
    )
    customer_2, customer_2_services = parse_customer(
        f"{TESTING_PKG_DIR}/data/customer_2.json"
    )

    print("Start insert customers")
    CustomerCRUD.insert_all([
        customer_1,
        customer_2,
    ])
    print("Finished insert customers")

    ############################################################################
    # CustomerService.

    print("Start insert customer_service")
    CustomerServiceCRUD.insert_all([
        *customer_1_services,
        *customer_2_services,
    ])
    print("Finished insert customer_service")

    insert_misc(customer_1, customer_2)

    print("finished dummy_init_db")


def insert_misc(customer_1, customer_2):
    ############################################################################
    # Client.
    client_1 = {
        "client_id": "client_1",
        "attitude": "Вы",
    }
    client_2 = {
        "client_id": "client_2",
        "attitude": "Ты",
    }
    print("Start insert clients")
    ClientCRUD.insert_all(
        [
            client_1,
            client_2,
        ]
    )
    print("Finished insert clients")

    ############################################################################
    # NewQueriesCsv.
    new_queries_csv_1 = {
        "csv_path": "path/to/new_queries1.csv",
    }
    new_queries_csv_2 = {
        "csv_path": "path/to/new_queries2.csv",
    }
    print("Start insert new_queries_csv")
    csv_ids = NewQueriesCsvCRUD.insert_all(
        [
            new_queries_csv_1,
            new_queries_csv_2,
        ]
    )
    print("Finished insert new_queries_csv")

    ############################################################################
    # Query.
    query_1 = {
        # "query_id": auto,
        "customer_id": customer_1["customer_id"],
        "client_id": client_1["client_id"],
        "csv_id": csv_ids[0],
        "channel_id": "phystech.career",
        "message": inspect.cleandoc(
            """#ищу
            Нужен разработчик на python для вёрстки сайта авто компании.
            Предложения пишите в телеграм: @client_1_tg
            """
        ),
        "message_group_id": mgig.IdGenerator.reserve_id(),
        "message_date": datetime.datetime.strptime(
            "2023-12-31T22:59:00",
            app_cfg.DATETIME_FORMAT
        ),
    }
    query_2 = {
        "customer_id": customer_1["customer_id"],
        "client_id": client_2["client_id"],
        "csv_id": csv_ids[1],
        "channel_id": "phystech.career",
        "message": inspect.cleandoc(
            """Нужен разработчик на android
            Требуется сделать приложение для онлайн-магазина, подробности в лс
            """
        ),
        "message_group_id": mgig.IdGenerator.reserve_id(),
        "message_date": datetime.datetime.strptime(
            "2023-12-31T23:59:00",
            app_cfg.DATETIME_FORMAT
        ),
    }
    print("Start insert queries")
    query_id_list = QueryCRUD.insert_all(
        [
            query_1,
            query_2,
        ]
    )
    print("Finished insert queries")

    ############################################################################
    # Offer.
    offer_1 = {
        "query_id": query_id_list[0],
        "file_path": "/path/to/offer1.pdf",
    }
    offer_2 = {
        "query_id": query_id_list[1],
        "file": "/path/to/offer2",
    }
    print("Start insert offers")
    OfferCRUD.insert_all(
        [
            offer_1,
            # offer_2,
        ]
    )
    print("Finished insert offers")
