import util.app_config as app_cfg

json_data = {
    "request_name": "get_info_for_co_generation",
    "reply": {
        "exchange": app_cfg.CO_GEN_EXCHANGE,
        "routing_key": app_cfg.CO_GEN_ROUTING_KEY
    },
    "reply_ctx": 1,
    "request_data": {
        "message_group_id": 1
    }
}
