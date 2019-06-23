from mlfmwk.data.base_loaders import BaseDataLoader
from mlfmwk.data.base_preprocessors import BaseDataPreprocessor
from mlfmwk.models.base_model import BaseModel
from mlfmwk.learners.base_learner import BaseLearner
from mlfmwk.experiments.base_config import Config

class Experiment:
    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 learner: BaseLearner,
                 config: Config):
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
        self.model.predict()

        # Load results
        self.config.to_csv(csv_file='results.csv')

from mlfmwk.data.custom_loaders import MyDataLoader
from mlfmwk.data.custom_preprocessors import MyDataPreprocessor
from mlfmwk.models.custom_models import MyModel
from mlfmwk.learners.custom_learners import MyLearner
from mlfmwk.experiments.base_config import Config

# Configure
meta = {'name': 'exp1',
        'objective': 'test'}

config = {'optimizer': 'Adam',
          'lr': 0.1,
          'batch_size': 128,
          'lstm_size': 100, }

results = {'acc': 0.99,
           'comment': 'Best model'}

# Load data
loader = MyDataLoader(config=config)

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)

# Build model
model = MyModel(config=config)


# Train
learner = MyLearner(config=config)

# Load results
config = Config(meta_data=meta, config=config, results=results)

# Run experiment
experiment = Experiment(loader=loader,
                        preprocessor=preprocessor,
                        model=model,
                        learner=learner,
                        config=config)
experiment.run()