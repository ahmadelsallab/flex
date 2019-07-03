# This file uses the same run() sequence in the base runner

from ..data.custom_loaders import MyDataLoader
from ..data.custom_preprocessors import MyDataPreprocessor
from ..learners.custom_learners import MyLearner
from ..models.custom_models import MyModel
from flex.flex.runs import Experiment

from ..configs.custom_config import config # Note that, we could directly put the params here, but it can also be kept under configs as it can be used with other runs

# Load data
loader = MyDataLoader(config=config)

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)

# Build model
model = MyModel(config=config)


# Train
learner = MyLearner(config=config)


# Run experiment
experiment = Experiment(loader=loader,
                        preprocessor=preprocessor,
                        model=model,
                        learner=learner,
                        config=config)
experiment.run()