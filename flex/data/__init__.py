from abc import ABCMeta, abstractmethod
from ..config import Configuration
import numpy as np

class RawData:
    def __init__(self, x:list, y:list):
        self.x = x
        self.y = y
        assert len(x) == len(y)


class Data:
    def __init__(self, x: np.ndarray, y: np.ndarray):
        self.x = x
        self.y = y
        assert len(x) == len(y)


class BaseDataLoader(metaclass=ABCMeta):
    def __init__(self, config: Configuration):
        self.config = config

    @abstractmethod
    def load_data(self, *args, **kwargs) -> RawData:

        pass


class BaseDataPreprocessor(metaclass=ABCMeta):
    def __init__(self, config: Configuration):
        self.config = config

    @abstractmethod
    def preprocess_data(self, data: RawData, *args, **kwargs) -> Data:
        pass
