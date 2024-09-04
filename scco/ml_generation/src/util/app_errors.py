import inspect
import json
import sys


def str_query_content(invalid_part, srv_req_data) -> str:
    return inspect.cleandoc(
        f"""
invalid part: {json.dumps(invalid_part, indent=2)}
service query content: {json.dumps(srv_req_data, indent=2)}
"""
    )


def str_error(description: str, invalid_part, srv_req_data) -> str:
    return inspect.cleandoc(
        f"""
[ERROR] {description}
{str_query_content(invalid_part, srv_req_data)}
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    )


def runtime_error_wrapper(
        description: str,
        invalid_part,
        srv_req_data,
) -> None:
    raise RuntimeError(str_error(description, invalid_part, srv_req_data))


def logger_wrapper(
        description: str,
        invalid_part,
        srv_req_data,
) -> None:
    print(str_error(description, invalid_part, srv_req_data), file=sys.stderr)


################################################################################

def dict_has_or_panic(
        json_dict,
        key: str,
        srv_req_data: any = "not passed") -> None:
    if key not in json_dict:
        runtime_error_wrapper(
            f"missing '{key}'",
            json_dict,
            srv_req_data,
        )


def dict_get_or_panic(
        json_dict,
        key: str,
        srv_query_data: any = "not passed") -> any:
    dict_has_or_panic(json_dict, key, srv_query_data)
    return json_dict[key]


def check_req_data_is_array(req_data, srv_req_data) -> bool:
    if not isinstance(req_data, list):
        logger_wrapper(
            "invalid json format: 'request_data' must be a json array",
            req_data,
            srv_req_data,
        )
        return False
    return True


def check_req_data_array_empty(req_data, srv_req_data) -> bool:
    if len(req_data) == 0:
        logger_wrapper(
            "invalid json format: 'request_data' is empty",
            req_data,
            srv_req_data,
        )
        return True
    return False
