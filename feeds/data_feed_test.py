from unittest import TestCase
from xml.dom.minidom import parseString

from canary_models.feeds.data_feed import DataFeed
from canary_models.feeds.fake_gateway import FakeGateway

class DataFeedTest(TestCase):

    def test_get_series_filters_series_by_date(self):
        feed = DataFeed()
        feed.gateway = FakeGateway()
        for obs in feed.get_series("fake_series"):
            self.assertTrue(obs.date > feed.EARLIEST_ALLOWED_DATE)
