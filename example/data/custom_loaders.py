from flex.flex.data import  BaseDataLoader
from flex.flex.data import  RawData



class MyDataLoader(BaseDataLoader):
    def __init__(self, config):
        super().__init__(config)

    def load_data(self, *args, **kwargs) -> RawData:
        print('MyDataLoader')