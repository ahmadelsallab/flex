from mlfmwk.learners.base_learner import BaseLearner

class MyLearner(BaseLearner):
    def __init__(self, config):
        super().__init__(config=config)

    def train(self, *args, **kwargs):
        pass

    def test(self, *args, **kwargs):
        pass