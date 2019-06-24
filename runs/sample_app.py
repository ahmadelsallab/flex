from mlfmwk.config.base_config import Configuration
from mlfmwk.data.custom_loaders import MyDataLoader
from mlfmwk.data.custom_preprocessors import MyDataPreprocessor
from mlfmwk.runs.base_app import Application
from mlfmwk.models.custom_models import MyModel

# Configure
meta = {'name': 'exp1',
        'objective': 'test'}

config = {'optimizer': 'Adam',
          'lr': 0.1,
          'batch_size': 128,
          'lstm_size': 100,
          'data_path':'../dat/'}

results = {'acc': 0.99,
           'comment': 'Best model'}

# Form config
config = Configuration(meta_data=meta, config=config, results=results)

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