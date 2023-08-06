import pytest
import pandas as pd
from unittest.mock import patch
from moviesViewEstimator.model import LinearRegressionModel


class TestModel:
    def test_prediction(self):

        predict_dataframe = pd.DataFrame([[8.2, 89224]])  # rate 8.2 and almost 90 thousand rate count
        predict_dataframe.columns = ['Rating', 'Rating Count']  # setting the columns names

        model = LinearRegressionModel()
        result = model.predict(predict_dataframe)

        assert isinstance(result.item(), int)

    @patch('tests.test_model.LinearRegressionModel', side_effect=FileNotFoundError)
    def test_no_file(self, mock):
        with pytest.raises(FileNotFoundError):

            model = LinearRegressionModel()

            assert model.linear_regression_model is None
