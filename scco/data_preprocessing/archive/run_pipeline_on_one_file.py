import json
import os
import pandas as pd

from pipeline import PreprocessingPipeline


def main():
    in_file = '../../tests/data/it/all_freelance/Messages_Request_From_2024_04_29 (3).csv'
    out_file = 'out.txt'
    json_in = {
        "customer_id": "0", "parsed_csv":
        "file://" + os.path.join(os.getcwd(), in_file)
    }
    print(f" [x] Received json {json_in}", flush=True)

    try:
        data = pd.read_csv(json_in['parsed_csv'])
        data.columns = ['channel_id', 'client_id', 'message', 'message_date']
        customer_id = json_in['customer_id']
    except Exception as e:
        print(" [x] Caught the following exception when parsing input:")
        print(e)
        return

    pipeline = PreprocessingPipeline(customer_id=customer_id)
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
