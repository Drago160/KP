import re
from emoji import replace_emoji


def remove_hashtags(s: str):
    return s.replace('#', '')


def remove_emoji(s: str):
    return replace_emoji(s, '')


def remove_hashtags_entirely(s: str):
    return re.sub(r"#(\w{1,50})", '', s)


def remove_at_mentions(s: str):
    return re.sub(r"@([a-zA-Z0-9_]{1,50})", '', s)
