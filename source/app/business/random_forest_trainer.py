from app.machine_learning_adapter import MachineLearningAdapter
from app.value_object.dataframe import Dataframe


class RandomForestTrainer:

    def __init__(self, machine_learning_adapter: MachineLearningAdapter, n_estimators: [int] = None, max_features: [int] = None):
        self._n_estimators = n_estimators or [50, 100, 150, 200, 250, 300, 350, 400]
        self._max_features = max_features or [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self._machine_learning_adapter = machine_learning_adapter

    def train(self, X: Dataframe, Y: [int]):
        pandas_dataframe = X.get_dataframe()
        number_of_columns_in_dataframe = len(pandas_dataframe.columns)
        max_features_capped = [max_feature for max_feature in self._max_features if max_feature < number_of_columns_in_dataframe]
        max_features_capped.append(number_of_columns_in_dataframe)

        classifier = self._machine_learning_adapter.get_new_random_forest_classifier()
        parameters = {
            'max_features': max_features_capped,
            'n_estimators': self._n_estimators
        }
        return self._machine_learning_adapter.get_trained_classifier(classifier, parameters, X, Y)
