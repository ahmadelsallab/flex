from mlfmwk.utils.data import BaseDataPreprocessor


class MyDataPreprocessor(BaseDataPreprocessor):
    def __init__(self, config):
        super().__init__(config)


    def preprocess_data(self, *args, **kwargs):
        print('MyDataPreprocessor')