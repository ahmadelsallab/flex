from abc import ABCMeta, abstractmethod

class BaseDataPreprocessor(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def preprocess_data(self, *args, **kwargs):
        pass
