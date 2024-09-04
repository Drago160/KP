from typing import Callable


def wrap_step_callback(step_obj) -> Callable:
    res = lambda ch, method, props, body: step_obj.callback(
        ch,
        method,
        props,
        body
    )
    print("Returning value")
    return res
