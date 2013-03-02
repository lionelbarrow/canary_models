from unittest import TestCase
from datetime import date
import json

from canary_models.controllers.data_controller import DataController
from canary_models.feeds.fake_gateway import FakeGateway

class ControllerTest(TestCase):

    def test_fed_funds_series_happy_path(self):
        controller = DataController()
        controller.data_feed.gateway = FakeGateway()
        start_date = date(year=2010, day=1, month=1)
        end_date = date(year=2011, day=1, month=1)
        series_json = controller.fed_funds_series(start_date, end_date)
        series = json.loads(series_json)
        self.assertEqual(len(series), 12)

    #def test_build_probit_model_runs_without_error(self):
    #    controller = DataController()
    #    model = controller.probit_model(1)
    #    self.assertTrue(isinstance(model, RegressionModel))

    #def test_get_previous_data_returns_correctly(self):
    #    controller = DataController()
    #    previous_data = controller.all_probit_data(1)
    #    self.assertTrue(True)
