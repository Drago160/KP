import pytest
from pytest_mock import MockerFixture
from typing import NamedTuple

from service.dispatcher import extract_basic_data
import crud.type_map as type_map
from testing.util import remove_reply_fields
import util.app_config as app_cfg

from service.request_cb.data_preproc.insert_new_queries_csv import (
    InsertNewQueriesCsv,
)

################################################################################

# Testing data.

from service.data.data_preproc.insert_new_queries_csv import (
    request_simple, answer_simple,
)


# Emulating `sqlalchemy.engine.row.Row`
class FakeDbAnswer(NamedTuple):
    csv_path: type_map.FilePath


db_insert_data = {
    "csv_path": "path/to/new_queries1.csv",
}

fake_db_answer = [
    FakeDbAnswer(
        csv_path='path/to/new_queries1.csv',
    )
]

################################################################################


class TestInsertNewQueriesCsv:
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
            "crud.objects.new_queries_csv.NewQueriesCsvCRUD.insert_one",
        )
        req_data, reply, _ = extract_basic_data(srv_req_data)

        # Make callback
        cb_obj = InsertNewQueriesCsv()
        act_answer = cb_obj.make_call(req_data, srv_req_data)

        # Check
        crud_patcher.assert_called_once_with(db_insert_data)
        assert exp_answer == act_answer
