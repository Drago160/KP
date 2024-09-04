import inspect

from util.app_errors import dict_get_or_panic
from util.app_errors import runtime_error_wrapper

from util.app_errors import check_not_empty_array
from util.app_errors import get_correctly_typed_dicts
from util.app_errors import assert_cast

import crud.message_group_id_generator as mgig
from crud.models import NewQueriesCsv
from crud.objects.query import QueryCRUD
from crud.objects.client import ClientCRUD
from crud.objects.new_queries_csv import NewQueriesCsvCRUD
import crud.type_map as type_map

from service.request_cb.request_cb import RequestCallback


class InsertPreprocessedQueries(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        arr = dict_get_or_panic(req_data, "array_data", srv_req_data)
        csv_path = dict_get_or_panic(req_data, "csv_path", srv_req_data)

        # Validate req_data to be array
        if not check_not_empty_array(arr, srv_req_data, "array_data"):
            print("Exit without sending answer")
            return

        # Check keys of array_data.
        required_keys_type_map = {
            "customer_id": type_map.CustomerId,
            "client_id": type_map.ClientId,
            "channel_ids": list[type_map.ChannelId],
            "messages": list[type_map.Text],
            "message_dates": list[str],
        }
        req_dicts = get_correctly_typed_dicts(
            required_keys_type_map=required_keys_type_map,
            data=arr,
        )

        csv_id = get_csv_id(csv_path, req_dicts, srv_req_data)

        group_ids = []

        for row in req_dicts:
            check_lens(row, srv_req_data)

            client_id = assert_cast(
                row["client_id"],
                type_map.ClientId,
                "field_name: client_id",
            )
            insert_new_client(client_id)
            row["csv_id"] = csv_id
            group_id = insert_message_group(row)
            group_ids.append(group_id)

        print("Preparing answer")
        answer = {
            "array_data": group_ids,
        }
        return answer

################################################################################

# Helpers

def get_csv_id(csv_path: str, req_dicts, srv_req_data) -> type_map.CsvId:
    print("Start get_csv_id")

    csv_ind = NewQueriesCsvCRUD.select_one(
        [NewQueriesCsv.csv_id],
        [NewQueriesCsv.csv_path == csv_path]
    )

    if csv_ind is None:
        description = inspect.cleandoc(
            f"""
            Passed csv_path is not presented in the database.
            csv_path = {csv_path}
            """
        )
        runtime_error_wrapper(description, req_dicts, srv_req_data)
    else:
        csv_ind = csv_ind.csv_id

    print(
        f"Finish get_csv_id\n"
        f"csv_file_ind = {csv_ind}"
        )

    return csv_ind


def flatten_data_dict(arr_obj: dict) -> list[dict]:
    zip_obj = zip(
        arr_obj["channel_ids"],
        arr_obj["messages"],
        arr_obj["message_dates"],
    )

    res = []
    for chan, msg, date in zip_obj:
        res_item = {}
        for k, v in arr_obj.items():
            if k == "channel_ids":
                typed_chan = type_map.ChannelId(chan)
                res_item["channel_id"] = typed_chan
            elif k == "messages":
                typed_msg = type_map.Text(msg)
                res_item["message"] = typed_msg
            elif k == "message_dates":
                typed_date = str(date)
                res_item["message_date"] = typed_date
            else:
                res_item[k] = v
        res.append(res_item)

    return res


def check_lens(row, srv_req_data) -> None:
    ch_ids_len = len(row["channel_ids"])
    msg_len = len(row["messages"])
    msg_dates_len = len(row["message_dates"])

    if msg_len != ch_ids_len or msg_len != msg_dates_len:
        description = inspect.cleandoc(
            f"""
            Length of channel_ids, messages and message_dates do not match
            len(channel_ids) = {ch_ids_len}
            len(messages) = {msg_len}
            len(message_dates) = {msg_dates_len}
            """
        )
        runtime_error_wrapper(description, row, srv_req_data)


def insert_new_client(client_id):
    # Insert new client.
    if not ClientCRUD.contain(client_id):
        print("Insert new client")
        ClientCRUD.insert_one(
            {
                "client_id": client_id,
                "attitude": "default"
            }
        )
        print("Insert new client finished")


def insert_message_group(data_dict) -> type_map.MessageGroupId:
    print("Start insert_message_group")

    # Prepare data for insertion.
    group_id = mgig.IdGenerator.reserve_id()

    insert_dicts = flatten_data_dict(data_dict)
    for query_dict in insert_dicts:
        query_dict["csv_id"] = data_dict["csv_id"]
        query_dict["message_group_id"] = group_id

    # Insert queries.
    QueryCRUD.insert_all(insert_dicts)

    print("insert_message_group finished")

    return group_id
