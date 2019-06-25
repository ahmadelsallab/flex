class Features:
    def __init__(self):
        pass

    def extract(self, data):
        raise NotImplementedError("extract to be implemented according to the exact feature type")

# Also called Nominal
class Categorical(Features):

    def __init__(self):
        super().__init__(self)

    # OHE = One-Hot-Encoding vs. Sparse (normal values)
    def extract(self, data, OHE=False):
        pass

# Also called Nominal
class Ordinal(Features):

    def __init__(self):
        super().__init__(self)

    def extract(self, data):
        pass