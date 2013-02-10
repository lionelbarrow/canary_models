from django.shortcuts import render_to_response
from django.template import RequestContext

from models import RegressionModel, SERIES
from feed import APIDataFeed

import json

DEFAULT_MONTHS_FORWARD = 6

def format_data_as_json(**kwargs):
    arg_dict = {}
    for word, value in kwargs.iteritems():
        arg_dict[word] = value
    return json.dumps(arg_dict)


class DataFeedController(object):

    def all_probit_data(self, months_forward):
        model = self.probit_model(months_forward)
        predictions = model.predict()
        endog, exog, exog_remainder = model.training_arrays()
        return predictions, endog, exog, exog_remainder

    def probit_model(self, months_forward):
        feed = APIDataFeed()
        all_series = {series: feed.get_series(series) for series in SERIES}
        return RegressionModel(all_series, months_forward)


class DataAPIController(object):

    @staticmethod
    def probit_data(request):
        if request.method == "POST":
            months_forward = request.POST["months_forward"]
        else:
            months_forward = DEFAULT_MONTHS_FORWARD
        predictions, endog, exog, exog_remainder = DataFeedController().all_probit_data(months_forward)
        d = format_data_as_json(predictions=predictions, recessions=endog, inputs=exog, remaining_inputs=exog_remainder)
        context = RequestContext(request, {"json_data": d})
        return render_to_response("data.html", context)
