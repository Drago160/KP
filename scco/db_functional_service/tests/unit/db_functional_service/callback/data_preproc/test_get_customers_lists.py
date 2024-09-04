import pytest
from pytest_mock import MockerFixture
from typing import NamedTuple

from service.dispatcher import extract_basic_data
import crud.type_map as type_map
from testing.util import remove_reply_fields
import util.app_config as app_cfg

from service.request_cb.data_preproc.get_customers_lists import (
    GetCustomersLists,
)

################################################################################

# Testing data.

from service.data.data_preproc.get_customers_lists import (
    request_simple, answer_simple,
)


# Emulating `sqlalchemy.engine.row.Row`
class FakeDbAnswer(NamedTuple):
    customer_id: type_map.ClientId
    black_list: type_map.CustomerBlackList
    white_list: type_map.CustomerWhiteList


fake_db_answer = [
    FakeDbAnswer(
        customer_id='customer_1',
        black_list=[
            "php",
            "wordpress",
            "c#"
        ],
        white_list=[
            "frontend",
            "вёрстка",
            "javascript",
            "веб-сайт"
        ]
    ),
    FakeDbAnswer(
        customer_id='customer_2',
        black_list=[
            "отделка",
            "кровля"
        ],
        white_list=[
            "электрика",
            "сантехника"
        ]
    ),
]

################################################################################


class TestGetCustomersLists:
    @pytest.mark.parametrize(
        "srv_req_data, exp_answer", [
            (request_simple, answer_simple),
        ]
    )
    def test_different_requests(
            self,
            mocker: MockerFixture,
            srv_req_data,
            exp_answer,
    ) -> None:
        # Prepare data
        exp_answer = remove_reply_fields(exp_answer)
        crud_patcher = mocker.patch(
            "crud.objects.customer.CustomerCRUD.select_all",
            return_value=fake_db_answer,
        )
        req_data, reply, _ = extract_basic_data(srv_req_data)

        # Make callback
        cb_obj = GetCustomersLists()
        act_answer = cb_obj.make_call(req_data, srv_req_data)

        # Check
        crud_patcher.assert_called_once()
        assert exp_answer == act_answer
