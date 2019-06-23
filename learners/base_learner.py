from abc import ABCMeta, abstractmethod
from mlfmwk.models.base_model import BaseModel
from mlfmwk.data.base_datastruct import Data

class BaseLearner(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def train(self, model: BaseModel, train_data: Data, *args, **kwargs):
        pass

    @abstractmethod
    def test(self, model: BaseModel, test_data: Data, *args, **kwargs):
        pass