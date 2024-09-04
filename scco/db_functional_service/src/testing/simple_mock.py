def inner_function():
    return 42


def outer_function():
    res = inner_function()
    return res
