from abc import ABC
from abc import abstractmethod


class MlModel(ABC):
    @abstractmethod
    def generate(self, data):
        raise NotImplementedError("Pure virtual method")


def wrap_ml_model(ml_model) -> MlModel:
    return ml_model
