from mlfmwk.config.base_config import Configuration
from mlfmwk.data.base_loaders import BaseDataLoader
from mlfmwk.data.base_preprocessors import BaseDataPreprocessor
from mlfmwk.learners.base_learner import BaseLearner
from mlfmwk.models.base_model import BaseModel


class Runner:
    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 learner: BaseLearner,
                 config: Configuration):
        self.loader = loader
        self.preprocessor = preprocessor
        self.model = model
        self.learner = learner
        self.config = config

    def run(self):
        # Load data
        raw_data = self.loader.load_data()

        # Preprocess data
        data = self.preprocessor.preprocess_data(raw_data)

        # TODO: Add to learner train, test split
        train_data = data
        test_data = data

        # Build model
        self.model.build()

        # Train
        self.learner.train(train_data=train_data, model=model)

        # Test
        self.learner.test(test_data=test_data, model=model)

        # Predict
        #self.model.predict()

        # Load results
        self.config.to_csv(csv_file='results.csv')

