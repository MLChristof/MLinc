import backtrader as bt
import numpy as n
import math as m


class MlLagIndicator(bt.Indicator):
    lines = ('mlli',)
    params = (('period', 3),)

    def normalize(self):
        """ Normalize closing prices sliding matrices """
        norm = (self.open_price()[-1] - n.min(self.open_price())) / \
               (n.max(self.open_price()) - n.min(self.open_price()))
        return norm

    def close_price(self):
        return self.data.close.get(size=self.p.period)

    def open_price(self):
        return self.data.open.get(size=self.p.period)

    def test(self):
        return self.data.open.get(size=self.p.period)


# class SimpleMovingAverage1(bt.indicator):
#     lines = ('sma',)
#     params = (('period', 20),)
#
#     def __init__(self):
#         self.addminperiod(self.params.period)
#
#     def next(self):
#         datasum = m.fsum(self.data.get(size=self.p.period))
#         self.lines.sma[0] = datasum / self.p.period
