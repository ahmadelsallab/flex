from flex.flex.data import BaseDataPreprocessor
from flex.flex.data import Data, RawData

class MyDataPreprocessor(BaseDataPreprocessor):

    def __init__(self, config):
        super().__init__(config)

    def preprocess_data(self, data: RawData, *args, **kwargs) -> Data:
        print('MyDataPreprocessor')