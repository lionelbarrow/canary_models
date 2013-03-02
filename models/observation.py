class Observation(object):

    def __init__(self, series_name, date, value):
        self.series_name = series_name
        self.date = date
        self.value = value

    def in_date_range(self, start_date, end_date):
        return start_date < self.date and self.date <= end_date

    def to_dict(self):
        return {"series": self.series_name, "date": str(self.date), "value": self.value}
