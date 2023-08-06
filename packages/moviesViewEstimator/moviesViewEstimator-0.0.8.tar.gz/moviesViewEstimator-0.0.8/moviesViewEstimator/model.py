import os
import pickle
import pkgutil
import logging
import numpy as np
import pandas as pd
import pkg_resources
from sklearn.linear_model import LinearRegression


class LinearRegressionModel:
    def __init__(self):
        """
        This class holds the information and functions do handle the prediction, train, and some data processing for a
        Linear Regression Model
        """

        # ----- Setting up the logger ----- #
        self.log_level = logging.INFO
        self.log_filename = 'movies_view_estimator'

        self.string_log_format = '%(asctime)s %(levelname)s - %(funcName)s - %(message)s'

        # It handles the information that will be printed in the console that is equal or above a logging level
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.WARNING)
        self.console_handler.setFormatter(logging.Formatter(self.string_log_format))

        self.logger = logging

        # set the log configuration
        self.logger.basicConfig(level=self.log_level,
                                format=self.string_log_format,
                                filename=f'{self.log_filename}.log',
                                filemode='w'
                                )

        self.logger.getLogger().addHandler(self.console_handler)

        self.logger.info('Logger invoked inside the LinearRegressionModel')

        self.logger.info('Setting up the linear_regression_model')

        # ----- Setting up path model ----- #

        self._path = os.path.dirname(__file__)
        self._filepath = os.path.join(self._path,  "linear_regression_model.pickle")

        # ----- Setting up the model ----- #
        self.linear_regression_model = None
        self._load_model()

    def _load_model(self) -> None:
        """
        These functions load the model in the constructor and re-assign the attribute to a linear regression model to
        future use.

        Returns:
            It tries to re-assign the attribute model, if not possible it shows an error to user.

        """
        self.logger.info(f'Load model called')
        try:
            with open(self._filepath, 'rb') as file:
                self.logger.info(f'Model found, assigning to the attribute linear_regression_model')
                self.linear_regression_model = pickle.load(file)
                self.logger.info(f'Model assignment done.')

        except FileNotFoundError:
            self.logger.warning(f'Model not found, train is required!')
            self.linear_regression_model = None

    def predict(self, rating_rating_count: pd.DataFrame) -> list:
        """
        The prediction function predicts the amount of views a movie have by receiving the Rating and Rating Count
        column.

        The prediction can be called when a model exists, when do not exist, it needs to be trained first.

        Args:
            rating_rating_count:
                It receives rating_rating_count which is a pandas dataframe as parameter that contains two columns
                 required to be trained or predicted, the Rating and Rating Count column

        Returns:
            It returns a list containing the amount of views predicted by the model

        """
        try:
            self.logger.info(f'Prediction called.')
            self._data_process(rating_rating_count)

            results = self.linear_regression_model.predict(rating_rating_count)
            self.logger.info(f'Prediction made, cleaning the results.')
            results = results.astype(int)
            results[results < 0] = 0
            self.logger.info(f'Returning prediction')
            return results

        except AttributeError:
            self.logger.error(f'No model found, please, train it first.')

    def train(self, rating_rating_count: pd.DataFrame, views: list or pd.DataFrame) -> None:
        """
        This function is used to train a mode, it can be trained when there is a model already, and you want to trained
        a better one, or to train when there is no model trained already.


        Examples:
            To train work, you will need a data in a form like this one:

            >>>
            Unnamed: 0                     Title  Year  Rating  Rating Count       views
            0  tt0109830              Forrest Gump  1994     8.7       1602217  10000000.0
            1  tt0114814        The Usual Suspects  1995     8.5        903320   7500000.0
            2  tt0047396               Rear Window  1954     8.5        397045   6000000.0
            3  tt0053125        North by Northwest  1959     8.3        270627   4000000.0
            4  tt1305806  The Secret in Their Eyes  2009     8.2        172373   3000000.0
            5  tt1895587                 Spotlight  2015     8.1        362975   1000000.0


        You need to pass the ['Rating', 'Rating Count'] to train and ['views'] as label.

        Args:
            rating_rating_count:
                It receives rating_rating_count which is a pandas dataframe as parameter that contains two columns
                required to be trained or predicted, the Rating and Rating Count column.

            views:
                It can be a pandas Series, or a list, it will be used as a label when training.

        Returns:
            It overrides the already trained model with this new one.
            It there is no model saved already, it creates one.
            Also, it re-assign the new model trained overriding the old one.
        """

        self.logger.info(f'Training called.')
        self._data_process(rating_rating_count)

        self.logger.info(f'Assigning temporary model')
        linear_regression_model = LinearRegression()

        self.logger.info(f'Training the new model')
        linear_regression_model.fit(rating_rating_count, views)

        with open(self._filepath, 'wb') as file:
            self.logger.info(f'Saving the new model for future use')
            pickle.dump(linear_regression_model, file)

        self.logger.info(f'Re-assigning the new model overriding the old one')
        self.linear_regression_model = linear_regression_model

    def _data_process(self, dataframe: pd.DataFrame) -> None:
        """
        This functions receives the dataframe and manipulate the Rating Count columns which is a string and might cause
        errors when tried to be read as a number.
        Args:
            dataframe:
                It returns the pandas dataframe that will check if the columns need to be handled or not.
                If a change is required it does in place.
                Else, it passes

        Returns:
            It returns nothing, but might change the dataframe in place if required

        """
        self.logger.info(f'Data process called')
        try:
            self.logger.info(f'Cleaning the data')
            pd.options.mode.chained_assignment = None
            dataframe['Rating Count'] = dataframe['Rating Count'].str.replace(',', '').astype(np.int64)

        except AttributeError:
            self.logger.info(f'Data already cleaned, there is no need to be re-cleaned')
            pass
