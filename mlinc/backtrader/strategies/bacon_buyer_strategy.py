from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')
# import datetime
# import os.path
# import sys
# import time
import numpy as n

import backtrader as bt


class BaconBuyerStrategy(bt.Strategy):
    # TODO Add smart staking/sizing
    # TODO Check Commission settings
    params = (
        ('maperiod', 48),
        ('RRR', 5),
        ('minSL', 2),  # in pips
        ('stakepercent', 5)
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

        self.indicator = bt.indicators.HullMovingAverage(self.datas[0], period=self.params.maperiod)
        # self.indicatorSMA = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

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
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        hma_data = n.array((self.indicator.lines.hma[-6],
                            self.indicator.lines.hma[-5],
                            self.indicator.lines.hma[-4],
                            self.indicator.lines.hma[-3],
                            self.indicator.lines.hma[-2],
                            self.indicator.lines.hma[-1],
                            self.indicator.lines.hma[0]))

        hma_diff = n.diff(hma_data)

        # Open Long Position on local minimum HMA
        # (if slope on last day of HMA is pos and 5 days before neg)
        if hma_diff[5] > 0 \
            and hma_diff[4] < 0 \
            and hma_diff[3] < 0 \
            and hma_diff[2] < 0 \
            and hma_diff[1] < 0 \
            and hma_diff[0] < 0:
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # determine Entry price, SL & TP
            EntryLong = self.datas[0]
            SL_long = self.indicator.lines.hma[0]
            if EntryLong - SL_long > self.params.minSL:
                SL_long = self.indicator.lines.hma[0]
            else:
                SL_long = EntryLong - self.params.minSL

            TP_long = (1/self.params.RRR)*(EntryLong-SL_long)+EntryLong
            #Stake Size
            stake_size = 2E-4*self.params.stakepercent*self.broker.getvalue()/(EntryLong-SL_long)
            # place order
            self.order = self.buy_bracket(limitprice=TP_long, price=EntryLong, stopprice=SL_long, size=stake_size)

        # Open Short Position on local maximum HMA
        # (if slope on last day of HMA is neg and 5 days before pos)
        if hma_diff[5] < 0 \
            and hma_diff[4] > 0 \
            and hma_diff[3] > 0 \
            and hma_diff[2] > 0 \
            and hma_diff[1] > 0 \
            and hma_diff[0] > 0:
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            # determine Entry price, SL & TP
            EntryShort = self.datas[0]
            SL_short = self.indicator.lines.hma[0]
            if  SL_short - EntryShort > self.params.minSL:
                SL_short = self.indicator.lines.hma[0]
            else:
                SL_short = EntryShort + self.params.minSL

            TP_short = (-1/self.params.RRR)*(SL_short - EntryShort) + EntryShort
            #Stake Size
            stake_size = 2E-4*self.params.stakepercent*self.broker.getvalue()/(SL_short-EntryShort)
            print(SL_short-EntryShort)
            print(self.broker.getvalue())
            print(stake_size)
            # place order
            self.order = self.sell_bracket(price=EntryShort,stopprice=SL_short,limitprice=TP_short, size=stake_size)







