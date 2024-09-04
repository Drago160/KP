import inspect
import os
import json
import enum

import util.app_config as app_cfg
from util.app_errors import dict_get_or_panic
from util.app_errors import runtime_error_wrapper

from sqlalchemy import asc
from sqlalchemy import desc

from crud.models import Query
from crud.models import Offer
from crud.objects.offer import OfferCRUD
from crud.objects.query import QueryCRUD
from crud.type_map import MessageGroupId
from crud.type_map import QueryId
from crud.type_map import FilePath
from crud.type_map import Text
from crud.type_map import CustomerId

from service.request_cb.request_cb import RequestCallback
from service.request_cb.request_cb import print_result_set


class FileStatus(enum.Enum):
    OFFER_FILE_NOT_EXIST = 1
    MESSAGES_FILE_EXIST = 2
    MESSAGES_FILE_SAVED = 3


class MapOffersToMessages(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter MapOffersToMessages callback")

        required_keys = [
            "message_group_id_begin",
            "message_group_id_end",
            "overwrite",
        ]

        file_exist_mg_ids = []
        offer_file_not_exist_mg_ids = []

        # Validate keys.
        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(req_data, key, srv_req_data)

        mg_ids, q_ids = select_existing_ids(data_dict)

        if len(mg_ids) == 0:
            print("EMPTY: len(mg_ids) == 0")
            answer = prepare_answer([], [])
            return answer

        offer_paths = select_offers_paths(q_ids)

        # leave only those message_group_id's, for which offers exist
        print("Creating handled_mg_ids")
        new_mg_ids = []
        for mg_id, q_id in zip(mg_ids, q_ids):
            if q_id in offer_paths:
                new_mg_ids.append(mg_id)
        handled_mg_ids = new_mg_ids
        mg_ids = new_mg_ids
        q_ids = list(offer_paths.keys())

        if len(handled_mg_ids) == 0:
            print("EMPTY: len(handled_mg_ids) == 0")
            answer = prepare_answer([], [])
            return answer

        print("Start cycle")
        for mg_id, q_id in zip(mg_ids, q_ids):
            messages, customers = select_messages(mg_id, req_data, srv_req_data)
            print("Extract offer path")
            offer_path = offer_paths[q_id]
            file_status = save_mapping_file(
                messages,
                customers,
                offer_path,
                mg_id,
            )
            if file_status == FileStatus.MESSAGES_FILE_EXIST:
                file_exist_mg_ids.append(mg_id)
            elif file_status == FileStatus.OFFER_FILE_NOT_EXIST:
                offer_file_not_exist_mg_ids.append(mg_id)

        answer = prepare_answer(
            handled_mg_ids,
            file_exist_mg_ids,
            offer_file_not_exist_mg_ids,
        )
        return answer


################################################################################

# Helpers

def select_existing_ids(data_dict) -> (list[MessageGroupId], list[QueryId]):
    print("Start select_existing_ids")
    print("Make query")
    result_set = QueryCRUD.select_all(
        columns=[
            Query.query_id,
            Query.message_group_id,
        ],
        wheres_cond=[
            Query.message_group_id >= data_dict["message_group_id_begin"],
            Query.message_group_id < data_dict["message_group_id_end"],
        ],
        order_bys=[
            asc(Query.message_date),
            desc(Query.message_date),  # to get query_id that matches with offer
        ]
    )
    print_result_set(result_set)

    if result_set is None:
        return [], []

    print("Collecting result_set")
    mg_ids = []
    q_ids = []
    prev = None
    for row in result_set:
        if prev != row.message_group_id:
            prev = row.message_group_id
            mg_ids.append(prev)
            q_ids.append(row.query_id)

    return mg_ids, q_ids


def select_offers_paths(q_ids: list[QueryId]) -> dict[QueryId, FilePath]:
    print("Starting select_offers_paths")
    print("Make query")
    result_set = OfferCRUD.select_all(
        columns=[
            Offer.query_id,
            Offer.file_path,
        ],
        wheres_cond=[
            Offer.query_id.in_(q_ids),
        ],
    )
    print_result_set(result_set)

    if result_set is None:
        return {}

    print("Collecting result_set")
    res = {}
    for row in result_set:
        res[row.query_id] = row.file_path
    return res


def select_messages(
        mg_id: MessageGroupId,
        req_data,
        srv_req_data,
) -> (list[Text], list[CustomerId]):
    print("Starting select_messages")
    print("Make query")
    result_set = QueryCRUD.select_all(
        columns=[
            Query.customer_id,
            Query.message,
        ],
        wheres_cond=[
            Query.message_group_id == mg_id,
        ],
        order_bys=[
            asc(Query.message_date),
        ],
    )
    print_result_set(result_set)

    if result_set is None:
        description = inspect.cleandoc(
            f"""
            Unexpected error: no such message_group_id in table, but MUST be.
            message_group_id: {mg_id}
            """
        )
        runtime_error_wrapper(description, req_data, srv_req_data)

    print("Collecting result_set")
    msg_list = []
    customer_list = []
    for row in result_set:
        msg_list.append(row.message)
        customer_list.append(row.customer_id)

    return msg_list, customer_list


def save_mapping_file(
        messages: list[Text],
        customers: list[CustomerId],
        offer_path: FilePath,
        mg_id: MessageGroupId,
        overwrite: bool = False,
) -> FileStatus:
    print("Starting save_mapping_file")
    dir_inside_volume = os.path.dirname(offer_path)
    dump_file_path = (f"{app_cfg.GENERATED_OFFERS_VOLUME_PATH}/"
                      f"{dir_inside_volume}/"
                      f"{mg_id}_messages.json")
    print(f"dir_inside_volume: {dir_inside_volume}")
    print(f"dump_file_path: {dump_file_path}")
    if os.path.exists(dump_file_path):
        # file was already generated (maybe by previous calls to
        # map_offers_to_messages), we don't have to make it again,
        # because it will have the same content
        print("file exist")
        if not overwrite:
            print("overwriting file")
            return FileStatus.MESSAGES_FILE_EXIST

    docker_offer_path = (f"{app_cfg.GENERATED_OFFERS_VOLUME_PATH}/"
                         f"{offer_path}")
    if not os.path.exists(docker_offer_path):
        # file with generated offer was removed
        # we will not generate json in that case
        print("file of offer does not exist, messages won't be saved")
        print(f"docker_offer_path: {docker_offer_path}")
        return FileStatus.OFFER_FILE_NOT_EXIST

    dump_file_dir = os.path.dirname(dump_file_path)
    if not os.path.exists(dump_file_dir):
        description = inspect.cleandoc(
            f"""
            Warning: directory with corporate offer for\
            message_group_id={mg_id} does not exist.
            Creating directory manually.
            """
        )
        print(description)
        os.makedirs(dump_file_dir, exist_ok=True)

    print("dump to file and save it")
    dump_obj = {
        "offer_file": offer_path,
        "customer_ids": customers,
        "messages": messages,
    }

    with open(dump_file_path, "w") as f:
        json.dump(dump_obj, f, ensure_ascii=False, indent=2)
    print("dump finished")

    return FileStatus.MESSAGES_FILE_SAVED


def prepare_answer(
        handled_message_group_ids: list[MessageGroupId],
        file_exist_message_group_ids: list[MessageGroupId],
        offer_file_not_exist_mg_ids: list[MessageGroupId],
) -> dict:
    print("Preparing answer")
    answer = {
        "handled_message_group_ids": handled_message_group_ids,
        "file_exist_message_group_ids": file_exist_message_group_ids,
        "offer_file_not_exist_message_group_ids": offer_file_not_exist_mg_ids,
    }
    return answer
