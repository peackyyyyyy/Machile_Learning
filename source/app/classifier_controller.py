from typing import List

from app.adapter.dataframe_adapter import DataframeAdapter
from app.machine_learning_adapter import MachineLearningAdapter
from app.value_object.dataframe import Dataframe
from app.value_object.model import Model


class ClassifierController(object):

    def __init__(self, dataframe_adapter: DataframeAdapter, machine_learning_adapter: MachineLearningAdapter):
        self._dataframe_adapter = dataframe_adapter
        self._maching_learning_adapter = machine_learning_adapter

    def predict_probabilities(self, dataframe: Dataframe, model: Model) -> List[float]:

        probabilities = self._maching_learning_adapter.predict_probabilities(dataframe, model)
        return probabilities
