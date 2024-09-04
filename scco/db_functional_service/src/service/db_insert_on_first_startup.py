import os

from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD

from testing.init_db import parse_customer
from testing.init_db import insert_misc

SERVICE_PKG_DIR = os.path.dirname(__file__)
FIRST_STARTUP_LOCK_FILE_NAME = "first-startup.lock"
INSERT_TO_DB_ON_FIRST_STARTUP = False  # one-hot disable


def check_first_startup() -> bool:
    if not INSERT_TO_DB_ON_FIRST_STARTUP:
        return False
    lock_file = f"{SERVICE_PKG_DIR}/{FIRST_STARTUP_LOCK_FILE_NAME}"
    if os.path.exists(lock_file):
        return False
    open(lock_file, "w")  # creating lock file
    return True


def db_insert_on_first_startup() -> None:
    print("start db_insert_dummy_values")

    ############################################################################
    # Customer.

    customer_1, customer_1_services = parse_customer(
        f"{SERVICE_PKG_DIR}/data/init_db/customer_it.json"
    )
    customer_2, customer_2_services = parse_customer(
        f"{SERVICE_PKG_DIR}/data/init_db/customer_builder.json"
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

    ############################################################################

    additional_insert_for_testing(customer_1, customer_2)

    print("finished dummy_init_db")


def additional_insert_for_testing(customer_1, customer_2):
    insert_misc(customer_1, customer_2)
