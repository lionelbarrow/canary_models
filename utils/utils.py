from datetime import date

import json

def return_as_json(f):
    def json_wrapped(*args):
        return json.dumps(f(*args))
    return json_wrapped

def parse_date(datestr):
    nums = map(int, datestr.split('-'))
    return date(year=nums[0], month=nums[1], day=nums[2])
