import os

import requests

class FredGateway(object):

    def __init__(self):
        self.FRED_API_URL = 'http://api.stlouisfed.org/fred/series/observations?series_id='
        self.FRED_API_KEY = os.environ.get('FRED_API_KEY', "fake_fred_key")

    def get_series(self, series):
        response = requests.get(self.FRED_API_URL + series + '&api_key=' + self.FRED_API_KEY)
        if response.status_code != 200:
            raise FredException("Error talking to Fred! Status was " + str(response.status_code) + ".")
        else:
            return response.content

class FredException(BaseException):
    pass
