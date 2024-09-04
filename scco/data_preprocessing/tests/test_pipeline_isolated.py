import unittest
import os
import pandas as pd

from pipeline import PreprocessingPipeline
from rabbit_rpc import FilterRpcClient, SaveCsvRpcClient, MatchingListsRpcClient, InsertToDbRpcClient
import config


def run_pipeline_isolated():
    rpc_connection = None
    rpc_channel = None

    filter_rpc_client = FilterRpcClient(rpc_connection, rpc_channel)
    new_queries_csv_info = {'path': None}

    save_csv_rpc_client = SaveCsvRpcClient(rpc_connection, rpc_channel, new_queries_csv_info)
    matching_lists_rpc_client = MatchingListsRpcClient(rpc_connection, rpc_channel, new_queries_csv_info)
    insert_to_db_rpc_client = InsertToDbRpcClient(rpc_connection, rpc_channel, new_queries_csv_info)

    json_in = {"customer_id": "0", "parsed_csv": 'it/outstaffing_409'}

    customer_id = str(json_in['customer_id'])
    csv_name = json_in['parsed_csv']
    data = pd.read_csv(os.path.join(config.PARSER_BOT_CSV_FOLDER, csv_name), dtype=str)

    assert ','.join(data.columns).lower() == "channel_name,sender_id,message,message_date"
    data.columns = ['channel_id', 'client_id', 'message', 'message_date']

    pipeline = PreprocessingPipeline(
        customer_id,
        csv_name,
        new_queries_csv_info,
        filter_rpc_client,
        save_csv_rpc_client,
        matching_lists_rpc_client,
        insert_to_db_rpc_client,
    )

    return pipeline(data)


class TestPipelineIsolated(unittest.TestCase):
    def test_pipeline_runs_isolated(self):
        config.DEBUG_ISOLATED = True
        result = run_pipeline_isolated()
        self.assertFalse(result.empty)
        config.DEBUG_ISOLATED = False
