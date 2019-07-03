
from flex.flex.config import Configuration
import pandas as pd
# Configure
meta = {'name': 'exp1',
        'objective': 'test'}

params = {'optimizer': 'Adam',
          'lr': 0.1,
          'batch_size': 128,
          'lstm_size': 100, }

results = {'acc': 0.99,
           'comment': 'Best model'}
config = pd.concat([pd.DataFrame([meta], index=[0]), pd.DataFrame([params], index=[0]), pd.DataFrame([results], index=[0])], axis=1)

# Form configs
config = Configuration(config=config)