import os

import util.parse_env as pe

################################################################################
# Global setup.

RMQ_NET_ALIAS = pe.get_or_default(
    "RMQ_NET_ALIAS",
    "env variable not found"
)

DB_FUNCTIONAL_SERVICE_EXCHANGE = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_EXCHANGE",
    "env variable not found",
)
DB_FUNCTIONAL_SERVICE_QUEUE = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_QUEUE",
    "env variable not found"
)
DB_FUNCTIONAL_SERVICE_ROUTING_KEY = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_ROUTING_KEY",
    "env variable not found"
)

POSTGRES_FS_ALIAS = pe.get_or_default(
    "POSTGRES_FS_ALIAS",
    "env variable not found"
)

GENERATED_OFFERS_VOLUME_PATH = pe.get_or_default(
    "GENERATED_OFFERS_VOLUME_PATH",
    f"{os.getcwd()}/tmp"
)
if os.path.basename(GENERATED_OFFERS_VOLUME_PATH) == "tmp":
    os.makedirs(GENERATED_OFFERS_VOLUME_PATH, exist_ok=True)

################################################################################
# Local setup.

POSTGRES_USER = pe.get_or_default(
    "POSTGRES_USER",
    "env variable not found"
)
POSTGRES_PASSWORD = pe.get_or_default(
    "POSTGRES_PASSWORD",
    "env variable not found"
)
POSTGRES_PORT = pe.get_or_default(
    "POSTGRES_PORT",
    "env variable not found"
)
POSTGRES_DB = pe.get_or_default(
    "POSTGRES_DB",
    "env variable not found"
)

_IS_ON_HOST_BOOL = pe.contains("IS_ON_HOST")


def is_on_host() -> bool:
    return _IS_ON_HOST_BOOL


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
