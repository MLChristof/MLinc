from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# datapath = os.path.join(modpath, 'backtrader-master\datas\orcl-1995-2014.txt')

# Import the backtrader platform
import backtrader as bt

# Import ML indicators
from mlinc.backtrader.indicators.lag_indicator import MlLagIndicator


class MlLagIndicatorStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('threshold', 0.6),
        ('SL', 0.02),
        ('TP', 0.02),
        ('printlog', False),
        )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
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

        # check if position is open
        the_size = self.getposition(data=self.datas[0]).size


        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        self.lagindex.append(self.indicator.lag_index())
        # print(self.lagindex[-1])

        # long position
        if self.lagindex[-1] < -self.params.threshold and the_size == 0:
            self.log('Go Long!!! Because lagindex is [{}]'.format(self.lagindex[-1]))
            # self.order = self.buy()
            self.order = self.buy_bracket(limitprice=self.dataclose*(1+self.params.TP),
                                          limitexec=bt.Order.Limit,
                                          exectype=bt.Order.Market,
                                          stopprice=self.dataclose*(1-self.params.SL),
                                          stopexec=bt.Order.Stop,
                                          )
        # short position
        elif self.lagindex[-1] > self.params.threshold and the_size == 0:
            self.log('Go Short!!! Because lagindex is [{}]'.format(self.lagindex[-1]))

            # self.order = self.sell()
            self.order = self.sell_bracket(limitprice=self.dataclose*(1-self.params.TP),
                                           limitexec=bt.Order.Limit,
                                           exectype=bt.Order.Market,
                                           stopprice=self.dataclose*(1+self.params.SL),
                                           stopexec=bt.Order.Stop,
                                           )

        else:
            return

    def stop(self):
        self.log('threshold: {0:.2f} maperiod: {1:.1f} SL: {2:.4f} TP: {3:.4f} Ending Value: {4:8.2f}'.format(
            self.params.threshold,
            self.params.maperiod,
            self.params.SL,
            self.params.TP,
            self.broker.getvalue()),
            doprint=True
                )


