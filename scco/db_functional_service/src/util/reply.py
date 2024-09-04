from broker.broker import Publisher
from util.app_errors import dict_get_or_panic


class Reply:
    def __init__(self, srv_req_data: dict):
        if "reply" not in srv_req_data:
            self._is_required = False
            return
        else:
            self._is_required = True

        reply = srv_req_data["reply"]
        self._exchange = dict_get_or_panic(reply, "exchange", srv_req_data)
        self._routing_key = dict_get_or_panic(reply, "routing_key", srv_req_data)

    def is_required(self) -> bool:
        return self._is_required

    def get_publisher(self) -> Publisher:
        return Publisher(
            name="",  # not used
            exchange=self._exchange,
            queue="",  # not used
            routing_key=self._routing_key,
        )


def add_reply_ctx(srv_query_data, answer):
    if "reply_ctx" in srv_query_data:
        answer["reply_ctx"] = srv_query_data["reply_ctx"]
