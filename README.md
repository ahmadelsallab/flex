# FLEX
Framework for mchine Learning EXperiment

# Features
- Framework independent. Frameworks are plugins.
- Reproducible experiments, with configuration management over meta data, hyper parameters and results.
- Support of reusable models, data loaders, preprocessing,...etc
- Standardized learning process and interfaces
- Extensible for models, data, training methods, utils and frameworks.
- Utils for models, data loaders, data preprocessing, text, image, ...etc.

# Usage

## Configuration management of experiments
In machine learning you perform many experiments until you settle on a good model. During this journey you have a lot of checkpoints, visualizations, results,...etc.

The logger helps you to organize and keep track of:
- The experiments results
- TODO: The model checkpoints
- TODO: Different visualizations and curves

More use cases under tests/test_experiment.py

### Log new experiment result
In general any experiment is composed of:
- meta_data: name, purpose, file, commit,...etc
- config: mostly the hyperparameters, and any other configuration like the used features. For deep learning, config can be further divided into: data, model, optimizer, learning hyper parameters
- results: metrics, best model file, comment,..etc


Suppose all your previous records are in 'results_old.csv'.

And now you want to log a new experiment.


```python
from flex.config import Configuration

exp_meta_data = {'name': 'experiment_1',
            'purpose': 'test my awesome model',
             'date': 'today',
            }

exp_config = {'model_arch': '100-100-100',
          'learning_rate': 0.0001,
          'epochs': 2,
          'optimizer': 'Adam',
         }

exp_results = {'val_acc': 0.95, 
         'F1': 0.92,
         'Comment': 'Best model'}

experiment = Configuration(csv_file='results_old.csv', meta_data=exp_meta_data, config=exp_config, results=exp_results)


```

__Note that__

you can add or remove experiment parameters. In that case, if you add a parameter, old records will have NaN for those. If you delete some parameters, they will remain in the old records, but will be NaN in the new logged one.

Now Write CSV of the results


```python
experiment.to_csv('results.csv')
```

If you want to see the whole record:


```python
print(experiment.df)
```


### Alternatively, you could init the Experiment with the old records, and later log one or more experiment


```python
from flex.config import Configuration

# Load the old records
experiment = Configuration(csv_file='results_old.csv')

# TODO: perform you experiment

# Now log the new experiment data
exp_meta_data = {'name': 'experiment_1',
            'purpose': 'test my awesome model',
             'date': 'today',
            }

exp_config = {'model_arch': '100-100-100',
          'learning_rate': 0.0001,
          'epochs': 2,
          'optimizer': 'Adam',
         }

exp_results = {'val_acc': 0.95, 
         'F1': 0.92,
         'Comment': 'Best model'}

experiment.log(meta_data=exp_meta_data, params=exp_config, perfromance=exp_results)

# Export the whole result
experiment.to_csv('results.csv')
```

### You can init an emtpy experiment, or with a certain csv, and add or change the old records csv.

__But in this case, the records will be modified not appended or updated.__


```python
from flex.config import Configuration
# Init empty experiment
experiment = Configuration() # or Experiment(csv_file="another_results.csv")

# Update with another
experiment.from_csv(csv_file='results_old.csv')

# Now log the new experiment data
exp_meta_data = {'name': 'experiment_1',
            'purpose': 'test my awesome model',
             'date': 'today',
            }

exp_config = {'model_arch': '100-100-100',
          'learning_rate': 0.0001,
          'epochs': 2,
          'optimizer': 'Adam',
         }

exp_results = {'val_acc': 0.95, 
         'F1': 0.92,
         'Comment': 'Best model',}

experiment.log(meta_data=exp_meta_data, params=exp_config, performance=exp_results)

# Export the whole result
experiment.to_csv('results.csv')

experiment.df
```

### Other use cases

- You can load old records from pandas.DataFrame instead of csv using orig_df in the Experiment constructor
```
df = pd.read_csv('results.old.csv')
experiment = Experiment(orig_df=df)
```

- You can log experiment using yaml files, either in init or using ```from_yaml``` method



# Known issues
https://github.com/ahmadelsallab/flex/issues



