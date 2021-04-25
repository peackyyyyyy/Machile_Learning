from app.value_object.dataframe import Dataframe
from typing import List
import random


class DataAdapter:

    def delete_useless_data(self, dataframes: List[dict], key: str):
        for dataframe in dataframes:
            dataframe.pop(key)
        return dataframes

    def split_into_train_test(self, dataframes: List[dict], number_train_test: int):
        dataframes_default_true = []
        dataframes_default_false = []
        dataframes_train = []
        random.shuffle(dataframes)
        for dataframe in dataframes:
            if dataframe['default'] == 1:
                dataframes_default_true.append(dataframe)
            elif dataframe['default'] == 0:
                dataframes_default_false.append(dataframe)
        list_default_true = len(dataframes_default_true)
        list_default_false = len(dataframes_default_false)
        train_default_false_number = number_train_test / 100 * list_default_false
        print("number of negative in train df: %d" % train_default_false_number)
        for i in range(int(train_default_false_number)):
            dataframes_train.append(dataframes_default_false.pop(0))
        train_default_true_number = number_train_test / 100 * list_default_true
        print("number of positive in train df: %d" % train_default_true_number)
        for i in range(int(train_default_true_number)):
            dataframes_train.append(dataframes_default_true.pop(0))
        dataframes_test = dataframes_default_false + dataframes_default_true
        return dataframes_train, dataframes_test
