from abc import ABCMeta, abstractmethod

from ..data import Data
from ..models import BaseModel
from ..config import Configuration

class BaseLearner(metaclass=ABCMeta):

    def __init__(self, config: Configuration):
        self.config = config

    @abstractmethod
    def train(self, model: BaseModel, train_data: Data, *args, **kwargs):
        pass

    @abstractmethod
    def test(self, model: BaseModel, test_data: Data, *args, **kwargs):
        pass