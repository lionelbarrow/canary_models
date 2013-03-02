from datetime import date

from canary_models.models.observation import Observation

class FakeGateway(object):

    def get_series(self, series):
        xml = '<?xml version="1.0" encoding="utf-8" ?><observations>'
        for year in range(70):
            for month in range(12):
                xml += '<observation date="' + str(1960+year) + '-' + str(month+1) + '-1" '
                xml += 'value="' + str(float(year) * .75) + '"/>'
        xml += '</observations>'
        return xml
