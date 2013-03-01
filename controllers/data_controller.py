from canary_models.models.regression_model import RegressionModel, SERIES
from canary_models.feeds.data_feed import DataFeed
from canary_models.utils.utils import return_as_json

DEFAULT_MONTHS_FORWARD = 6

class DataController(object):

    def __init__(self, testing=False):
        self.testing = testing
        self.data_feed = DataFeed(testing=testing)

    @return_as_json
    def fed_funds_series(self, start_date, end_date):
        return self.data_feed.get_series("FEDFUNDS", start_date, end_date)


class DataAPIController(object):

    def all_probit_data(self, months_forward):
        model = self.probit_model(months_forward)
        predictions = model.predict()
        endog, exog, exog_remainder = model.training_arrays()
        return predictions, endog, exog, exog_remainder

    def probit_model(self, months_forward):
        feed = APIDataFeed()
        all_series = {series: feed.get_series(series) for series in SERIES}
        return RegressionModel(all_series, months_forward)

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
