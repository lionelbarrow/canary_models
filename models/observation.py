class Observation(object):

    def __init__(self, series_name, date, value):
        self.series_name = series_name
        self.date = date
        self.value = value

    def in_range(self, start_date, end_date):
        pass
