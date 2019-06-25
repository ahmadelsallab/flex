# This file uses the same run() sequence in the base app

from mlfmwk.data.custom_loaders import MyDataLoader
from mlfmwk.data.custom_preprocessors import MyDataPreprocessor
from mlfmwk.models.custom_models import MyModel
from mlfmwk.utils.runs import Application

from mlfmwk.configs.custom_config import config # Note that, we could directly put the config here, but it can also be kept under configs as it can be used with other runs

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

        # Preprocess data
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