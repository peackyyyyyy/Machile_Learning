from unittest import TestCase
from app.adapter.file_adapter import FileAdapter


class TestFileAdapter(TestCase):

    def setUp(self) -> None:
        self._subject = FileAdapter()

    def test_string_to_int_should_return_expected_expression(self):
        test = [{"toto": 7, "ed": "Niveau bac", "default": "Oui"}, {"toto": 4, "ed": "Bac+2", "default": "Oui"},
                {"toto": 4, "ed": "Bac+5 et plus", "default": "Non"}]
        expected = [{"toto": 7, "ed": 0, "default": 1}, {"toto": 4, "ed": 2, "default": 1}, {"toto": 4, "ed": 5,
                                                                                             "default": 0}]
        result = self._subject.string_to_int(test)
        self.assertListEqual(expected, result)

    def test_get_label_list_should_return_expected_expression(self):
        dataframes_train = [{"branch": 7, "ed": "Niveau bac", "default": "Oui"}, {"branch": 4, "ed": "Bac+2", "default": "Oui"},
                {"branch": 4, "ed": "Bac+5 et plus", "default": "Non"}]
        dataframes_test = [{"branch": 3, "ed": "Bac+3", "default": "Non"}, {"branch": 4, "ed": "Bac+1", "default": "Oui"},
                {"branch": 4, "ed": "Bac+5 et plus", "default": "Oui"}]
        expected_dataframes_train = [{"branch": 7, "ed": "Niveau bac"}, {"branch": 4, "ed": "Bac+2"},
                {"branch": 4, "ed": "Bac+5 et plus"}]
        expected_dataframes_test = [{"branch": 3, "ed": "Bac+3"}, {"branch": 4, "ed": "Bac+1"},
                {"branch": 4, "ed": "Bac+5 et plus"}]
        expected_label_train = ["Oui", "Oui", "Non"]
        expected_label_test = ["Non", "Oui", "Oui"]
        result_dataframes_train, result_dataframes_test, label_train, label_test = self._subject.get_label_list(
            dataframes_train, dataframes_test)
        self.assertListEqual(expected_dataframes_train, result_dataframes_train)
        self.assertListEqual(expected_dataframes_test, result_dataframes_test)
        self.assertListEqual(expected_label_train, label_train)
        self.assertListEqual(expected_label_test, label_test)


