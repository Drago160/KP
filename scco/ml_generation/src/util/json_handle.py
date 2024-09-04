import inspect  # cleandoc
import textwrap  # dedent
import json


def dict_has_or_panic(json_dict, key: str, db_query: any = "not passed") -> None:
    if key not in json_dict:
        raise RuntimeError(
            inspect.cleandoc(f"""
Missing "{key}".
db_query content: {json.dumps(db_query, indent=2)}
json_dict content: {json.dumps(json_dict, indent=2)}
            """)
        )


def dict_get_or_panic(json_dict, key: str, srv_query_data: any = "not passed") -> any:
    dict_has_or_panic(json_dict, key, srv_query_data)
    return json_dict[key]
