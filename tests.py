from unittest import TestCase
import numpy as np

from xml.dom.minidom import parseString
import datetime, pickle

from feed import APIDataFeed
from controller import DataFeedController
from models import RegressionModel, SERIES

class TestData(object):

    def __init__(self):
        test_data = open("predictive_models/sample_data.txt")
        self.FED_DATA = pickle.load(test_data)
        test_data.close()

class Feed_Unit(TestCase):

    def test_is_good_date_returns_true_correctly(self):
        feed = APIDataFeed()
        good_date_dom = parseString('<observation date="2012-9-29" />')
        good_date = good_date_dom.getElementsByTagName('observation')[0]

        self.assertTrue(feed.is_good_date(good_date))

    def test_is_good_date_returns_false_correctly(self):
        feed = APIDataFeed()
        bad_date_dom = parseString('<observation date="1929-10-20" />')
        bad_date = bad_date_dom.getElementsByTagName('observation')[0]

        self.assertFalse(feed.is_good_date(bad_date))

    def test_observation_values_returns_floats(self):
        feed = APIDataFeed()
        dom = parseString('<observation value=".12" />').getElementsByTagName('observation')
        values = feed.observation_values(dom)

        self.assertTrue(isinstance(values[0], float))

class Controller_Unit(TestCase):

    def test_build_probit_model_runs_without_error(self):
        controller = DataFeedController()
        model = controller.probit_model(1)
        self.assertTrue(isinstance(model, RegressionModel))

class Controller_Integration(TestCase):

    def test_get_previous_data_returns_correctly(self):
        controller = DataFeedController()
        previous_data = controller.all_probit_data(1)
        self.assertTrue(True)

class Model_Unit(TestCase):

    def test_validate_accepts_all_legitimate_series(self):
        names = SERIES[:-1]
        model = RegressionModel({}, 1)
        model.validate_series_names(names)
        self.assertTrue(True)

    def test_validate_raises_error_on_invalid_series(self):
        invalid_series = ["invalid", SERIES[0], SERIES[1]]
        model = RegressionModel({}, 1)
        try:
            model.validate_series_names(invalid_series)
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False, "Expected value error was not raised.")

    def test_length_check_can_pass(self):
        valid_series = {"numbers": [1,2,3], "letters": ["a", "b", "c"]}
        model = RegressionModel({}, 1)
        model.validate_series_lengths(valid_series)
        self.assertTrue(True)

    def test_length_check_can_fail(self):
        invalid_series = {"numbers": [1, 2], "letters": ["a"]}
        model = RegressionModel({}, 1)
        try:
            model.validate_series_lengths(invalid_series)
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False, "Expected value error was not raised.")

    def test_build_np_array_runs_without_error(self):
        model = RegressionModel(TestData().FED_DATA, 6)
        model.build_model()
        self.assertTrue(True)

    def test_chop_array_chops_from_front_correctly(self):
        test_array = np.arange(20).reshape(4, 5)
        model = RegressionModel({}, 2)
        result, remainder = model.chop_array(test_array, chop_front=True)

        expected_result = np.arange(10, 20).reshape(2, 5)
        self.assertTrue(np.equal(result, expected_result).all())

        expected_remainder = np.arange(10).reshape(2, 5)
        self.assertTrue(np.equal(remainder, expected_remainder).all())

    def test_chop_array_chops_from_back_correctly(self):
        test_array = np.arange(20).reshape(4, 5)
        model = RegressionModel({}, 2)
        result, remainder = model.chop_array(test_array, chop_front=False)

        expected_result = np.arange(10).reshape(2, 5)
        self.assertTrue(np.equal(result, expected_result).all())

        expected_remainder = np.arange(10, 20).reshape(2, 5)
        self.assertTrue(np.equal(remainder, expected_remainder).all())
