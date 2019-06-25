from mlfmwk.utils.models import BaseModel

class MyModel(BaseModel):
    def __init__(self, config):
        super().__init__(config=config)

    def build(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    def predict(self, data, *args, **kwargs):
        pass