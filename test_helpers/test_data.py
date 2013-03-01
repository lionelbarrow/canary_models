import pickle

class TestData(object):

    def __init__(self):
        test_data = open("test_helpers/pickled_sample_data.txt")
        self.FED_DATA = pickle.load(test_data)
        test_data.close()
