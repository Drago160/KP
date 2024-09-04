from util.app_errors import get_correctly_typed_dicts
from util.app_errors import check_not_empty_array

from crud.models import Customer
from crud.objects.customer import CustomerCRUD
import crud.type_map as type_map

from service.request_cb.request_cb import RequestCallback


class GetCustomersLists(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter GetCustomersLists callback")

        # Validate req_data to be array
        if not check_not_empty_array(req_data, srv_req_data):
            print("Exit without sending answer")
            return

        # Validate keys.
        required_keys_type_map = {
            "customer_id": type_map.CustomerId,
        }
        req_dict = get_correctly_typed_dicts(
            required_keys_type_map=required_keys_type_map,
            data=req_data,
        )

        customer_ids = []
        for elem in req_dict:
            customer_ids.append(elem["customer_id"])

        # Make db query.
        print("Start query")
        result_set = CustomerCRUD.select_all(
            [
                Customer.customer_id,
                Customer.black_list,
                Customer.white_list,
            ],
            wheres_cond=[
                Customer.customer_id.in_(customer_ids),
            ],
        )

        print("Collecting data")
        answer_list = []
        for row in result_set:
            answer_list.append(
                {
                    "customer_id": row[0],
                    "black_list": row[1],
                    "white_list": row[2],
                }
            )

        print("Preparing answer")
        answer = {
            "array_data": answer_list,
        }
        return answer
