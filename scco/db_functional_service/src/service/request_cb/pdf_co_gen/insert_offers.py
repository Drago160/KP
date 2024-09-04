import inspect

from util.app_errors import dict_get_or_panic
from util.app_errors import runtime_error_wrapper

from sqlalchemy import desc

from crud.models import Query
from crud.objects.offer import OfferCRUD
from crud.objects.query import QueryCRUD

from service.request_cb.request_cb import RequestCallback
from service.request_cb.request_cb import print_result_set


class InsertOffers(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter InsertOffers callback")

        required_keys = [
            "message_group_id",
            "file_path",
        ]

        answer_list = []

        for row in req_data:
            # Validate keys.
            data_dict = {}
            for key in required_keys:
                data_dict[key] = dict_get_or_panic(row, key, srv_req_data)

            query_data = select_from_query(data_dict, req_data, srv_req_data)
            data_dict.update(query_data)

            # Hook file to the most recent message in the message group.
            OfferCRUD.insert_one(
                {
                    "query_id": data_dict["query_id"],
                    "file_path": data_dict["file_path"],
                }
            )

            answer_list.append(
                {
                    "customer_id": data_dict["customer_id"],
                    "client_id": data_dict["client_id"],
                    "file_path": data_dict["file_path"],
                }
            )

        print("Preparing answer")
        answer = {
            "array_data": answer_list,
        }
        return answer

################################################################################

# Helpers


def select_from_query(data_dict, req_data, srv_req_data) -> dict:
    result_all = QueryCRUD.select_all(
        columns=[
            Query.query_id,
            Query.customer_id,
            Query.client_id,
        ],
        wheres_cond=[
            Query.message_group_id == data_dict["message_group_id"]
        ],
        order_bys=[desc(Query.message_date)],
    )
    if len(result_all) == 0 or result_all is None:
        description = inspect.cleandoc(
            f"""
            unexpected error: no such message_group_id in table.
            message_group_id: {data_dict["message_group_id"]}
            """
        )
        runtime_error_wrapper(description, req_data, srv_req_data)

    result_first = result_all[0]
    print_result_set(result_first)

    res = {
        "query_id": result_first.query_id,
        "customer_id": result_first.customer_id,
        "client_id": result_first.client_id,
    }

    return res
