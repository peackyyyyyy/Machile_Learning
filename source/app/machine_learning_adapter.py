from io import BytesIO
from typing import List

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import joblib
from sklearn.tree import DecisionTreeClassifier
import pickle

from app.value_object.dataframe import Dataframe
from app.value_object.model import Model


class MachineLearningAdapter(object):

    def __init__(self, cross_validation=5, n_jobs=-1):
        self._cross_validation = cross_validation
        self._n_jobs = n_jobs

    def get_new_random_forest_classifier(self):
        return RandomForestClassifier()

    def get_new_decision_tree_classifier(self):
        return DecisionTreeClassifier()

    def get_trained_classifier(self, classifier, parameters, X: Dataframe, Y: List[int]) -> Model:
        dataframe = X.get_dataframe()
        grid_search_cross_validation = GridSearchCV(classifier, parameters, cv=self._cross_validation,
                                                    n_jobs=self._n_jobs)
        models_architectures = grid_search_cross_validation.fit(dataframe, Y)
        best_model = models_architectures.best_estimator_
        model_trained = best_model.fit(dataframe, Y)
        model = Model(model_trained)
        return model

    def predict_probabilities(self, X: Dataframe, classifier_model: Model) -> List[float]:
        pandas_dataframe = X.get_dataframe()
        sklearn_classifier = classifier_model.get_model()
        sklearn_classifier.n_jobs = -1
        Y_as_numpy_ndarray = sklearn_classifier.predict_proba(pandas_dataframe)[:, 1]
        Y_as_list = Y_as_numpy_ndarray.tolist()
        return Y_as_list

    def convert_model_to_pickle(self, model: Model) -> bytes:
        buffer = BytesIO()
        pickle.dump(model.get_model(), buffer)
        return buffer.getvalue()

    def convert_pickle_to_model(self, pickle_data: bytes) -> Model:
        buffer = BytesIO(pickle_data)
        cots_model = joblib.load(buffer)
        return Model(cots_model)
