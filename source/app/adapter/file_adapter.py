import pandas as pd
from typing import List, Tuple


class FileAdapter:

    def convert_csv_to_dict(self, path: str) -> List[dict]:
        result = []
        reader = pd.read_csv(path)
        for index, row in reader.iterrows():
            result.append(row.to_dict())
        return result

    def string_to_int(self, dataframes: List[dict]) -> List[dict]:
        for dataframe in dataframes:
            level = dataframe['ed']
            if level == 'Niveau bac':
                dataframe['ed'] = 0
            elif level == 'Bac+1':
                dataframe['ed'] = 1
            elif level == 'Bac+2':
                dataframe['ed'] = 2
            elif level == 'Bac+3':
                dataframe['ed'] = 3
            elif level == 'Bac+4':
                dataframe['ed'] = 4
            elif level == 'Bac+5 et plus':
                dataframe['ed'] = 5
            try:
                label = dataframe['default']
                if label == 'Oui':
                    dataframe['default'] = 1
                elif label == 'Non':
                    dataframe['default'] = 0
            except KeyError:
                pass
        return dataframes

    def get_label_list(self, dataframes_train: List[dict], dataframes_test: List[dict]) -> Tuple[List[dict], List[dict],
                                                                                                 List[dict], List[
                                                                                                     dict]]:
        label_train = []
        label_test = []
        dataframes_train_labeless = []
        dataframes_test_labeless = []
        for dataframe_train in dataframes_train:
            label_train.append(dataframe_train['default'])
            dataframes_train_labeless.append({key: dataframe_train[key] for key in dataframe_train.keys() &
                                              {"branch", "ncust", "customer", "age", "ed", "employ", "address",
                                               "income", "debtinc", "creddebt", "othdebt"}})
        for dataframe_test in dataframes_test:
            label_test.append(dataframe_test['default'])
            dataframes_test_labeless.append({key: dataframe_test[key] for key in dataframe_test.keys() &
                                              {"branch", "ncust", "customer", "age", "ed", "employ", "address",
                                               "income", "debtinc", "creddebt", "othdebt"}})
        return dataframes_train_labeless, dataframes_test_labeless, label_train, label_test
