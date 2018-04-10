import numpy as n


class MlLagIndicator(object):
    def __init__(self, data, period):
        self.data = data
        self.period = period

    def test(self):
        return self.data
