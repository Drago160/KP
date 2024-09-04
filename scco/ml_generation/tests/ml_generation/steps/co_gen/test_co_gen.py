import pytest

import json
from pathlib import Path

from ml_generation.steps.co_gen import CoGen

from .fake_objects import CoGenTestMethod
from .fake_objects import CoGenTestChannel
from .fake_objects import CoGenTestBroker
from .fake_objects import CoGenTestMlModel

################################################################################

# Testing data.

# dumps(load()) is required to test that data files are correct
# json files

SRC_FILE_DIR = Path(__file__).resolve().parent

with open(SRC_FILE_DIR / "data" / "simple_input_data.json", "r") as f:
    simple_input_data = json.dumps(json.load(f)).encode("utf-8")
with open(SRC_FILE_DIR / "data" / "simple_pdf_gen_pub.json", "r") as f:
    simple_pdf_gen_pub = json.load(f)

################################################################################


@pytest.mark.parametrize("input_data, pdf_gen_pub", [
    (simple_input_data, simple_pdf_gen_pub),
])
def test_co_gen(input_data, pdf_gen_pub):
    # Setting up
    fake_ml_model = CoGenTestMlModel()
    fake_method = CoGenTestMethod()
    fake_ch = CoGenTestChannel()
    fake_broker = CoGenTestBroker(pdf_gen_pub)  # here are asserts

    # Creating object
    co_gen = CoGen(fake_broker, fake_ml_model)

    # Testing
    co_gen.callback(fake_ch, fake_method, None, input_data)
