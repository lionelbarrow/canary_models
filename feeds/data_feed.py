from xml.dom.minidom import parseString
from datetime import date
import os

import requests

from canary_models.utils.utils import parse_date
from canary_models.models.observation import Observation

class DataFeed(object):

    FRED_API_KEY = os.environ.get('FRED_API_KEY', "test_fred_key")
    FRED_API_URL = 'http://api.stlouisfed.org/fred/series/observations?series_id='
    EARLIEST_ALLOWED_DATA = date(year=1964, day=1, month=1)

    def __init__(self, testing=False):
        self.testing = testing

    def query_fred_for_series(self, series):
        response = requests.get(self.FRED_API_URL + series + '&api_key=' + FRED_API_KEY)
        dom = parseString(response.content)
        elements = dom.getElementsByTagName('observation')
        return elements

    #def filter_observations_by_date(self, observations):
    #    return filter(self.is_good_date, observations)

    #def is_good_date(self, observation):
    #    date = parse_date(observation.getAttribute('date'))
    #    return date > self.EARLIEST_ALLOWED_DATA

    def new_observation(self, domElement, series):
        date = parse_date(domElement.getAttribute("date"))
        return Observation(series, date, float(domElement.getAttribute("value")))

    def get_series(self):
        xml_observations = query_fred_for_series(series)
        observations = [new_observation(xml_obs, series) for xml_obs in xml_observations]
        return observations
