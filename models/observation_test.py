from datetime import date
from unittest import TestCase

from canary_models.models.observation import Observation

class ObservationTest(TestCase):

    def setUp(self):
        test_date = date(year=2010, day=1, month=1)
        self.observation = Observation("TEST_SERIES", test_date, 55.00)

    def test_date_in_range_too_early(self):
        start_date = date(year=3000, day=1, month=1)
        end_date = date(year=3000, day=31, month=12)
        self.assertFalse(self.observation.in_date_range(start_date, end_date))

    def test_date_in_range_too_late(self):
        start_date = date(year=2000, day=1, month=1)
        end_date = date(year=200, day=31, month=12)
        self.assertFalse(self.observation.in_date_range(start_date, end_date))

    def test_date_in_range_just_right(self):
        start_date = date(year=2000, day=1, month=1)
        end_date = date(year=3000, day=31, month=12)
        self.assertTrue(self.observation.in_date_range(start_date, end_date))

    def test_date_in_range_does_not_include_the_start_date(self):
        start_date = date(year=2010, day=1, month=1)
        end_date = date(year=3000, day=31, month=12)
        self.assertFalse(self.observation.in_date_range(start_date, end_date))

    def test_date_in_range_includes_the_end_date(self):
        start_date = date(year=2000, day=1, month=1)
        end_date = date(year=2010, day=1, month=1)
        self.assertTrue(self.observation.in_date_range(start_date, end_date))
