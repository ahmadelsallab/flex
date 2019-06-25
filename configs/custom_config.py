
from mlfmwk.utils.config import Configuration

# Configure
meta = {'name': 'exp1',
        'objective': 'test'}

config = {'optimizer': 'Adam',
          'lr': 0.1,
          'batch_size': 128,
          'lstm_size': 100, }

results = {'acc': 0.99,
           'comment': 'Best model'}

# Form configs
config = Configuration(meta_data=meta, params=config, performance=results)