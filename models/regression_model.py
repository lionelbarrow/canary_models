import numpy as np
import statsmodels.api as sm

SERIES = ('FEDFUNDS', 'USREC', 'TB3MS', 'GS10')

class RegressionModel(object):

    def __init__(self, all_series, months_forward):
        self.series = all_series
        self.exogenous_variables = ["FEDFUNDS", "TB3MS", "GS10"]
        self.endogenous_variables = ["USREC"]
        self.months_forward = months_forward

    def validate_input(self):
        self.validate_series_names(self.series.keys())
        self.validate_series_lengths(self.series)

    def validate_series_names(self, names):
        if not set(names).issubset(set(SERIES)):
            raise ValueError("all_series may only include the keys " + ", ".join(SERIES) + ".")

    def validate_series_lengths(self, series):
        first_length = len( series[series.keys()[0]] )
        for name in series.keys():
            current_length = len(series[name])
            if current_length != first_length:
                raise ValueError("Series " + name + " was wrong length. Got " + str(current_length) + ", expected " + str(first_length) + ".")

    def build_model(self):
        endo, exo, remaining_exo = self.training_arrays()
        probit_model = sm.Probit(endo, exo)
        probit_result = probit_model.fit()
        return probit_model, probit_result, remaining_exo

    def training_arrays(self):
        endog, endog_remainder = self.build_and_chop_series(self.endogenous_variables, True)
        exog, exog_remainder = self.build_and_chop_series(self.exogenous_variables, False)
        return endog, exog, exog_remainder

    def build_and_chop_series(self, variables, chop_front):
        built_input = self.build_array(self.series, variables)
        chopped_array, remainder = self.chop_array(built_input, chop_front)
        return chopped_array, remainder

    def build_array(self, all_series, variables):
        return np.array([all_series[v] for v in variables]).T

    def chop_array(self, input, chop_front=False):
        if chop_front:
            chopped_array = np.array(input[self.months_forward:, :])
            remainder = np.array(input[:self.months_forward, :])
        else:
            chopped_array = np.array(input[:-self.months_forward, :])
            remainder = np.array(input[-self.months_forward:, :])
        return chopped_array, remainder

    def predict(self):
        self.validate_input()
        probit_model, probit_result, remaining_exo = self.build_model()
        predictions = probit_model.predict(probit_result.params, exog=remaining_exo)
        return predictions
