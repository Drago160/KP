from util.app_errors import get_correctly_typed_dict

from crud.objects.new_queries_csv import NewQueriesCsvCRUD
import crud.type_map as type_map

from service.request_cb.request_cb import RequestCallback


class InsertNewQueriesCsv(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter InsertNewQueriesCsv callback")

        # Check keys.
        required_keys_type_map = {
            "csv_path": type_map.FilePath,
        }
        req_dict = get_correctly_typed_dict(
            required_keys_type_map=required_keys_type_map,
            data=req_data,
        )

        # Make db query.
        print("Start query")
        NewQueriesCsvCRUD.insert_one(
            {
                "csv_path": req_dict["csv_path"],
            }
        )

        print("Preparing answer")
        answer = {
            "csv_path": req_dict["csv_path"],
        }
        return answer
