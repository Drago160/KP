request_simple = {
    "request_name": "insert_preprocessed_queries",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": {
        "csv_path": "path/to/new_queries1.csv",
        "array_data": [
            {
                "customer_id": "customer_1",
                "client_id": "client_3",
                "channel_ids": [
                    "phystech.career",
                    "yandex.career",
                ],
                "messages": [
                    "Text of message 1, client_3",
                    "Text of message 2, client_3",
                ],
                "message_dates": [
                    "2024-01-01T00:31:00",
                    "2024-01-01T00:32:00"
                ],
            },
            {
                "customer_id": "customer_2",
                "client_id": "client_4",
                "channel_ids": [
                    "linkedin",
                    "headhunter",
                    "linkedin",
                ],
                "messages": [
                    "Text of message 1, client 4",
                    "Text of message 2, client 4",
                    "Text of message 3, client 4",
                ],
                "message_dates": [
                    "2024-01-01T00:41:00",
                    "2024-01-01T00:42:00",
                    "2024-01-01T00:43:00",
                ],
            },
            {
                "customer_id": "customer_2",
                "client_id": "client_5",
                "channel_ids": [
                    "phystech.career",
                ],
                "messages": [
                    "Text of message 1, client 5",
                ],
                "message_dates": [
                    "2024-01-01T00:51:00",
                ],
            },
        ]
    }
}

################################################################################

answer_simple = {
  "array_data": [
    3,
    4,
    5
  ],
  "reply_ctx": "something"
}
