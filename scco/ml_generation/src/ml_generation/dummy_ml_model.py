from ml_generation.ml_model import MlModel


class DummyMlModel(MlModel):
    def generate(self, data):
        gen_data = {
            "main_text": "some_useful_text"
        }
        return gen_data
