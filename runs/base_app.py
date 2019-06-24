from mlfmwk.config.base_config import Configuration
from mlfmwk.data.base_loaders import BaseDataLoader
from mlfmwk.data.base_preprocessors import BaseDataPreprocessor
from mlfmwk.learners.base_learner import BaseLearner
from mlfmwk.models.base_model import BaseModel


class Application:
    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 config: Configuration):
        self.loader = loader
        self.preprocessor = preprocessor
        self.model = model
        self.config = config

    def run(self):
        # Load data
        raw_data = self.loader.load_data()

        # Preprocess data
        data = self.preprocessor.preprocess_data(raw_data)

        # Load model
        self.model.load()

        # Predict
        result = self.model.predict(data)

        return result