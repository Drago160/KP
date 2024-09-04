from abc import abstractmethod


class RequestCallback:
    @abstractmethod
    def make_call(
            self,
            req_data,
            srv_req_data,
    ) -> any:
        raise NotImplementedError("Pure virtual method")


def print_result_set(result_set) -> None:
    print(f"-----------------------------")
    print(f"result_set:\n{result_set}")
    print(f"-----------------------------")
