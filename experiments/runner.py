from mlfmwk.data.custom_loaders import MyDataLoader
from mlfmwk.data.custom_preprocessors import MyDataPreprocessor
from mlfmwk.models.custom_models import MyModel
from mlfmwk.learners.custom_learners import MyLearner
from mlfmwk.experiments.base_experiment import Experiment

# Configure
meta = {'name': 'exp1',
        'objective': 'test'}

config = {'optimizer': 'Adam',
          'lr': 0.1,
          'batch_size': 128,
          'lstm_size': 100,}

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

learner.train()

# Test
learner.test()

# Predict
model.predict()