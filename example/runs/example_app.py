# This file uses the same run() sequence in the base app

from ..data.custom_loaders import MyDataLoader
from ..data.custom_preprocessors import MyDataPreprocessor
from ..models.custom_models import MyModel
from flex.flex.runs import Application

from ..configs.custom_config import config # Note that, we could directly put the params here, but it can also be kept under configs as it can be used with other runs

# Load data
loader = MyDataLoader(config=config)

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)

# Build model
model = MyModel(config=config)

# Run experiment
app = Application(loader=loader,
                    preprocessor=preprocessor,
                    model=model,
                    config=config)
results = app.run()