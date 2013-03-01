from unittest import TestCase
from xml.dom.minidom import parseString

from canary_models.feeds.data_feed import DataFeed

class DataFeedTest(TestCase):
    pass
    #def test_is_good_date_returns_true_correctly(self):
    #    feed = DataFeed()
    #    good_date_dom = parseString('<observation date="2012-9-29" />')
    #    good_date = good_date_dom.getElementsByTagName('observation')[0]

    #    self.assertTrue(feed.is_good_date(good_date))

    #def test_is_good_date_returns_false_correctly(self):
    #    feed = DataFeed()
    #    bad_date_dom = parseString('<observation date="1929-10-20" />')
    #    bad_date = bad_date_dom.getElementsByTagName('observation')[0]

    #    self.assertFalse(feed.is_good_date(bad_date))

    #def test_observation_values_returns_floats(self):
    #    feed = DataFeed()
    #    dom = parseString('<observation value=".12" />').getElementsByTagName('observation')
    #    values = feed.observation_values(dom)

    #    self.assertTrue(isinstance(values[0], float))
