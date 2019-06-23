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
          'lstm_size': 100,}

results = {'acc': 0.99,
           'comment': 'Best model'}

# Load data
loader = MyDataLoader(config=config)
raw_data = loader.load_data()

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)
data = preprocessor.preprocess_data(raw_data)

# TODO: Add to learner train, test split
train_data = data
test_data = data

# Build model
model = MyModel(config=config)
model.build()

# Train
learner = MyLearner(config=config)

learner.train(train_data=train_data, model=model)

# Test
learner.test(test_data=test_data, model=model)

# Predict
model.predict()

# Load results
experiment = Config(meta_data=meta, config=config, results=results)
experiment.to_csv(csv_file='results.csv')