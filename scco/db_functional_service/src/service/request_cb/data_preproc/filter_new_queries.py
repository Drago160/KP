import datetime
import dateutil.parser as date_parser
import json

from sqlalchemy import tuple_

import util.app_config as app_cfg
from util.app_errors import get_correctly_typed_dicts

from util.app_errors import check_not_empty_array

from crud.models import Query
from crud.objects.query import QueryCRUD
import crud.type_map as type_map

from service.request_cb.request_cb import RequestCallback


class FilterNewQueries(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter FilterNewQueries callback")

        # Validate req_data to be array
        if not check_not_empty_array(req_data, srv_req_data):
            print("Exit without sending answer")
            return

        # Validate keys.
        required_keys_type_map = {
            "customer_id": type_map.CustomerId,
            "client_id": type_map.ClientId,
            "channel_id": type_map.ChannelId,
            "message_date": str,
        }
        required_keys = required_keys_type_map.keys()
        req_dicts = get_correctly_typed_dicts(
            required_keys_type_map=required_keys_type_map,
            data=req_data,
        )

        req_map = {}
        print("req_map = {")
        for row in req_dicts:
            row["client_id"] = row["client_id"]
            sort_key = get_sort_key(row, required_keys)
            req_map[sort_key] = row
            print(f"{sort_key} --- {row}")
        print("}")

        # Make db query.
        print("Creating query")
        columns = [
            Query.customer_id,
            Query.client_id,
            Query.channel_id,
            Query.message_date,
        ]
        tup = tuple_(*columns)
        tup.in_(req_map.keys())

        print("Start query")
        result_set = QueryCRUD.select_all(
            columns=columns,
            wheres_cond=[
                tup.in_(req_map.keys())
            ],
        )
        print(f"result_set:\n{result_set}")

        print("Process result_set")
        res_dict = dict(req_map)
        for row in result_set:
            act_key = get_sort_key_row(row, required_keys)
            if act_key not in res_dict:
                print(f"row.customer_id = {row.customer_id}")
                print(f"act_key = {act_key}")
                print(f"res_dict = {res_dict}")
            del res_dict[act_key]

        res = list(res_dict.values())

        print("Preparing answer")
        answer = {
            "not_exist": res,
        }
        return answer


################################################################################

# Helpers


def get_sort_key(row, required_keys):
    res_list = []
    for key in required_keys:
        value = row[key]
        if key == "message_date":
            # reformat string
            value_datatime = date_parser.parse(value)
            value = value_datatime.strftime(app_cfg.DATETIME_FORMAT)
        res_list.append(value)
    return tuple(res_list)


def get_sort_key_row(row, required_keys):
    res_list = []

    for key in required_keys:
        print(f"key = {key}")
        field = row.__getattribute__(key)

        if isinstance(field, datetime.datetime):
            print(f"is instance of datetime.datetime")
            field = field.strftime(app_cfg.DATETIME_FORMAT)
        print(f"try append {key}")
        res_list.append(field)

    print(f"return tuple: {res_list}")
    return tuple(res_list)
