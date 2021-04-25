import csv
import os

from app.adapter.dataframe_adapter import DataframeAdapter
from app.adapter.datas_adapter import DataAdapter
from app.adapter.file_adapter import FileAdapter
from app.business.classifier_controller import ClassifierController
from app.value_object.model_data import ModelData


class Prediction:

    def __init__(self, classifier_controller: ClassifierController, file_adapter: FileAdapter,
                 dataframe_adapter: DataframeAdapter, datas_adapter: DataAdapter):
        self._classifier_controller = classifier_controller
        self._file_adapter = file_adapter
        self._dataframe_adapter = dataframe_adapter
        self._datas_adapter = datas_adapter

    def make_prediction(self, path: str, model: ModelData, threshold: float, output_directory, stats_dir):
        dataframes = []
        data = self._file_adapter.convert_csv_to_dict(path)
        dict_dataframes = self._file_adapter.string_to_int(data)
        for dict_dataframe in dict_dataframes:
            dataframe = self._dataframe_adapter.create_dataframe(dict_dataframe)
            dataframes.append(dataframe)
        global_dataframe = self._dataframe_adapter.concatenate_dataframes_by_rows(dataframes)
        print("Starting prediction")
        results = self._classifier_controller.predict_probabilities(global_dataframe, model.get_model())
        for result, dict_dataframe in zip(results, dict_dataframes):
            if result > threshold:
                label = 'Oui'
            else:
                label = 'Non'
            dict_dataframe['default'] = label
        csv_columns = ["branch", "ncust", "customer", "age", "ed", "employ", "address", "income", "debtinc", "creddebt",
                       "othdebt", "default"]
        print("Saving files at %s" % path)
        output_file = os.path.join(output_directory, "prediction.csv")
        try:
            with open(output_file, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_dataframes:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        try:
            with open(stats_dir, 'w') as f:
                f.write("Model %d stats:" % model.get_number()+"\n")
                f.write("Model threshold : %s" % model.get_threshold()+"\n")
                f.write("positives_rate :%s" % model.get_statistics().get_positives_rate()+"\n")
                f.write("negatives_rate :%s" % model.get_statistics().get_negatives_rate()+"\n")
                f.write("false_positives_rate :%s" % model.get_statistics().get_false_positives_rate()+"\n")
                f.write("false_negatives_rate :%s" % model.get_statistics().get_false_negatives_rate()+"\n")
                f.close()
        except IOError:
            print("I/O error")
