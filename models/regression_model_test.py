from unittest import TestCase
import datetime, pickle

import numpy as np

from canary_models.models.regression_model import RegressionModel, SERIES
from canary_models.test_helpers.test_data import TestData

class RegressionModelTest(TestCase):

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
