import backtrader as bt
import numpy as n
import math


class MlLagIndicator(bt.Indicator):
    lines = ('mlli',)
    params = (('period', 5),)

    def __init__(self):
        self.lines.mlli = bt.Max(-1.0, self.lag_index())

        super(MlLagIndicator, self).__init__()

    def next(self):
        self.lines.mlli[0] = self.lag_index()

    @staticmethod
    def normalize(param):
        """ Normalize closing prices sliding matrices """
        norm = (param[-1] - n.min(param)) / \
               (n.max(param) - n.min(param))
        return norm

    def lag_index(self):
        try:
            return self.normalize(self.close_price_0()) - self.normalize(self.close_price_1())
        except IndexError:
            return 0

    def close_price_0(self):
        return self.datas[0].close.get(size=self.p.period)

    def close_price_1(self):
        return self.datas[1].close.get(size=self.p.period)

