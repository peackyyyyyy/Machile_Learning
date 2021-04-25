import time
import os
from app.adapter.dataframe_adapter import DataframeAdapter
from app.adapter.file_adapter import FileAdapter
from app.business.model_evaluator import ModelEvaluator
from app.business.prediction import Prediction
from app.business.random_forest_trainer import RandomForestTrainer
from app.business.severity_statistics import SeverityStatistics
from app.business.train_test import TrainTest
from app.classifier_controller import ClassifierController
from app.machine_learning_adapter import MachineLearningAdapter
from app.adapter.datas_adapter import DataAdapter

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = root_dir.split("source").pop(0)
    dataframe_adapter = DataframeAdapter()
    file_adapter = FileAdapter()
    machine_learning_adapter = MachineLearningAdapter()
    random_forest_trainer = RandomForestTrainer(machine_learning_adapter)
    classifier_controller = ClassifierController(dataframe_adapter, machine_learning_adapter)
    severity_statistics = SeverityStatistics(classifier_controller, dataframe_adapter)
    data_adapter = DataAdapter()
    train_test = TrainTest(dataframe_adapter, file_adapter, random_forest_trainer, severity_statistics,
                           classifier_controller, machine_learning_adapter, data_adapter)
    model_evaluator = ModelEvaluator()
    prediction = Prediction(classifier_controller, file_adapter, dataframe_adapter, data_adapter)
    data_train_dir = os.path.join(root_dir, "data/Data_Projet.csv")
    data = file_adapter.convert_csv_to_dict(data_train_dir)
    threshold = [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53]
    models_data = train_test.train(threshold, data)
    best_model = model_evaluator.get_best_model(models_data)
    result_dir_path = os.path.join(root_dir, "result", str(time.time()))
    os.makedirs(result_dir_path)
    stats_dir = os.path.join(result_dir_path, "stats_model.txt")
    data_test_dir = os.path.join(root_dir, "data/Data_Projet_New.csv")
    prediction.make_prediction(data_test_dir, best_model, 0.5, result_dir_path, stats_dir)