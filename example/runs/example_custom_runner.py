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