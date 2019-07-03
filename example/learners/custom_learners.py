from flex.flex.learners import BaseLearner
from flex.flex.models import BaseModel
from flex.flex.data import Data

class MyLearner(BaseLearner):
    def __init__(self, config):
        super().__init__(config=config)

    def train(self, model: BaseModel, train_data: Data, *args, **kwargs):
        pass

    def test(self, model: BaseModel, test_data: Data, *args, **kwargs):
        pass