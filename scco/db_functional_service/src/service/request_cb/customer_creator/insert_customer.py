from util.app_errors import dict_get_or_panic
from util.app_errors import get_correctly_typed_dict

from crud.objects.customer_service import CustomerServiceCRUD
from crud.objects.customer import CustomerCRUD
from crud.models import Customer
from crud.models import CustomerService
import crud.type_map as type_map

from service.request_cb.request_cb import RequestCallback


class InsertCustomer(RequestCallback):
    def __init__(self):
        super().__init__()

    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        print("Enter InsertCustomer callback")

        # Check keys.
        required_keys_type_map = {
            "customer_id": type_map.CustomerId,
            "contact_info": type_map.Text,
            "company_name": type_map.Text,
            "black_list": list[type_map.Text],
            "tags": list[type_map.Text],
            "white_list": list[type_map.Text],
            "specific_features": list[type_map.Text],
            "services": list[dict],
        }
        req_dict = get_correctly_typed_dict(
            required_keys_type_map=required_keys_type_map,
            data=req_data,
        )

        # Check for customer to exist.
        result_one = CustomerCRUD.select_one(
            columns=[
                Customer.customer_id
            ],
            wheres_cond=[
                Customer.customer_id == req_dict["customer_id"],
            ]
        )

        if result_one is not None:
            # Customer already exists, updating him.
            print("Updating customer")
            CustomerCRUD.update(
                new_vals={
                    "contact_info": req_dict["contact_info"],
                    "company_name": req_dict["company_name"],
                    "black_list": req_dict["black_list"],
                    "tags": req_dict["tags"],
                    "white_list": req_dict["white_list"],
                    "specific_features": req_dict["specific_features"],
                },
                wheres_cond=[
                    Customer.customer_id == req_dict["customer_id"],
                ],
            )
            print("Finished updating customer")

            # Updating customer services.
            print("Deleting previous customer services")
            CustomerServiceCRUD.delete(
                wheres_cond=[
                    CustomerService.customer_id == req_dict["customer_id"],
                ],
            )
            print("Finished deleting previous customer services")

            for service in req_dict["services"]:
                service["customer_id"] = req_dict["customer_id"]

            print("Inserting new customer services")
            CustomerServiceCRUD.insert_all(req_dict["services"])
            print("Finished inserting customer services")

        else:
            # Customer not found, here is the new one.
            print("Inserting customer")
            CustomerCRUD.insert_one(
                {
                    "customer_id": req_dict["customer_id"],
                    "contact_info": req_dict["contact_info"],
                    "company_name": req_dict["company_name"],
                    "black_list": req_dict["black_list"],
                    "tags": req_dict["tags"],
                    "white_list": req_dict["white_list"],
                    "specific_features": req_dict["specific_features"],
                }
            )
            print("Finished inserting customer")

            # Insert customer services.
            print("Inserting customer services")
            for service in req_dict["services"]:
                service["customer_id"] = req_dict["customer_id"]

            CustomerServiceCRUD.insert_all(req_dict["services"])
            print("Finish insert customer services")
