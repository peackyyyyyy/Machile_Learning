from typing import List

from app.value_object.model_data import ModelData


class ModelEvaluator:

    def get_best_model(self, models_data: List[ModelData]) -> ModelData:
        best_model = models_data[0]
        print("Calculating the Best Model")
        for model_data in models_data:
            if self._safe_div(model_data.get_statistics().get_positives_rate(), model_data.get_statistics().get_false_positives_rate()) \
                    + self._safe_div(model_data.get_statistics().get_negatives_rate(), model_data.get_statistics().get_false_negatives_rate()) \
                    >= self._safe_div(best_model.get_statistics().get_positives_rate(), best_model.get_statistics().get_false_positives_rate()) \
                    + self._safe_div(best_model.get_statistics().get_negatives_rate(), best_model.get_statistics().get_false_negatives_rate()):
                best_model = model_data
        print("The Model %d is the best Model" % best_model.get_number())
        return best_model

    def _safe_div(self, a, b):
        if b == 0.0:
            return float('Inf')
        else:
            return a / b