def remove_reply_fields(exp_answer: dict | None) -> dict | None:
    if exp_answer is None:
        return None
    if 'reply_ctx' in exp_answer:
        del exp_answer['reply_ctx']
    return exp_answer
