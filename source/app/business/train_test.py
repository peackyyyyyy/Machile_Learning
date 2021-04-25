from typing import List

from app.adapter.dataframe_adapter import DataframeAdapter
from app.adapter.file_adapter import FileAdapter
from app.business.random_forest_trainer import RandomForestTrainer
from app.business.severity_statistics import SeverityStatistics
from app.business.classifier_controller import ClassifierController
from app.adapter.machine_learning_adapter import MachineLearningAdapter
from app.adapter.datas_adapter import DataAdapter
from app.value_object.model_data import ModelData


class TrainTest:

    def __init__(self, dataframe_adapter: DataframeAdapter, file_adapter: FileAdapter, random_forest_trainer:
    RandomForestTrainer, severity_statistics: SeverityStatistics, classifier_controller: ClassifierController,
                 machine_learning_adapter: MachineLearningAdapter, datas_adapter: DataAdapter):
        self._dataframe_adapter = dataframe_adapter
        self._file_adapter = file_adapter
        self._random_forest_trainer = random_forest_trainer
        self._severity_statistics = severity_statistics
        self._classifier_controller = classifier_controller
        self._machine_learning_adapter = machine_learning_adapter
        self._datas_adapter = datas_adapter

    def train(self, thresholds: List[float], data: List[dict]):
        models_data = []
        i = 1
        for threshold in thresholds:
            dataframes_train = []
            dataframes_tests = []
            dict_dataframes = self._file_adapter.string_to_int(data)
            train_split_dataframes, test_split_dataframes = self._datas_adapter.split_into_train_test(dict_dataframes, 80)
            train_dataframes, test_dataframes, label_train, label_test = self._file_adapter.get_label_list(
                train_split_dataframes, test_split_dataframes)
            for train_dataframe in train_dataframes:
                dataframe = self._dataframe_adapter.create_dataframe(train_dataframe)
                dataframes_train.append(dataframe)
            global_train_dataframe = self._dataframe_adapter.concatenate_dataframes_by_rows(dataframes_train)
            for test_dataframe in test_dataframes:
                dataframe = self._dataframe_adapter.create_dataframe(test_dataframe)
                dataframes_tests.append(dataframe)
            global_test_dataframe = self._dataframe_adapter.concatenate_dataframes_by_rows(dataframes_tests)
            print("Model %d is training, gonna take a while" % i)
            model = self._random_forest_trainer.train(global_train_dataframe, label_train)
            statistics = self._severity_statistics.get_statistics(global_test_dataframe, model, threshold, label_test)
            model_data = ModelData(i, model, statistics, threshold)
            print("Model %d stats:" % i)
            print("positives_rate :%s" % model_data.get_statistics().get_positives_rate())
            print("negatives_rate :%s" % model_data.get_statistics().get_negatives_rate())
            print("false_positives_rate :%s" % model_data.get_statistics().get_false_positives_rate())
            print("false_negatives_rate :%s" % model_data.get_statistics().get_false_negatives_rate())
            models_data.append(model_data)
            i = i + 1
        return models_data
