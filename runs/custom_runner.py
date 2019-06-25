# This file uses the same run() sequennce in the base runner

from mlfmwk.data.custom_loaders import MyDataLoader
from mlfmwk.data.custom_preprocessors import MyDataPreprocessor
from mlfmwk.learners.custom_learners import MyLearner
from mlfmwk.models.custom_models import MyModel
from mlfmwk.utils.runs import Runner

from mlfmwk.configs.custom_config import config # Note that, we could directly put the config here, but it can also be kept under configs as it can be used with other runs

# Load data
loader = MyDataLoader(config=config)

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)

# Build model
model = MyModel(config=config)


# Train
learner = MyLearner(config=config)


# Run experiment
experiment = Runner(loader=loader,
                    preprocessor=preprocessor,
                    model=model,
                    learner=learner,
                    config=config)
experiment.run()