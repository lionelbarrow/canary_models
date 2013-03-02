import os

import requests

class FredGateway(object):

    def get_series(self, series):
        response = requests.get(self.fred_api_url() + series + '&api_key=' + self.fred_api_key())
        if response.status_code != 200:
            raise FredException("Error talking to Fred! Status was " + str(response.status_code) + ".")
        else:
            return response.content

    def fred_api_url(self):
        return 'http://api.stlouisfed.org/fred/series/observations?series_id='

    def fred_api_key(self):
        return os.environ.get('FRED_API_KEY', "fake_fred_key")

class FredException(BaseException):
    pass
