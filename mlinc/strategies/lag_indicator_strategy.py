from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script instrument (in argv[0])
import time

# Import the backtrader platform
import backtrader as bt
import numpy as n

# Import ML indicators
from mlinc.indicators.lag_indicator import MlLagIndicator


class MlLagIndicatorStrategy(bt.Strategy):
    params = (
        ('maperiod', 5),
        )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        # print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.lagindex = [0, 0, 0]
        self.threshold_long = -0.6
        self.threshold_short = 0.95

        self.indicator = MlLagIndicator(self.datas[0], self.datas[1], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])
        # pass

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        self.lagindex.append(self.indicator.lag_index())
        # print(self.lagindex[-1])

        if self.lagindex[-3] > self.lagindex[-2] < self.lagindex[-1] and self.lagindex[-2] < self.threshold_long:
            self.log('Go Long!!! Because lagindex is [{}, {}, {}]'.format(self.lagindex[-3],
                                                                          self.lagindex[-2],
                                                                          self.lagindex[-1]))
            self.order = self.buy()
        elif self.lagindex[-3] < self.lagindex[-2] > self.lagindex[-1] and self.lagindex[-2] > self.threshold_short:
            self.log('Go Short!!! Because lagindex is [{}, {}, {}]'.format(self.lagindex[-3],
                                                                           self.lagindex[-2],
                                                                           self.lagindex[-1]))
            self.order = self.sell()
        else:
            return