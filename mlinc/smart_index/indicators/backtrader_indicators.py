import backtrader as bt
import numpy as n
import math as m


class MlLagIndicator(bt.Indicator):
    lines = ('mlli',)
    params = (('period', 3),)

    # def __init__(self):
        # self.lines.mlli = 100
        # self.data = self.datas[0]

    @property
    def data_array(self):
        return self.data.get(size=self.p.period)

    @property
    def close_price(self):
        return self.data.close[0]

    @property
    def open_price(self):
        return self.data.open[0]

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
