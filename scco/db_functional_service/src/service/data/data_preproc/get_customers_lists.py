request_simple = {
    "request_name": "get_customers_lists",
    "reply": {
        "exchange": "scco_test_exchange",
        "routing_key": "scco_test_rk",
    },
    "reply_ctx": "something",  # not required
    "request_data": [
        {
            "customer_id": "customer_1",
        },
        {
            "customer_id": "customer_2",
        }
    ]
}

################################################################################

answer_simple = {
  "array_data": [
    {
      "customer_id": "customer_1",
      "black_list": [
        "php",
        "wordpress",
        "c#"
      ],
      "white_list": [
        "frontend",
        "вёрстка",
        "javascript",
        "веб-сайт"
      ]
    },
    {
      "customer_id": "customer_2",
      "black_list": [
        "отделка",
        "кровля"
      ],
      "white_list": [
        "электрика",
        "сантехника"
      ]
    }
  ],
  "reply_ctx": "something"
}
