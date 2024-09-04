import inspect

from sqlalchemy import desc

from util.app_errors import dict_get_or_panic
from util.app_errors import runtime_error_wrapper

from crud.models import Query
from crud.models import Client
from crud.models import Customer
from crud.models import CustomerService

from crud.objects.query import QueryCRUD
from crud.objects.client import ClientCRUD
from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD

from service.request_cb.request_cb import RequestCallback
from service.request_cb.request_cb import print_result_set


class GetInfoForCoGeneration(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter GetInfoForCoGeneration callback")

        required_keys = [
            "message_group_id",
        ]

        # Validate keys.
        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(req_data, key, srv_req_data)

        answer = {}

        # Query 1.
        answer_query = get_from_query_table(
            data_dict,
            req_data,
            srv_req_data,
        )
        answer.update(answer_query)
        data_dict["client_id"] = answer_query["client_id"]
        data_dict["customer_id"] = answer_query["customer_id"]

        # Query 2.
        answer_client = get_from_client_table(
            data_dict,
            req_data,
            srv_req_data,
        )
        answer.update(answer_client)

        # Query 3.
        answer_customer = get_from_customer_table(
            data_dict,
            req_data,
            srv_req_data,
        )
        answer.update(answer_customer)

        # Query 4.
        answer_customer_service = get_from_customer_service_table(
            data_dict,
            req_data,
            srv_req_data,
        )
        answer.update(answer_customer_service)
        return answer

################################################################################

# Helpers


def arise_error(field_name, data_dict, req_data, srv_req_data):
    description = inspect.cleandoc(
        f"""
        invalid {field_name}: given value does not exist
        {field_name}: {data_dict[field_name]}
        """
    )
    runtime_error_wrapper(description, req_data, srv_req_data)


def get_from_query_table(data_dict, req_data, srv_req_data) -> dict:
    print("Start get_from_query_table")

    result_set = QueryCRUD.select_all(
        [
            Query.customer_id,
            Query.client_id,
            Query.channel_id,
            Query.message,
        ],
        wheres_cond=[
            Query.message_group_id == data_dict["message_group_id"],
        ],
        order_bys=[
            desc(Query.message_date),
        ],
    )
    print("QueryCRUD.select_all completed")

    if result_set is None or len(result_set) == 0:
        arise_error("message_group_id", data_dict, req_data, srv_req_data)

    print_result_set(result_set)

    customer_id = result_set[0].customer_id
    client_id = result_set[0].client_id
    channel_ids = []
    messages = []
    for row in result_set:
        channel_ids.append(row.channel_id)
        messages.append(row.message)

    answer = {
        "customer_id": customer_id,
        "client_id": client_id,
        "channel_ids": channel_ids,
        "messages": messages,
    }

    return answer


def get_from_client_table(data_dict, req_data, srv_req_data) -> dict:
    print("Start get_from_client_table")

    result_one = ClientCRUD.select_one(
        [
            Client.attitude,
        ],
        wheres_cond=[
            Client.client_id == data_dict["client_id"],
        ],
    )
    print("ClientCRUD.select_one completed")

    if result_one is None:
        arise_error("client_id", data_dict, req_data, srv_req_data)

    print_result_set(result_one)

    answer = {
        "attitude": result_one.attitude,
    }

    return answer


def get_from_customer_table(data_dict, req_data, srv_req_data) -> dict:
    print("Start get_from_customer_table")

    result_one = CustomerCRUD.select_one(
        [
            Customer.company_name,
            Customer.contact_info,
            Customer.tags,
            Customer.white_list,
            Customer.specific_features,
        ],
        wheres_cond=[
            Customer.customer_id == data_dict["customer_id"],
        ],
    )
    print("CustomerCRUD.select_one completed")

    if result_one is None:
        arise_error("customer_id", data_dict, req_data, srv_req_data)

    print_result_set(result_one)

    answer = {
        "company_name": result_one.company_name,
        "contact_info": result_one.contact_info,
        "tags": result_one.tags,
        "white_list": result_one.white_list,
        "specific_features": result_one.specific_features,
    }

    return answer


def get_from_customer_service_table(
        data_dict,
        query_data,
        db_query,
) -> dict:
    print("Start get_from_customer_service_table")

    result_set = CustomerServiceCRUD.select_all(
        [
            CustomerService.service_name,
            CustomerService.service_desc,
        ],
        wheres_cond=[
            CustomerService.customer_id == data_dict["customer_id"],
        ],
    )
    print("CustomerServiceCRUD.select_all completed")

    if result_set is None:
        arise_error("customer_id", data_dict, query_data, db_query)

    print_result_set(result_set)

    services_list = []
    for row in result_set:
        services_list.append(
            {
                "service_name": row.service_name,
                "service_desc": row.service_desc,
            }
        )

    answer = {
        "customer_services": services_list,
    }

    return answer
