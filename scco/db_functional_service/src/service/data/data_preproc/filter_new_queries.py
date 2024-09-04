request_simple = {
    "request_name": "filter_new_queries",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
        {
            "customer_id": "customer_1",
            "client_id": "client_1",
            "channel_id": "phystech.career",
            "message_date": "2024-01-01T00:00:00",
        },
        {
            "customer_id": "customer_1",
            "client_id": "client_2",
            "channel_id": "phystech.career",
            "message_date": "2023-12-31T23:59:00",
        }
    ]
}

#################

answer_simple = {
  "not_exist": [
    {
      "customer_id": "customer_1",
      "client_id": "client_1",
      "channel_id": "phystech.career",
      "message_date": "2024-01-01T00:00:00"
    }
  ],
  "reply_ctx": "something"
}

################################################################################

request_custom_datetime = {
    "request_name": "filter_new_queries",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
        {
            "customer_id": "customer_1",
            "client_id": "client_1",
            "channel_id": "phystech.career",
            "message_date": "2024-01-01",  # another data format
        },
        {
            "customer_id": "customer_1",
            "client_id": "client_2",
            "channel_id": "phystech.career",
            "message_date": "2023-12-31T23:59:00",
        }
    ]
}

#################

answer_custom_datetime = {
  "not_exist": [
    {
      "customer_id": "customer_1",
      "client_id": "client_1",
      "channel_id": "phystech.career",
      "message_date": "2024-01-01"
    }
  ],
  "reply_ctx": "something"
}

################################################################################

request_cast_type = {
    "request_name": "filter_new_queries",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
        {
            "customer_id": "customer_1",
            "client_id": "client_1",
            "channel_id": 128,  # number must be cast to string
            "message_date": "2024-01-01T00:00:00",
        },
        {
            "customer_id": "customer_1",
            "client_id": 60,  # number must be cast to string
            "channel_id": "phystech.career",
            "message_date": "2023-12-31T23:59:00",
        }
    ]
}

#################

answer_cast_type = {}