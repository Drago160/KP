request_simple = {
    "request_name": "insert_offers",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_routing_key",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
        {
            "message_group_id": 2,
            "file_path": "/path/to/inserted_offer_2.pdf",
        },
    ]
}

################################################################################

answer_simple = {
  "array_data": [
    {
      "customer_id": "customer_1",
      "client_id": "client_2",
      "file_path": "/path/to/inserted_offer_2.pdf"
    }
  ],
  "reply_ctx": "something"
}

