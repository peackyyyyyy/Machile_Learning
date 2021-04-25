from app.value_object.model import Model
from app.value_object.statistics import Statistics


class ModelData:

    def __init__(self, number: int, model: Model, statistics: Statistics, threshold: float):
        self._model = model
        self._statistics = statistics
        self._threshold = threshold
        self._number = number

    def get_model(self):
        return self._model

    def get_statistics(self):
        return self._statistics

    def get_threshold(self):
        return self._threshold

    def get_number(self):
        return self._number