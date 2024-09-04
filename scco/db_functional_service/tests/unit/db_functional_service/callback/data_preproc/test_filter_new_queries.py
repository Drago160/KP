import pytest
from pytest_mock import MockerFixture
from typing import NamedTuple

import datetime

from service.dispatcher import extract_basic_data
import crud.type_map as type_map
from testing.util import remove_reply_fields
import util.app_config as app_cfg

from service.request_cb.data_preproc.filter_new_queries import (
    FilterNewQueries,
)

################################################################################

# Testing data.

from service.data.data_preproc.filter_new_queries import (
    request_simple, answer_simple,
)


# Emulating `sqlalchemy.engine.row.Row`
class FakeDbAnswer(NamedTuple):
    customer_id: type_map.ClientId
    client_id: type_map.ClientId
    channel_id: type_map.ChannelId
    message_date: type_map.MessageDatetime


fake_db_answer = [
    FakeDbAnswer(
        customer_id='customer_1',
        client_id='client_2',
        channel_id='phystech.career',
        message_date=datetime.datetime.strptime(
                "2023-12-31T23:59:00",
                app_cfg.DATETIME_FORMAT
        ),
    )
]

################################################################################


class TestFilterNewQueries:
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
            "crud.objects.query.QueryCRUD.select_all",
            return_value=fake_db_answer,
        )
        req_data, reply, _ = extract_basic_data(srv_req_data)

        # Make callback
        cb_obj = FilterNewQueries()
        act_answer = cb_obj.make_call(req_data, srv_req_data)

        # Check
        crud_patcher.assert_called_once()
        assert exp_answer == act_answer
