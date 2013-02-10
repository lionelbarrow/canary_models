from xml.dom.minidom import parseString
from datetime import date

import requests

FRED_API_KEY = os.environ['FRED_API_KEY']

def parse_date(datestr):
    nums = map(int, datestr.split('-'))
    return date(year=nums[0], month=nums[1], day=nums[2])

class APIDataFeed(object):

    FRED_API_URL = 'http://api.stlouisfed.org/fred/series/observations?series_id='
    EARLIEST_ALLOWED_DATA = date(year=1964, day=1, month=1)

    def __init__(self):
        pass

    def query_fred_for_series(self, series):
        response = requests.get(self.FRED_API_URL + series + '&api_key=' + FRED_API_KEY)
        dom = parseString(response.content)
        observations = dom.getElementsByTagName('observation')
        return observations

    def filter_observations_by_date(self, observations):
        return filter(self.is_good_date, observations)

    def is_good_date(self, observation):
        date = parse_date(observation.getAttribute('date'))
        return date > self.EARLIEST_ALLOWED_DATA

    def observation_values(self, observations):
        return [float(obs.getAttribute('value')) for obs in observations]

    def get_series(self, series):
        raw_observations = self.query_fred_for_series(series)
        salient_observations = self.filter_observations_by_date(raw_observations)
        return self.observation_values(salient_observations)
