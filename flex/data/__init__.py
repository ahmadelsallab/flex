from abc import ABCMeta, abstractmethod


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BaseDataLoader(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def load_data(self, *args, **kwargs):

        pass

class BaseDataPreprocessor(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def preprocess_data(self, *args, **kwargs):
        pass
