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


def try_cast(obj, t) -> (bool, any):
    try:
        res = t(obj)
        return True, res
    except ValueError:
        return False, None


def force_cast(obj, t) -> any:
    try:
        res = t(obj)
        return res
    except ValueError:
        raise RuntimeError("Can't cast {} to {}".format(t, type(obj)))


def assert_cast(obj, t, error_msg: str) -> any:
    try:
        res = t(obj)
        return res
    except ValueError:
        description = inspect.cleandoc(
            f"""
            Cast failed: unable to cast {type(obj)} to {t}
            {error_msg}
            """
        )
        runtime_error_wrapper(description, "not passed", "not passed")


def get_correctly_typed_dict(required_keys_type_map: dict, data) -> dict:
    res_dict = {}
    for key, t in required_keys_type_map.items():
        data_val = dict_get_or_panic(data, key)
        ok, new_val = try_cast(data_val, t)
        if not ok:
            description = inspect.cleandoc(
                f"""
                Passed types mismatched: unable to cast {type(data_val)} to {t}
                required_keys: '{required_keys_type_map}'
                """
            )
            runtime_error_wrapper(description, "not passed", "not_passed")
        res_dict[key] = new_val
    return res_dict


def get_correctly_typed_dicts(required_keys_type_map: dict, data) -> list[dict]:
    res_dicts = []
    for elem in data:
        res_dict = get_correctly_typed_dict(required_keys_type_map, elem)
        res_dicts.append(res_dict)
    return res_dicts


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


def check_is_array(req_data, srv_req_data, arr_name="request_data") -> bool:
    if not isinstance(req_data, list):
        logger_wrapper(
            f"invalid json format: '{arr_name}' must be a json array",
            req_data,
            srv_req_data,
        )
        return False
    return True


def check_array_empty(req_data, srv_req_data, arr_name="request_data") -> bool:
    if len(req_data) == 0:
        logger_wrapper(
            f"invalid json format: '{arr_name}' is empty",
            req_data,
            srv_req_data,
        )
        return True
    return False


def check_not_empty_array(
        req_data,
        srv_req_data,
        arr_name="request_data",
) -> bool:
    return check_is_array(req_data, srv_req_data, arr_name) \
        and not check_array_empty(req_data, srv_req_data, arr_name)
