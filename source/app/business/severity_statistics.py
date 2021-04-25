from app.adapter.dataframe_adapter import DataframeAdapter
from app.classifier_controller import ClassifierController
from app.value_object.dataframe import Dataframe
from app.value_object.model import Model
from app.value_object.statistics import Statistics


class SeverityStatistics:

    def __init__(self, classifier_controller: ClassifierController, dataframe_adapter: DataframeAdapter):
        self._classifier_controller = classifier_controller
        self._dataframe_adapter = dataframe_adapter

    def get_statistics(self, dataframe: Dataframe, model: Model, threshold: float, labels) -> Statistics:
        is_safe_and_predict_safe = 0.0
        is_safe_and_predict_default = 0.0
        is_default_and_predict_safe = 0.0
        is_default_and_predict_default = 0.0
        probabilities = self._classifier_controller.predict_probabilities(dataframe, model)
        labels_probabilities = zip(labels, probabilities)

        for label, probability in labels_probabilities:
            predict_default = probability > threshold
            is_default = label == 1

            if is_default and predict_default:
                is_default_and_predict_default += 1
            if is_default and not predict_default:
                is_default_and_predict_safe += 1
            if not is_default and not predict_default:
                is_safe_and_predict_safe += 1
            if not is_default and predict_default:
                is_safe_and_predict_default += 1



        positives_rate = self._safe_div(is_default_and_predict_default, is_default_and_predict_default + is_default_and_predict_safe)
        negatives_rate = self._safe_div(is_safe_and_predict_safe, is_safe_and_predict_safe + is_safe_and_predict_default)
        false_positives_rate = self._safe_div(is_safe_and_predict_default, is_safe_and_predict_default + is_safe_and_predict_safe)
        false_negatives_rate = self._safe_div(is_default_and_predict_safe, is_default_and_predict_safe + is_default_and_predict_default)

        statistics = Statistics(false_positives_rate, false_negatives_rate, positives_rate, negatives_rate)
        return statistics

    def _safe_div(self, a, b):
        if b == 0.0:
            return float('Inf')
        else:
            return a / b