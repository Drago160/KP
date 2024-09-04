import pytest

import json
from pathlib import Path

from ml_generation.steps.preproc import Preproc

from .fake_objects import PreprocTestMethod
from .fake_objects import PreprocTestChannel
from .fake_objects import PreprocTestBroker

from .data.simple_db_pub import json_data as simple_db_pub

################################################################################

# Testing data.

# dumps(load()) is required to test that data files are correct
# json files

SRC_FILE_DIR = Path(__file__).resolve().parent

with open(SRC_FILE_DIR / "data" / "simple_input_data.json", "r") as f:
    simple_input_data = json.dumps(json.load(f)).encode("utf-8")

################################################################################


@pytest.mark.parametrize("input_data, db_pub", [
    (simple_input_data, simple_db_pub),
])
def test_preproc(input_data, db_pub):
    # Setting up
    fake_method = PreprocTestMethod()
    fake_ch = PreprocTestChannel()
    fake_broker = PreprocTestBroker(db_pub)  # here are asserts

    # Creating object
    preproc = Preproc(fake_broker)

    # Testing
    preproc.callback(fake_ch, fake_method, None, input_data)
