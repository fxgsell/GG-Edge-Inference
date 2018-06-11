class Infer:
    def __init__(self, path="/ml/my-model"): ## TODO: Update the path
        self.categories = ['bad', 'good', 'none']
        # Load MXNet model in self.net

    def do(self, frame):
        category = 0 # TODO: Replace By self.net inference

        return self.categories[category]