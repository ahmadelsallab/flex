# FLEX
Framework for machine Learning EXperiment

# Features
- Framework independent. Frameworks are plugins.
- Reproducible experiments, with configuration management over meta data, hyper parameters and results.
- Support of reusable models, data loaders, preprocessing,...etc
- Standardized learning process and interfaces
- Extensible for models, data, training methods, utils and frameworks.
- Utils for models, data loaders, data preprocessing, text, image, ...etc.

# Installation
! pip install --upgrade git+https://github.com/ahmadelsallab/flex.git

Or 

!git clone https://github.com/ahmadelsallab/flex.git
!cd ml_logger && pip install .
# Requirements
pip install requirements.txt


# Concept
FLEX is a framework to organize the running of ML experiments, and make them reproducible, by tracking their configurations.
The philosophy of FLEX is to keep the main components of an ML programs as re-usable plugins.

We define an ML Experiment to be composed of:
- Data loaders: loading and generating the data.
- Data pre-processors: data preparation and features processing. 
- Models: networks, classifiers,..etc.
- Learners: training procedure.
- Configurations: meta data, hyper parameters, results.

Each of the above components, can be re-used across different experiments.
Moreover, the mixture of them forms an experiment. 

## _"FLEX is flexible_"
You can use FLEX in many different ways:

- For managing experiments configurations and reproducing results.
- For wrapping and deploying ML models.
- For running standard experiments and re-using models, data,...etc across different experiments.
- Or just using the utilities inside aside of the whole framework.


Under the package called "flex", you will find many base classes that implements standard interfaces for:
- Data loading 
- Data pre-processing
- Models building
- Training (learners)
- Deployment

All the library is "framework agnostic", meaning, DL frameworks like Keras, Pytorch, ...etc are just plugins to FLEX.
It's not mandatory to use all the base classes, meaning, you can still use most of the features if you implement your own.
But we encourage to follow the same structure in order to have organized and easy flow.

## Folders structure
We have provided an example folder for the best folder structure to use FLEX.
However, this structure is not mandatory; you still can use some features like configuration management without that structure.

The structure is described here:
- configs: contains the different meta_data, params and results of different experiments using the Configuration base class.
You can define them directly as dicts (see the examples example/notebooks). However, if you wish to re-use some configuration, it's better to inherit from Configuration.
- data: contains custom re-usable loaders and pre-processors
- models: contains the different custom re-usable models
- runs: contains the different experiments and deployment apps.
- utils: project wide utilities.


## Use cases
In the following we will demo some use cases.

More use cases under the example/notebooks.
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

# Model wrapping and deployment
You have trained a model, and want to deploy it, meaning to feed it input and get an output.
But before, there are some steps you need to perform to load and prepare the data.
The class Application enables you to cast your data loaders, preprocessor and model in one app.

The run method applies the standard steps:

1- Load data

2- Preprocess data

3- Load model

4- Predict output

In the example below, there are some assumptions:

1- Global settings and configurations are pre-configured under configs/custom_config.py
You could directly write them in the same code if you want

2- All loaders, preprocessors, models,...etc are pre-defined and saved in the project folders as customs.
You could define them here if you want and pass them to the Application constructor

```buildoutcfg
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

```

You can also override and implement your own deployment steps by inheriting from the Application class and implementing your own run method

```buildoutcfg
from ..data.custom_loaders import MyDataLoader
from ..data.custom_preprocessors import MyDataPreprocessor
from ..models.custom_models import MyModel
from flex.flex.runs import Application

from ..configs.custom_config import config # Note that, we could directly put the params here, but it can also be kept under configs as it can be used with other runs

class MyApp(Application):

    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 config: Configuration):
        super().__init__(loader, preprocessor, model, config)

    # Override your custom run here
    def run(self):
        # Load data
        raw_data = self.loader.load_data()

        # Pre-process data
        data = self.preprocessor.preprocess_data(raw_data)

        # Load model
        self.model.load()

        # Predict
        result = self.model.predict(data)

        return result

# Load data
loader = MyDataLoader(config=config)

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)

# Build model
model = MyModel(config=config)

# Run experiment
app = MyApp(loader=loader,
            preprocessor=preprocessor,
            model=model,
            config=config)

results = app.run()
```

# Running and tracking ML experiment
You have an awesome model that you want to train with a dataset, following some genius pre-processing pipeline.

Moreover, as you are experimenting with different hyper-params, model choices, pre-processing choices,...etc, you want to keep track of all results and configurations you have made, and where they led, and also be able to reproduce the results of each experiment when needed.

The class Runner provides the ability to run an experiment, and use the Configuration class to save and load the experiment info to be able to run later.

The Runner class takes any custom loader, preprocessor, model,..etc. 

Through the standard run interface, standard training and evaluation steps are executed:
1- Load data

2- Preprocess data

3- Build model

4- Train model

5- Evaluate model

6- Save configuration

```buildoutcfg
from ..data.custom_loaders import MyDataLoader
from ..data.custom_preprocessors import MyDataPreprocessor
from ..learners.custom_learners import MyLearner
from ..models.custom_models import MyModel
from flex.flex.runs import Runner

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
experiment = Runner(loader=loader,
                    preprocessor=preprocessor,
                    model=model,
                    learner=learner,
                    config=config)
experiment.run()
```

Moreover, you can override the standard run() and implement some custom steps if needed:

````buildoutcfg
from ..data.custom_loaders import MyDataLoader
from ..data.custom_preprocessors import MyDataPreprocessor
from ..learners.custom_learners import MyLearner
from ..models.custom_models import MyModel
from flex.flex.runs import Runner

from ..configs.custom_config import config # Note that, we could directly put the params here, but it can also be kept under configs as it can be used with other runs


class MyExperiment(Runner):
    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 learner: BaseLearner,
                 config: Configuration):
        super().__init__(loader, preprocessor, model, learner, config)

    # Override your custom run here
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
        #self.model.predict()

        # Load performance
        self.config.to_csv(csv_file='../../runs/performance.csv')



# Load data
loader = MyDataLoader(config=config)

# Preprocess data
preprocessor = MyDataPreprocessor(config=config)

# Build model
model = MyModel(config=config)


# Train
learner = MyLearner(config=config)


# Run experiment
experiment = MyExperiment(loader=loader,
                    preprocessor=preprocessor,
                    model=model,
                    learner=learner,
                    config=config)
experiment.run()
````
# Known issues
https://github.com/ahmadelsallab/flex/issues

# Future developments
- JSON Support
- xlsx support
- The model checkpoints
- Different visualizations and curves
- Upload the result file to gdrive for online updates and sharing



