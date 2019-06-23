from abc import ABCMeta, abstractmethod


class BaseDataLoader(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def load_data(self, *args, **kwargs):

        pass
