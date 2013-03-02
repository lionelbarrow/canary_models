from datetime import date

from canary_models.controllers.data_controller import DataController

start_date = date(year=1960, month=1, day=1)
end_date = date(year=2015, month=1, day=1)

dc = DataController()
json_output = dc.fed_funds_series(start_date, end_date)

f = open('fed_funds.json', 'w')
f.write(json_output)
f.close()
