from abc import ABCMeta, abstractmethod
from ..config import Configuration

class BaseModel(metaclass=ABCMeta):
    def __init__(self, config: Configuration):
        self.config = config

    @abstractmethod
    def build(self, *args, **kwargs):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, data, *args, **kwargs):
        pass
