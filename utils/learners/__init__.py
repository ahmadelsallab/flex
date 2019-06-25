from abc import ABCMeta, abstractmethod

from mlfmwk.utils.data.base_datastruct import Data
from mlfmwk.utils.models.base_model import BaseModel


class BaseLearner(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def train(self, model: BaseModel, train_data: Data, *args, **kwargs):
        pass

    @abstractmethod
    def test(self, model: BaseModel, test_data: Data, *args, **kwargs):
        pass