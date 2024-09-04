request_simple = {
    "request_name": "map_offers_to_messages",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_routing_key"
    },
    "reply_ctx": "something",  # not required
    "request_data": {
        "message_group_id_begin": 1,
        "message_group_id_end": 5,
        "overwrite": True
    }
}

################################################################################

answer_simple = {
  "handled_message_group_ids": [
    1
  ],
  "file_exist_message_group_ids": [
    1
  ],
  "reply_ctx": "something"
}

################################################################################
