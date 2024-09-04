from typing import Annotated
from typing import get_type_hints
from typing import get_args

from sqlalchemy import Text

import json

################################################################################

# import concurrent.futures
#
#
# def worker():
#     print("Worker thread running")
#
#
# pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
#
# pool.submit(worker)
# pool.submit(worker)
#
# pool.shutdown(wait=True)
#
# print("Main thread continuing to run")

################################################################################

import datetime

print(f"{datetime.datetime.now():%Y-%m-%dT%H:%M:%S}")

print(
    datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
)
