from typing import List, Tuple

import pandas
import io

from app.value_object.dataframe import Dataframe


class DataframeAxis:
    COLUMNS = 1
    ROWS = 0


class DataframeAdapter:

    def create_dataframe(self, matrix_features: dict) -> Dataframe:
        matrix_features = dict(matrix_features)
        self._transform_scalar_value_into_list(matrix_features)
        pandas_dataframe = pandas.DataFrame(matrix_features)
        pandas_dataframe = pandas_dataframe[sorted(pandas_dataframe)]
        dataframe = Dataframe(pandas_dataframe)
        return dataframe

    def concatenate_dataframes_by_columns(self, dataframes: List[Dataframe]) -> Dataframe:
        return self._concatenate_dataframes(dataframes, DataframeAxis.COLUMNS)

    def concatenate_dataframes_by_rows(self, dataframes: List[Dataframe]) -> Dataframe:
        return self._concatenate_dataframes(dataframes, DataframeAxis.ROWS)

    def convert_dataframe_to_dict(self, dataframe: Dataframe) -> dict:
        pandas_dataframe = dataframe.get_dataframe()
        return pandas_dataframe.to_dict(orient='list')

    def only_keep_columns(self, columns: List[str], dataframe: Dataframe) -> Dataframe:
        pandas_dataframe = dataframe.get_dataframe()
        dataframe_columns = pandas_dataframe.columns.values
        columns_to_remove = list(set(dataframe_columns) - set(columns))
        pandas_dataframe_dropped = pandas_dataframe.drop(columns=columns_to_remove)
        dataframe_updated = Dataframe(pandas_dataframe_dropped)
        return dataframe_updated

    def get_column_values(self, column: str, dataframe: Dataframe) -> List[str] or List[float] or List[int]:
        pandas_dataframe = dataframe.get_dataframe()
        return pandas_dataframe[column].values.tolist()

    def remove_columns(self, columns: List[str], dataframe: Dataframe) -> Dataframe:
        pandas_dataframe = dataframe.get_dataframe()
        pandas_dataframe_dropped = pandas_dataframe.drop(columns=columns, errors='ignore')
        dataframe_updated = Dataframe(pandas_dataframe_dropped)
        return dataframe_updated

    def convert_dataframe_to_csv(self, dataframe: Dataframe) -> bytes:
        pandas_dataframe = dataframe.get_dataframe()
        return pandas_dataframe.to_csv(index=False, header=True).encode('utf-8')

    def convert_csv_to_dataframe(self, csv_data: bytes) -> Dataframe:
        csv_buffer = io.BytesIO(csv_data)
        pandas_dataframe = pandas.read_csv(csv_buffer)
        return Dataframe(pandas_dataframe)

    def drop_duplicate_in_dataframe(self, column, dataframe: Dataframe) -> Dataframe:
        pandas_dataframe = dataframe.get_dataframe()
        pandas_dataframe_dropped_duplicate = pandas_dataframe.drop_duplicates(subset=column, keep="last")
        return Dataframe(pandas_dataframe_dropped_duplicate)

    def get_rows_number(self, dataframe: Dataframe) -> int:
        pandas_dataframe = dataframe.get_dataframe()
        return len(pandas_dataframe)

    def convert_string_values_as_features(self, dataframe: Dataframe) -> Dataframe:
        pandas_dataframe = dataframe.get_dataframe()
        dataframe_with_dummies = pandas.get_dummies(pandas_dataframe)
        return Dataframe(dataframe_with_dummies)

    def split_rows(self, dataframe: Dataframe, number) -> Tuple[Dataframe, Dataframe]:
        pandas_dataframe = dataframe.get_dataframe()
        first_dataframe = pandas_dataframe[:number]
        second_dataframe = pandas_dataframe[number:]
        return Dataframe(first_dataframe), Dataframe(second_dataframe)

    def _concatenate_dataframes(self, dataframes, axis):
        pandas_dataframes = [dataframe.get_dataframe() for dataframe in dataframes]
        pandas_concatenated_dataframes = pandas.concat(pandas_dataframes, axis=axis, sort=True)
        return Dataframe(pandas_concatenated_dataframes)

    def _transform_scalar_value_into_list(self, matrix_features):
        if matrix_features and matrix_features.keys():
            first_key = list(matrix_features.keys())[0]
            if not isinstance(matrix_features[first_key], list):
                for key in matrix_features.keys():
                    matrix_features[key] = [matrix_features[key]]
