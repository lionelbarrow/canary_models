from xml.dom.minidom import parseString
from datetime import date

import requests

from canary_models.utils.utils import parse_date
from canary_models.feeds.fred_gateway import FredGateway
from canary_models.models.observation import Observation

class DataFeed(object):

    def __init__(self):
        self.gateway = FredGateway()
        self.EARLIEST_ALLOWED_DATE = date(year=1964, day=1, month=1)

    def get_series(self, series):
        raw_xml = self._get_series(series)
        observations = self._xml_to_observations(raw_xml, series)
        return self._filter_observations_by_date(observations)

    def _get_series(self, series):
        return self.gateway.get_series(series)

    def _xml_to_observations(self, raw_xml, series):
        dom = parseString(raw_xml)
        xml_observations = dom.getElementsByTagName('observation')
        observations = [self._new_observation(xml_obs, series) for xml_obs in xml_observations]
        return observations

    def _new_observation(self, domElement, series):
        date = parse_date(domElement.getAttribute("date"))
        return Observation(series, date, float(domElement.getAttribute("value")))

    def _filter_observations_by_date(self, observations):
        return filter(self._observation_valid, observations)

    def _observation_valid(self, observation):
        return observation.date > self.EARLIEST_ALLOWED_DATE
