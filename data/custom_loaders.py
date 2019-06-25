from mlfmwk.utils.data import  BaseDataLoader


class MyDataLoader(BaseDataLoader):
    def __init__(self, config):
        super().__init__(config)


    def load_data(self, *args, **kwargs):
        print('MyDataLoader')