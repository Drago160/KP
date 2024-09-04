import json
import os
import pandas as pd

from pipeline import PreprocessingPipeline
from rabbit_rpc import FilterRpcClient, SaveCsvRpcClient, MatchingListsRpcClient, InsertToDbRpcClient
import config

config.DEBUG_ISOLATED = True


def main():
    rpc_connection = None
    rpc_channel = None

    filter_rpc_client = FilterRpcClient(rpc_connection, rpc_channel)
    new_queries_csv_info = {'path': None}

    save_csv_rpc_client = SaveCsvRpcClient(rpc_connection, rpc_channel, new_queries_csv_info)
    matching_lists_rpc_client = MatchingListsRpcClient(rpc_connection, rpc_channel, new_queries_csv_info)
    insert_to_db_rpc_client = InsertToDbRpcClient(rpc_connection, rpc_channel, new_queries_csv_info)

    in_file = 'it/outstaffing_409'
    out_file = 'out.txt'
    json_in = {"customer_id": "0", "parsed_csv": in_file}
    print(f" [x] Received json {json_in}", flush=True)

    try:
        customer_id = str(json_in['customer_id'])
        csv_name = json_in['parsed_csv']
        data = pd.read_csv(os.path.join(config.PARSER_BOT_CSV_FOLDER, csv_name), dtype=str)

    except Exception as e:
        print(" [x] Caught the following exception when parsing input:")
        print(e)
        return

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
    data = pipeline(data)
    if data.empty:
        return

    print(f" [x] Saving {len(data)} messages to file {out_file}")
    with open(out_file, 'w') as f:
        for index, row in data.iterrows():
            json_str = json.dumps({col: str(row[col]) for col in data.columns}, ensure_ascii=False)
            print(json_str, file=f)
    print(" [x] Done", flush=True)


if __name__ == '__main__':
    main()
