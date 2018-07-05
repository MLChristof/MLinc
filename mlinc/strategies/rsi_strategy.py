from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')
# import datetime
# import os.path
# import sys
# import time

import backtrader as bt


class RsiStrategy(bt.Strategy):
    params = (
        ('maperiod', 14),
        )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        # print('%s' % (dt.isoformat()))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.threshold_long = 30
        self.threshold_short = 70

        self.indicator = bt.indicators.RelativeStrengthIndex(self.datas[0], period=self.params.maperiod)

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
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        # if self.order:
        #     return
        if self.indicator < self.threshold_long:
            self.rsivalue = self.indicator
        # print(self.indicator.array)
        # print(self.indicator.)
        # print(self.code())

    def code(self):
        if self.threshold_short > self.indicator > self.threshold_short-10:
            return 'Code Yellow: RSI={}'.format(self.indicator)
        elif self.indicator >= self.threshold_short:
            return 'Code Red: RSI={}, Possibility to go short!'.format(self.indicator)
        elif self.threshold_long+10 > self.indicator > self.threshold_long:
            return 'Code Yellow: RSI={}'.format(self.indicator)
        elif self.indicator <= self.threshold_long:
            return 'Code Red: RSI={}, Possibility to go long!'.format(self.indicator.lines)
        else:
            return






